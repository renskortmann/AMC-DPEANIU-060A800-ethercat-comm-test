import struct
import time
import csv
import queue
import threading
from collections import deque
from pathlib import Path

import numpy as np
try:
    import pysoem
    _PYSOEM_AVAILABLE = True
except (ImportError, OSError):
    pysoem = None
    _PYSOEM_AVAILABLE = False
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ------------ CONFIGURATION ------------
ADAPTER_NAME = r"\Device\NPF_{FEDAB1B5-C8AC-4C77-9EAB-A081EF22B39C}"

LOG_FILE = "current_and_position_log.dat"
DATA_DIR  = Path("data")            # all .dat and .csv files are stored here

CYCLE_TIME_S = 0.001      # 1 ms target cycle
PRINT_INTERVAL_S = 1.0    # print once per second
LOG_BATCH_SIZE = 100      # flush every 100 samples

GUI_REFRESH_MS = 50       # ~20 Hz GUI redraw rate, decoupled from the 1kHz acquisition loop
FULL_REDRAW_EVERY = 5     # full matplotlib redraw every N frames; blit on the rest (~4x faster)
WINDOW_MIN_S = 0.1        # shared time-axis slider range (seconds)
WINDOW_MAX_S = 5.0
WINDOW_DEFAULT_S = 2.0
WINDOW_STEP_S = 0.1
BUFFER_MAXLEN = 20000     # ~20s of samples at 1kHz -- comfortably above WINDOW_MAX_S

FFT_FREQ_MIN = 50         # FFT max-frequency slider range (Hz)
FFT_FREQ_MAX = 250
FFT_FREQ_STEP = 10
FFT_FREQ_DEFAULT = 250

# Binary .dat log format: 8-byte magic header + fixed-size records
LOG_MAGIC = b"PDOBIN01"
RECORD_STRUCT = struct.Struct("<dffii")  # elapsed_s, cycle_ms, current_A, position_counts, velocity_counts_per_sec
# ---------------------------------------


def connect_and_configure(adapter_name):
    """Open the EtherCAT master, read K_P via SDO, map PDOs, and go OP state."""

    master = pysoem.Master()
    master.open(adapter_name)

    if master.config_init() <= 0:
        raise RuntimeError("No EtherCAT slaves found")

    slave = master.slaves[0]

    print(f"Connected to slave: {slave.name}")

    #
    # Read K_P once using SDO
    #
    raw_max_peak = struct.unpack(
        "<H",
        slave.sdo_read(0x20D8, 0x0C)
    )[0]

    k_p_amps = raw_max_peak / 10.0

    print(f"Maximum Peak Current = {k_p_amps:.1f} A")

    #
    # Configure PDO mapping from slave defaults
    #
    master.config_map()

    #
    # Go operational
    #
    master.state = pysoem.OP_STATE
    master.send_processdata()
    master.receive_processdata(2000)
    master.write_state()

    # OP state is only confirmed once the slave sees live process-data frames
    reached_op_state = False
    for _ in range(40):
        master.send_processdata()
        master.receive_processdata(2000)
        master.state_check(pysoem.OP_STATE, 50000)
        if master.state == pysoem.OP_STATE:
            reached_op_state = True
            break

    if not reached_op_state:
        raise RuntimeError("Failed to reach OP state")

    print("EtherCAT operational.")

    return master, slave, k_p_amps


def acquisition_loop(master, slave, k_p_amps, buffer, buffer_lock, stop_event, command_queue, status_queue):
    """Cyclic PDO read loop, meant to run in a background thread.

    Always appends (elapsed_s, position_counts, current_amps) samples to
    `buffer` (guarded by `buffer_lock`) for the scope GUI -- this runs
    independently of file logging.

    Binary (.dat) file logging is entirely driven by commands received on
    `command_queue`: ("start", base_filename), ("pause",), ("resume",),
    ("stop",). This thread is the sole owner of the log file (opens, writes,
    closes it) to avoid concurrent access from the GUI thread. Status
    updates/errors are posted to `status_queue` for the GUI to display.

    Runs until `stop_event` is set.
    """

    log_state = "IDLE"       # IDLE -> RUNNING <-> PAUSED -> (stop) -> IDLE
    log_file = None
    log_path = None
    log_byte_buffer = bytearray()

    def handle_command(command):
        nonlocal log_state, log_file, log_path, log_byte_buffer

        action = command[0]

        if action == "start":
            if log_state != "IDLE":
                return

            base_path = Path(command[1])
            timestamp = time.strftime("%d-%m-%Y_%H-%M-%S")
            suffix = base_path.suffix or ".dat"
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            new_path = DATA_DIR / f"{base_path.stem}_{timestamp}{suffix}"

            try:
                new_file = open(new_path, "wb")
                new_file.write(LOG_MAGIC)
            except OSError as exc:
                status_queue.put(("error", str(exc)))
                return

            log_file = new_file
            log_path = str(new_path)
            log_byte_buffer = bytearray()
            log_state = "RUNNING"
            status_queue.put(("started", log_path))

        elif action == "pause":
            if log_state == "RUNNING":
                log_state = "PAUSED"
                status_queue.put(("paused", log_path))

        elif action == "resume":
            if log_state == "PAUSED":
                log_state = "RUNNING"
                status_queue.put(("resumed", log_path))

        elif action == "stop":
            if log_state in ("RUNNING", "PAUSED"):
                if log_byte_buffer:
                    log_file.write(bytes(log_byte_buffer))
                    log_byte_buffer.clear()
                log_file.close()
                status_queue.put(("stopped", log_path))
                log_state = "IDLE"
                log_file = None

    start_time = time.perf_counter()
    next_cycle = start_time

    last_print = start_time
    last_loop_time = start_time

    sample_count = 0

    while not stop_event.is_set():

        #
        # Process any pending Start/Pause/Resume/Stop commands from the GUI
        #
        while True:
            try:
                command = command_queue.get_nowait()
            except queue.Empty:
                break
            handle_command(command)

        #
        # Measure actual cycle interval
        #
        now = time.perf_counter()
        actual_cycle_ms = (now - last_loop_time) * 1000.0
        last_loop_time = now

        #
        # PDO exchange
        #
        master.send_processdata()
        wkc = master.receive_processdata(2000)

        pdo = slave.input

        #
        # AMC default TPDO layout
        #
        status_word = struct.unpack_from("<H", pdo, 0)[0]
        position = struct.unpack_from("<i", pdo, 2)[0]
        velocity = struct.unpack_from("<i", pdo, 6)[0]
        raw_current = struct.unpack_from("<h", pdo, 10)[0]

        current_amps = raw_current * k_p_amps / 8192.0

        elapsed = now - start_time

        with buffer_lock:
            buffer.append((elapsed, position, current_amps))

        #
        # Binary log write (only while logging is running)
        #
        if log_state == "RUNNING":
            log_byte_buffer += RECORD_STRUCT.pack(
                elapsed, actual_cycle_ms, current_amps, position, velocity
            )

            if len(log_byte_buffer) >= LOG_BATCH_SIZE * RECORD_STRUCT.size:
                log_file.write(bytes(log_byte_buffer))
                log_byte_buffer.clear()

        sample_count += 1

        #
        # Print once per second
        #
        if (now - last_print) >= PRINT_INTERVAL_S:

            avg_freq = sample_count / elapsed

            print(
                f"t={elapsed:8.3f}s  "
                f"WKC={wkc}/{master.expected_wkc}  "
                f"SW=0x{status_word:04X}  "
                f"I={current_amps:+8.3f}A  "
                f"Pos={position:+10d}  "
                f"Vel={velocity:+10d}  "
                f"dt={actual_cycle_ms:6.3f}ms  "
                f"avg={avg_freq:7.1f}Hz"
            )

            last_print = now

        #
        # Absolute-time scheduling
        #
        next_cycle += CYCLE_TIME_S

        remaining = next_cycle - time.perf_counter()

        if remaining > 0:
            time.sleep(remaining)
        else:
            #
            # We're behind schedule.
            # Skip sleeping and continue.
            #
            pass

    #
    # Flush and close any still-open log file on shutdown, even if the user
    # never clicked "Stop Log".
    #
    if log_state in ("RUNNING", "PAUSED") and log_file is not None:
        if log_byte_buffer:
            log_file.write(bytes(log_byte_buffer))
            log_byte_buffer.clear()
        log_file.close()


def convert_dat_to_csv(dat_path):
    """Convert a completed binary .dat log file to a .csv file with the same
    columns as the original CSV logger. Returns the path to the created CSV.
    """

    dat_path = Path(dat_path)
    csv_path = dat_path.with_suffix(".csv")

    with open(dat_path, "rb") as src:

        magic = src.read(len(LOG_MAGIC))

        if magic != LOG_MAGIC:
            raise ValueError(f"'{dat_path}' is not a recognized .dat log file")

        with open(csv_path, "w", newline="") as dst:

            writer = csv.writer(dst)

            writer.writerow([
                "elapsed_s",
                "cycle_ms",
                "current_A",
                "position_counts",
                "velocity_counts_per_sec"
            ])

            while True:
                chunk = src.read(RECORD_STRUCT.size)

                if not chunk:
                    break

                if len(chunk) != RECORD_STRUCT.size:
                    raise ValueError(f"'{dat_path}' contains a truncated record")

                elapsed, cycle_ms, current_amps, position, velocity = RECORD_STRUCT.unpack(chunk)

                writer.writerow([
                    f"{elapsed:.6f}",
                    f"{cycle_ms:.3f}",
                    f"{current_amps:.5f}",
                    position,
                    velocity
                ])

    return csv_path


def simulation_acquisition_loop(buffer, buffer_lock, stop_event, command_queue, status_queue):
    """Generates synthetic position and current data at ~1 kHz for use when
    real EtherCAT hardware is unavailable.  Uses the same command_queue /
    status_queue protocol as acquisition_loop so that binary file logging
    works identically in simulation mode.
    """

    SIM_POS_AMP   = 50000  # peak position amplitude (counts)
    SIM_POS_FREQ  = 0.5    # position oscillation (Hz)
    SIM_CUR_AMP   = 2.5    # peak current amplitude (A)
    SIM_CUR_FREQ  = 3.0    # current oscillation (Hz)
    SIM_NOISE_AMP = 0.05   # current noise (A)

    log_state = "IDLE"       # IDLE -> RUNNING <-> PAUSED -> (stop) -> IDLE
    log_file = None
    log_path = None
    log_byte_buffer = bytearray()

    def handle_command(command):
        nonlocal log_state, log_file, log_path, log_byte_buffer

        action = command[0]

        if action == "start":
            if log_state != "IDLE":
                return

            base_path = Path(command[1])
            timestamp = time.strftime("%d-%m-%Y-%H-%M-%S")
            suffix = base_path.suffix or ".dat"
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            new_path = DATA_DIR / f"{base_path.stem}_{timestamp}{suffix}"

            try:
                new_file = open(new_path, "wb")
                new_file.write(LOG_MAGIC)
            except OSError as exc:
                status_queue.put(("error", str(exc)))
                return

            log_file = new_file
            log_path = str(new_path)
            log_byte_buffer = bytearray()
            log_state = "RUNNING"
            status_queue.put(("started", log_path))

        elif action == "pause":
            if log_state == "RUNNING":
                log_state = "PAUSED"
                status_queue.put(("paused", log_path))

        elif action == "resume":
            if log_state == "PAUSED":
                log_state = "RUNNING"
                status_queue.put(("resumed", log_path))

        elif action == "stop":
            if log_state in ("RUNNING", "PAUSED"):
                if log_byte_buffer:
                    log_file.write(bytes(log_byte_buffer))
                    log_byte_buffer.clear()
                log_file.close()
                status_queue.put(("stopped", log_path))
                log_state = "IDLE"
                log_file = None

    start_time = time.perf_counter()
    next_cycle = start_time
    last_loop_time = start_time
    prev_position = 0

    while not stop_event.is_set():

        while True:
            try:
                command = command_queue.get_nowait()
            except queue.Empty:
                break
            handle_command(command)

        now = time.perf_counter()
        actual_cycle_ms = (now - last_loop_time) * 1000.0
        last_loop_time = now
        elapsed = now - start_time

        position = int(SIM_POS_AMP * np.sin(2 * np.pi * SIM_POS_FREQ * elapsed))
        velocity = int((position - prev_position) / CYCLE_TIME_S)
        prev_position = position
        current_amps = (
            SIM_CUR_AMP * np.sin(2 * np.pi * SIM_CUR_FREQ * elapsed)
            + SIM_NOISE_AMP * (2.0 * np.random.random() - 1.0)
        )

        with buffer_lock:
            buffer.append((elapsed, position, current_amps))

        if log_state == "RUNNING":
            log_byte_buffer += RECORD_STRUCT.pack(
                elapsed, actual_cycle_ms, current_amps, position, velocity
            )
            if len(log_byte_buffer) >= LOG_BATCH_SIZE * RECORD_STRUCT.size:
                log_file.write(bytes(log_byte_buffer))
                log_byte_buffer.clear()

        next_cycle += CYCLE_TIME_S
        remaining = next_cycle - time.perf_counter()
        if remaining > 0:
            time.sleep(remaining)

    if log_state in ("RUNNING", "PAUSED") and log_file is not None:
        if log_byte_buffer:
            log_file.write(bytes(log_byte_buffer))
            log_byte_buffer.clear()
        log_file.close()


class ScopeGUI:
    """Tkinter window with a 2x2 graph grid: scrolling position/current scope
    traces on the left sharing an adjustable time-axis window length, and
    their live FFTs on the right sharing an adjustable max-frequency axis,
    plus binary (.dat) logging controls (start/pause/resume/stop, filename
    entry, convert to CSV).
    """

    def __init__(self, root, buffer, buffer_lock, stop_event, command_queue, status_queue, sim_warning=None):
        self.root = root
        self.buffer = buffer
        self.buffer_lock = buffer_lock
        self.stop_event = stop_event
        self.command_queue = command_queue
        self.status_queue = status_queue

        self.log_state = "IDLE"
        self.last_closed_log_path = None

        self.window_seconds = tk.DoubleVar(value=WINDOW_DEFAULT_S)
        self.fft_max_freq = tk.IntVar(value=FFT_FREQ_DEFAULT)
        self.filename_var = tk.StringVar(value=LOG_FILE)
        self.status_var = tk.StringVar(value="Not logging.")

        root.title(
            "EtherCAT Drive Scope - Position & Current  [SIMULATION]"
            if sim_warning else
            "EtherCAT Drive Scope - Position & Current"
        )
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = Figure(figsize=(11, 6), dpi=100)
        self.ax_position = self.figure.add_subplot(2, 2, 1)
        self.ax_current = self.figure.add_subplot(2, 2, 3, sharex=self.ax_position)
        self.ax_fft_position = self.figure.add_subplot(2, 2, 2)
        self.ax_fft_current = self.figure.add_subplot(2, 2, 4, sharex=self.ax_fft_position)

        self.ax_position.set_ylabel("Position (counts)")
        self.ax_position.set_title("Position")
        self.ax_position.tick_params(labelbottom=False)

        self.ax_current.set_ylabel("Current (A)")
        self.ax_current.set_xlabel("Time (s)")
        self.ax_current.set_title("Current")

        self.ax_fft_position.set_ylabel("Magnitude")
        self.ax_fft_position.set_title("Position FFT")
        self.ax_fft_position.tick_params(labelbottom=False)

        self.ax_fft_current.set_ylabel("Magnitude")
        self.ax_fft_current.set_xlabel("Frequency (Hz)")
        self.ax_fft_current.set_title("Current FFT")

        self.line_position, = self.ax_position.plot([], [], color="tab:blue")
        self.line_current, = self.ax_current.plot([], [], color="tab:orange")
        self.line_fft_position, = self.ax_fft_position.plot([], [], color="tab:green")
        self.line_fft_current, = self.ax_fft_current.plot([], [], color="tab:red")

        self.figure.tight_layout()

        # Blitting: mark every data line as "animated" so it is excluded from
        # the background snapshot. The background (axes frames, tick labels,
        # grid) is only re-rendered every FULL_REDRAW_EVERY frames; all other
        # frames restore the cached background and blit only the lines —
        # typically 10-20× faster than a full draw.
        for _line in (self.line_position, self.line_current,
                      self.line_fft_position, self.line_fft_current):
            _line.set_animated(True)

        # Seed xlim so the axes look right before the first data arrives.
        self.ax_position.set_xlim(-WINDOW_DEFAULT_S, 0.0)
        self.ax_fft_position.set_xlim(0, FFT_FREQ_DEFAULT)

        self._blit_bg = None          # cached background (captured after full draw)
        self._blit_counter = 0        # counts refresh calls since last full draw
        self._needs_full_draw = True  # forces a full draw on first refresh

        # Simulation warning banner — spans full width at the very top.
        if sim_warning:
            tk.Label(
                main_frame,
                text=f"\u26a0  SIMULATION MODE \u2014 {sim_warning}",
                background="#c0392b",
                foreground="white",
                font=("TkDefaultFont", 10, "bold"),
                anchor="w",
                padx=8,
                pady=4,
            ).pack(side=tk.TOP, fill=tk.X)

        # Horizontal content area: controls column on the left, canvas on the right.
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        #
        # Left controls column
        #
        controls_panel = ttk.Frame(content_frame, padding=8)
        controls_panel.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Separator(content_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y)

        # Time-axis window slider (vertical, top = max window)
        ttk.Label(controls_panel, text="Time window (s)").pack(anchor="w")
        self.slider = tk.Scale(
            controls_panel,
            from_=WINDOW_MAX_S,
            to=WINDOW_MIN_S,
            resolution=WINDOW_STEP_S,
            orient=tk.VERTICAL,
            variable=self.window_seconds,
        )
        self.slider.pack(fill=tk.Y, expand=True)

        ttk.Separator(controls_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        # FFT max-frequency slider (vertical, top = max frequency)
        ttk.Label(controls_panel, text="Max Freq (Hz)").pack(anchor="w")
        self.fft_freq_slider = tk.Scale(
            controls_panel,
            from_=FFT_FREQ_MAX,
            to=FFT_FREQ_MIN,
            resolution=FFT_FREQ_STEP,
            orient=tk.VERTICAL,
            variable=self.fft_max_freq,
        )
        self.fft_freq_slider.pack(fill=tk.Y, expand=True)

        ttk.Separator(controls_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        # Logging controls
        ttk.Label(controls_panel, text="Log filename:").pack(anchor="w")
        self.filename_entry = ttk.Entry(controls_panel, textvariable=self.filename_var)
        self.filename_entry.pack(fill=tk.X, pady=(2, 0))

        self.log_toggle_button = ttk.Button(
            controls_panel, text="Start Log", command=self.on_log_toggle_click
        )
        self.log_toggle_button.pack(fill=tk.X, pady=(6, 0))

        self.stop_log_button = ttk.Button(
            controls_panel, text="Stop Log", command=self.on_stop_log_click, state=tk.DISABLED
        )
        self.stop_log_button.pack(fill=tk.X, pady=(4, 0))

        self.convert_button = ttk.Button(
            controls_panel, text="Convert to CSV", command=self.on_convert_click, state=tk.DISABLED
        )
        self.convert_button.pack(fill=tk.X, pady=(4, 0))

        ttk.Label(
            controls_panel, textvariable=self.status_var, wraplength=150, justify=tk.LEFT
        ).pack(fill=tk.X, pady=(8, 0))

        #
        # Canvas — fills the remaining space to the right of the controls column
        #
        self.canvas = FigureCanvasTkAgg(self.figure, master=content_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Invalidate the blit background whenever the axes parameters change.
        self.canvas.mpl_connect("resize_event", self._invalidate_blit_bg)
        self.window_seconds.trace_add("write", self._invalidate_blit_bg)
        self.fft_max_freq.trace_add("write", self._invalidate_blit_bg)

        self.root.after(GUI_REFRESH_MS, self.refresh)

    def on_log_toggle_click(self):
        if self.log_state == "IDLE":
            self.command_queue.put(("start", self.filename_var.get()))
        elif self.log_state == "RUNNING":
            self.command_queue.put(("pause",))
        elif self.log_state == "PAUSED":
            self.command_queue.put(("resume",))

    def on_stop_log_click(self):
        if self.log_state in ("RUNNING", "PAUSED"):
            self.command_queue.put(("stop",))

    def on_convert_click(self):
        if not self.last_closed_log_path:
            self.status_var.set("No completed log file to convert yet.")
            return

        dat_path = self.last_closed_log_path
        self.convert_button.config(state=tk.DISABLED)

        def worker():
            try:
                csv_path = convert_dat_to_csv(dat_path)
                self.status_queue.put(("converted", str(csv_path)))
            except (OSError, ValueError) as exc:
                self.status_queue.put(("convert_error", str(exc)))

        threading.Thread(target=worker, daemon=True).start()

    def _drain_status_queue(self):
        while True:
            try:
                event, payload = self.status_queue.get_nowait()
            except queue.Empty:
                break

            if event == "started":
                self.log_state = "RUNNING"
                self.log_toggle_button.config(text="Pause Log")
                self.stop_log_button.config(state=tk.NORMAL)
                self.filename_entry.config(state=tk.DISABLED)
                self.status_var.set(f"Logging to: {payload}")

            elif event == "paused":
                self.log_state = "PAUSED"
                self.log_toggle_button.config(text="Resume Log")
                self.status_var.set(f"Paused. File: {payload}")

            elif event == "resumed":
                self.log_state = "RUNNING"
                self.log_toggle_button.config(text="Pause Log")
                self.status_var.set(f"Logging to: {payload}")

            elif event == "stopped":
                self.log_state = "IDLE"
                self.log_toggle_button.config(text="Start Log")
                self.stop_log_button.config(state=tk.DISABLED)
                self.filename_entry.config(state=tk.NORMAL)
                self.last_closed_log_path = payload
                self.convert_button.config(state=tk.NORMAL)
                self.status_var.set(f"Stopped. Last file: {payload}")

            elif event == "error":
                self.status_var.set(f"Error: {payload}")

            elif event == "converted":
                self.convert_button.config(state=tk.NORMAL)
                self.status_var.set(f"Converted to: {payload}")

            elif event == "convert_error":
                self.convert_button.config(state=tk.NORMAL)
                self.status_var.set(f"Conversion failed: {payload}")

    def _invalidate_blit_bg(self, *_):
        """Force a full matplotlib redraw on the next refresh cycle.
        Called on canvas resize and when the time-window or FFT-frequency
        slider changes so the axes decorations are redrawn with new limits.
        """
        self._needs_full_draw = True

    def refresh(self):
        if self.stop_event.is_set():
            return

        self._drain_status_queue()

        with self.buffer_lock:
            snapshot = list(self.buffer)

        if snapshot:
            window = self.window_seconds.get()
            now = snapshot[-1][0]
            cutoff = now - window

            visible = [s for s in snapshot if s[0] >= cutoff]

            times     = [s[0] for s in visible]
            positions = [s[1] for s in visible]
            currents  = [s[2] for s in visible]

            # Express x as "seconds before now" so xlim stays fixed at
            # [-window, 0] — a stable coordinate space that allows blitting
            # without the axes drifting between full redraws.
            rel_times = [t - now for t in times]

            self.line_position.set_data(rel_times, positions)
            self.line_current.set_data(rel_times, currents)

            self._blit_counter += 1
            full_draw = self._needs_full_draw or (self._blit_counter % FULL_REDRAW_EVERY == 0)

            if full_draw:
                self._needs_full_draw = False
                self.ax_position.set_xlim(-window, 0.0)
                self.ax_position.relim()
                self.ax_position.autoscale_view(scalex=False, scaley=True)
                self.ax_current.relim()
                self.ax_current.autoscale_view(scalex=False, scaley=True)
                self._update_fft_plots(times, positions, currents)
                self.canvas.draw()
                self._blit_bg = self.canvas.copy_from_bbox(self.figure.bbox)
            else:
                # Fast path: restore cached background and blit only the lines.
                self.canvas.restore_region(self._blit_bg)
                self.ax_position.draw_artist(self.line_position)
                self.ax_current.draw_artist(self.line_current)
                self.ax_fft_position.draw_artist(self.line_fft_position)
                self.ax_fft_current.draw_artist(self.line_fft_current)
                self.canvas.blit(self.figure.bbox)

        self.root.after(GUI_REFRESH_MS, self.refresh)

    def _update_fft_plots(self, times, positions, currents):
        if len(times) < 2:
            return

        # actual sample spacing (not nominal), to tolerate cycle-time jitter
        dt = (times[-1] - times[0]) / (len(times) - 1)
        if dt <= 0:
            return

        freqs = np.fft.rfftfreq(len(times), d=dt)
        pos_mag = np.abs(np.fft.rfft(np.asarray(positions) - np.mean(positions)))
        cur_mag = np.abs(np.fft.rfft(np.asarray(currents) - np.mean(currents)))

        max_freq = self.fft_max_freq.get()
        mask = freqs <= max_freq
        if not mask.any():
            return

        self.line_fft_position.set_data(freqs[mask], pos_mag[mask])
        self.line_fft_current.set_data(freqs[mask], cur_mag[mask])

        self.ax_fft_position.set_xlim(0, max_freq)

        self.ax_fft_position.relim()
        self.ax_fft_position.autoscale_view(scalex=False, scaley=True)
        self.ax_fft_current.relim()
        self.ax_fft_current.autoscale_view(scalex=False, scaley=True)

    def on_close(self):
        self.stop_event.set()
        self.root.destroy()


def main():

    master = None
    slave = None
    k_p_amps = None
    sim_warning = None

    if not _PYSOEM_AVAILABLE:
        sim_warning = "pysoem not available (missing DLL). Showing simulated data."
        print(f"WARNING: {sim_warning}")
    else:
        try:
            master, slave, k_p_amps = connect_and_configure(ADAPTER_NAME)
        except Exception as exc:
            sim_warning = f"Hardware unavailable ({exc}). Showing simulated data."
            print(f"WARNING: {sim_warning}")

    buffer = deque(maxlen=BUFFER_MAXLEN)
    buffer_lock = threading.Lock()
    stop_event = threading.Event()
    command_queue = queue.Queue()
    status_queue = queue.Queue()

    if sim_warning:
        acq_thread = threading.Thread(
            target=simulation_acquisition_loop,
            args=(buffer, buffer_lock, stop_event, command_queue, status_queue),
            daemon=True,
        )
    else:
        acq_thread = threading.Thread(
            target=acquisition_loop,
            args=(master, slave, k_p_amps, buffer, buffer_lock, stop_event, command_queue, status_queue),
            daemon=True,
        )
    acq_thread.start()

    root = tk.Tk()
    ScopeGUI(root, buffer, buffer_lock, stop_event, command_queue, status_queue, sim_warning=sim_warning)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

    print("\nStopping logger...")

    stop_event.set()
    acq_thread.join(timeout=5.0)

    if master is not None:
        master.close()


if __name__ == "__main__":
    main()
