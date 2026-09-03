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

CYCLE_TIME_S = 0.010      # 10 ms target cycle (100 Hz PDO rate)
PRINT_INTERVAL_S = 1.0    # print once per second (~100 samples at 100Hz)
LOG_BATCH_SIZE = 50       # flush every 50 samples (now ~500ms at 100Hz, was ~500ms at 1kHz)

GUI_REFRESH_MS = 100      # ~10 Hz GUI redraw rate, decoupled from 100Hz acquisition loop
FULL_REDRAW_EVERY = 5     # full matplotlib redraw every N frames; blit on the rest (~4x faster)
WINDOW_MIN_S = 0.1        # shared time-axis slider range (seconds)
WINDOW_MAX_S = 5.0
WINDOW_DEFAULT_S = 2.0
WINDOW_STEP_S = 0.1
FAULT_WINDOW_S = 2.0      # Track cycle times within this window for recent fault diagnostics
BUFFER_MAXLEN = 2000      # ~20s of samples at 100Hz PDO rate (was 20000 at 1kHz)

FFT_FREQ_MIN = 50         # FFT max-frequency slider range (Hz)
FFT_FREQ_MAX = 250
FFT_FREQ_STEP = 10
FFT_FREQ_DEFAULT = 250

# CiA402 Controlword (0x6040) commands and masked Statusword (0x6041) states.
# Assumes Controlword/Statusword sit at RxPDO/TxPDO byte offset 0 (AMC default).
CIA402_CW_FAULT_RESET = 0x0080
CIA402_CW_DISABLE_VOLTAGE = 0x0000
CIA402_CW_SHUTDOWN = 0x0006
CIA402_CW_SWITCH_ON = 0x0007
CIA402_CW_ENABLE_OPERATION = 0x000F

CIA402_SW_MASK = 0x006F
CIA402_SW_FAULT_BIT = 0x0008
CIA402_SW_READY_TO_SWITCH_ON = 0x0021
CIA402_SW_SWITCHED_ON = 0x0023
CIA402_SW_OPERATION_ENABLED = 0x0027

CIA402_MODES_OF_OPERATION_INDEX = 0x6060
CIA402_MODES_OF_OPERATION_SUB_INDEX = 0x00
CIA402_MODES_OF_OPERATION_DISPLAY_INDEX = 0x6061
CIA402_MODES_OF_OPERATION_DISPLAY_SUB_INDEX = 0x00
CIA402_MODE_CST = 10  # Cyclic Synchronous Torque -- required for 0x6071 Target Torque to be used

ENABLE_STEP_TIMEOUT_S = 1.0  # give up on a single state-machine step after this long

# --------- ANALOG INPUT 2 READOUT (PAI-2 CROSS-CHECK) ---------
# PAI-2 (AUX Encoder, pin C4) is configured as Analog Input 2 on the drive.
# Its scaled value (0x201A.02h) is PDO-mappable and appended to the default
# TxPDO at byte offset 14 (after Digital Inputs, which end at byte 13).
# Raw value is 16-bit signed, representing ±10V from the laser sensor.
ANALOG_INPUT_2_TPDO_OFFSET = 14

SINE_FREQ_HZ = 2.0      # current-loop reference applied once the drive is enabled (reduced from 10Hz for better sampling at 100Hz rate: 50 samples/period)
SINE_AMPLITUDE_A = 1.0  # reduced from 2.0A to avoid exceeding velocity/acceleration protection limits at lower cycle rate

# GUI PERFORMANCE TUNING
ENABLE_FFT = True  # Set to False to reduce GIL contention during testing; True for full scope features
MINIMAL_GUI_ON_DRIVE = True  # Disable all plotting when drive is enabled; re-enable on disable for analysis

# --------- PDO MAPPING CONFIGURATION ---------
# Explicit RxPDO (0x1600) and TxPDO (0x1A00) mapping definitions.
# Each entry is (obj_index, obj_subindex, bit_length).
# This ensures the script is self-sufficient and doesn't depend on the drive's stored mapping.
RXPDO_MAPPING = [
    (0x6040, 0x00, 16),   # Control Word
    (0x607A, 0x00, 32),   # Target Position
    (0x60FF, 0x00, 32),   # Target Velocity
    (0x6071, 0x00, 16),   # Target Current
    (0x2001, 0x03, 16),   # User Bits
]

TXPDO_MAPPING = [
    (0x6041, 0x00, 16),   # Status Word
    (0x6064, 0x00, 32),   # Actual Position
    (0x606C, 0x00, 32),   # Actual Velocity
    (0x6077, 0x00, 16),   # Actual Current
    (0x2023, 0x01, 16),   # Digital Inputs
    (0x201A, 0x02, 16),   # Analog Input 2 Value (laser sensor cross-check)
]

# Binary .dat log format: 8-byte magic header + fixed-size records
LOG_MAGIC = b"PDOBIN01"
RECORD_STRUCT = struct.Struct("<dfffii")  # elapsed_s, cycle_ms, current_A, analog_input_2_raw, position_counts, velocity_counts_per_sec
# ---------------------------------------


def _configure_pdo_mapping(slave, mapping_index, entries):
    """Configure RPDO (0x1600) or TPDO (0x1A00) mapping via SDO.
    
    Must be called while the EtherCAT state machine is in Pre-Operational state.
    Writes mapping entries (obj_index, obj_subindex, bit_length) to the specified
    mapping object index.
    """
    # Disable mapping while editing per manual section "PDO Configuration"
    slave.sdo_write(mapping_index, 0x00, struct.pack("<B", 0))
    
    # Write each entry as a packed 32-bit value: (index << 16) | (subindex << 8) | bitlength
    for i, (obj_index, obj_sub, bit_length) in enumerate(entries, start=1):
        if i > 16:
            raise ValueError(f"Cannot map more than 16 entries to mapping index 0x{mapping_index:04X}")
        mapping_value = (obj_index << 16) | (obj_sub << 8) | bit_length
        slave.sdo_write(mapping_index, i, struct.pack("<I", mapping_value))
    
    # Re-enable with final count
    slave.sdo_write(mapping_index, 0x00, struct.pack("<B", len(entries)))


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
    # Print protection limits before enabling
    #
    _print_protection_limits(slave)

    #
    # VOICE COIL MOTOR CONFIGURATION
    # The motor is a linear voice coil with NO velocity/acceleration feedback device.
    # The drive is configured for Cyclic Synchronous Torque (CST) mode with current-loop-only control.
    # Disable all feedback sensor error checking to prevent false Feedback Sensor Error on startup.
    # The PAI-2 laser sensor will not be used by the drive for control (remains mapped in TxPDO for diagnostics only).
    #
    _configure_feedback_disabled(slave)

    #
    # Configure PDO mappings explicitly to ensure Analog Input 2 is included.
    # Must be done while slave is in Pre-Operational state (guaranteed after config_init).
    #
    _configure_pdo_mapping(slave, 0x1600, RXPDO_MAPPING)
    _configure_pdo_mapping(slave, 0x1A00, TXPDO_MAPPING)
    print(f"Configured RxPDO ({len(RXPDO_MAPPING)} entries) and TxPDO ({len(TXPDO_MAPPING)} entries)")

    #
    # Apply PDO mapping to the master
    #
    master.config_map()

    #
    # Verify active TxPDO mapping (must now match TXPDO_MAPPING after explicit configuration).
    #
    tpdo_count = struct.unpack("<B", slave.sdo_read(0x1A00, 0x00))[0]
    mapped_entries = [
        struct.unpack("<I", slave.sdo_read(0x1A00, sub))[0]
        for sub in range(1, tpdo_count + 1)
    ]
    
    # Verify Analog Input 2 (0x201A:02) is mapped
    expected_ai2_mapping = (0x201A << 16) | (0x02 << 8) | 16
    if tpdo_count != len(TXPDO_MAPPING) or expected_ai2_mapping not in mapped_entries:
        raise RuntimeError(
            f"TxPDO mapping verification failed: expected {len(TXPDO_MAPPING)} entries "
            f"with AI2 (0x{expected_ai2_mapping:08X}), got {tpdo_count} entries: "
            + ", ".join(f"0x{e:08X}" for e in mapped_entries)
        )
    
    print(f"Active TxPDO mapping ({tpdo_count} entries): "
          + ", ".join(f"0x{e:08X}" for e in mapped_entries))

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


def _write_output(slave, controlword, target_current_raw=0):
    # AMC default RxPDO layout (assumed, mirrors the TxPDO read layout):
    # Controlword at offset 0, target current at offset 10.
    # slave.output returns an immutable bytes copy -- rebuild and reassign it.
    buf = bytearray(slave.output)
    struct.pack_into("<H", buf, 0, controlword)
    struct.pack_into("<h", buf, 10, target_current_raw)
    slave.output = bytes(buf)


def _amps_to_raw_current(amps, k_p_amps):
    raw = int(round(amps * 32768.0 / k_p_amps))  # DC2 = 2^15 / K_P
    return max(-32768, min(32767, raw))

def _read_fault_info(slave):
    """Best-effort read of the standard CoE error register/history (0x1001 /
    0x1003) -- not every object is guaranteed to exist on a given slave."""
    parts = []
    try:
        error_register = struct.unpack("<B", slave.sdo_read(0x1001, 0x00))[0]
        parts.append(f"0x1001 Error Register=0x{error_register:02X}")
    except Exception as exc:
        parts.append(f"0x1001 read failed ({exc})")

    try:
        num_errors = struct.unpack("<B", slave.sdo_read(0x1003, 0x00))[0]
        if num_errors:
            last_error = struct.unpack("<I", slave.sdo_read(0x1003, 0x01))[0]
            parts.append(f"0x1003 Last Error=0x{last_error:08X}")
    except Exception as exc:
        parts.append(f"0x1003 read failed ({exc})")

    return ", ".join(parts) if parts else "no fault info available"


def _read_extended_fault_info(slave):
    """Read and decode 0x1001 (Error Register) and 0x2002h (Drive/System Status) bits."""
    parts = []
    
    # Error Register 0x1001:0x00 — bit meanings per CANopen standard
    try:
        error_reg = struct.unpack("<B", slave.sdo_read(0x1001, 0x00))[0]
        error_bits = []
        if error_reg & 0x01:
            error_bits.append("Generic Error")
        if error_reg & 0x02:
            error_bits.append("Over-Current")
        if error_reg & 0x04:
            error_bits.append("Over-Voltage")
        if error_reg & 0x08:
            error_bits.append("Thermal")
        if error_reg & 0x10:
            error_bits.append("Device-Specific-1")
        if error_reg & 0x20:
            error_bits.append("Device-Specific-2")
        if error_reg & 0x40:
            error_bits.append("Communication")
        if error_reg & 0x80:
            error_bits.append("Protocol")
        parts.append(f"0x1001={error_bits if error_bits else ['None']}")
    except Exception as exc:
        parts.append(f"0x1001 read failed: {exc}")
    
    # Drive/System Status 0x2002h — read all 7 sub-indices
    for sub in range(1, 8):
        try:
            status_val = struct.unpack("<H", slave.sdo_read(0x2002, sub))[0]
            if status_val:
                parts.append(f"0x2002.{sub:02X}=0x{status_val:04X}")
        except Exception:
            pass  # Sub-index may not exist
    
    return " | ".join(parts) if parts else "no extended diagnostics available"


def _check_and_log_fault_during_operation(master, slave, log_prefix=""):
    """Check if fault bit is set in TxPDO status word; if so, read extended diagnostics."""
    try:
        status_word = struct.unpack_from("<H", slave.input, 0)[0]
        if status_word & CIA402_SW_FAULT_BIT:
            extended_info = _read_extended_fault_info(slave)
            print(f"[FAULT DETECTED] {log_prefix} SW=0x{status_word:04X} | {extended_info}")
            return extended_info
    except Exception as exc:
        print(f"[ERROR checking fault] {exc}")
    return None


def _print_protection_limits(slave):
    """Read and print drive protection limits at startup.
    
    Reads velocity and position limit objects (0x2037h, 0x2039h) and prints
    them in a formatted block with both raw and converted values.
    Each field is wrapped in try/except so one read failure doesn't block others.
    """
    print()
    print("--- Drive Protection Limits (read at startup) ---")
    
    # Read KS (switching frequency) for velocity conversion
    ks_hz = None
    try:
        ks_data = slave.sdo_read(0x20D8, 0x24)
        # Handle both Unsigned16 (2 bytes) and Unsigned32 (4 bytes) formats
        if len(ks_data) == 4:
            ks_raw = struct.unpack("<I", ks_data)[0]
        elif len(ks_data) == 2:
            ks_raw = struct.unpack("<H", ks_data)[0]
        else:
            raise ValueError(f"Unexpected KS data length: {len(ks_data)} bytes (expected 2 or 4)")
        ks_hz = ks_raw / 65536.0
    except Exception as exc:
        print(f"  WARNING: KS read failed ({exc}) — velocity limits unavailable")
    
    # Motor Over Speed Limit (0x2037.01h)
    try:
        motor_overspeed = struct.unpack("<i", slave.sdo_read(0x2037, 0x01))[0]
        if ks_hz is not None:
            converted = motor_overspeed * ks_hz / 131072.0  # DS1 to counts/s
            print(f"  Motor Over Speed Limit:      {converted:+11.1f} counts/s   (raw DS1=0x{motor_overspeed:08X})")
        else:
            print(f"  Motor Over Speed Limit:      0x{motor_overspeed:08X} (raw DS1 — KS unavailable for conversion)")
    except Exception as exc:
        print(f"  Motor Over Speed Limit:      read failed ({exc})")
    
    # Positive Velocity Limit (0x2037.05h)
    try:
        pos_vel_limit = struct.unpack("<i", slave.sdo_read(0x2037, 0x05))[0]
        if ks_hz is not None:
            converted = pos_vel_limit * ks_hz / 131072.0
            print(f"  Positive Velocity Limit:     {converted:+11.1f} counts/s   (raw DS1=0x{pos_vel_limit:08X})")
        else:
            print(f"  Positive Velocity Limit:     0x{pos_vel_limit:08X} (raw DS1 — KS unavailable for conversion)")
    except Exception as exc:
        print(f"  Positive Velocity Limit:     read failed ({exc})")
    
    # Negative Velocity Limit (0x2037.06h)
    try:
        neg_vel_limit = struct.unpack("<i", slave.sdo_read(0x2037, 0x06))[0]
        if ks_hz is not None:
            converted = neg_vel_limit * ks_hz / 131072.0
            print(f"  Negative Velocity Limit:     {converted:+11.1f} counts/s   (raw DS1=0x{neg_vel_limit:08X})")
        else:
            print(f"  Negative Velocity Limit:     0x{neg_vel_limit:08X} (raw DS1 — KS unavailable for conversion)")
    except Exception as exc:
        print(f"  Negative Velocity Limit:     read failed ({exc})")
    
    if ks_hz is not None:
        print(f"  (velocity conversion assumes KI=1; only valid if 1Vp-p Sin/Cos feedback is not in use)")
    
    # Position Limits Control (0x2039.0Ah) — already in counts
    try:
        pos_limits_control = struct.unpack("<H", slave.sdo_read(0x2039, 0x0A))[0]
        if pos_limits_control == 3:
            pos_control_str = "ENABLED"
        elif pos_limits_control == 0:
            pos_control_str = "DISABLED"
        else:
            pos_control_str = f"UNKNOWN (0x{pos_limits_control:04X})"
        print(f"  Position Limits Control:     {pos_control_str}")
    except Exception as exc:
        print(f"  Position Limits Control:     read failed ({exc})")
    
    # Max Measured Position Limit (0x2039.03h) — in counts, no conversion
    try:
        max_pos = struct.unpack("<i", slave.sdo_read(0x2039, 0x03))[0]
        print(f"    Max Measured Position:       {max_pos:+12d} counts")
    except Exception as exc:
        print(f"    Max Measured Position:       read failed ({exc})")
    
    # Min Measured Position Limit (0x2039.04h) — in counts, no conversion
    try:
        min_pos = struct.unpack("<i", slave.sdo_read(0x2039, 0x04))[0]
        print(f"    Min Measured Position:       {min_pos:+12d} counts")
    except Exception as exc:
        print(f"    Min Measured Position:       read failed ({exc})")
    
    # Feedback Sensor Configuration
    print()
    print("--- Feedback Sensor Configuration ---")
    try:
        encoder_type = struct.unpack("<H", slave.sdo_read(0x2032, 0x07))[0]
        encoder_str = "Not Assigned (disabled)" if encoder_type == 0 else f"Encoder Type: 0x{encoder_type:04X}"
        print(f"  Serial Encoder Type (0x2032.07):  {encoder_str}")
    except Exception as exc:
        print(f"  Serial Encoder Type (0x2032.07):  read failed ({exc})")
    
    try:
        error_window = struct.unpack("<H", slave.sdo_read(0x2032, 0x0D))[0]
        # Convert from physical units (SF1 scaling): raw value / 0x4000 = physical value (0 to 1)
        phys_window = error_window / 0x4000 if error_window > 0 else 0.0
        print(f"  Sin/Cos Error Window (0x2032.0D): 0x{error_window:04X} (phys ≈ {phys_window:.3f})")
    except Exception as exc:
        print(f"  Sin/Cos Error Window (0x2032.0D): read failed ({exc})")
    
    try:
        error_action = struct.unpack("<H", slave.sdo_read(0x2065, 0x06))[0]
        action_str = "No Action (disabled)" if error_action == 0 else f"Action: 0x{error_action:04X}"
        print(f"  Feedback Sensor Error Action (0x2065.06): {action_str}")
    except Exception as exc:
        print(f"  Feedback Sensor Error Action (0x2065.06): read failed ({exc})")
    
    print("---------------------------------------------------")
    print()


def _configure_feedback_disabled(slave):
    """Disable ALL encoder feedback monitoring for current-loop-only voice coil operation.
    
    Attempts to disable encoder-related SDO objects. Some may be read-only or protected;
    failures are logged but do not stop operation if at least the critical flags are disabled.
    """
    failed_writes = []
    successful_writes = []
    
    # Primary writes: must succeed or we'll likely fault on enable
    critical_writes = [
        (0x2032, 0x01, "<H", 0x0000, "Encoder Present"),
        (0x2032, 0x06, "<H", 0x0000, "Encoder Enable"),
        (0x2032, 0x07, "<H", 0x0000, "Serial Encoder Type"),
        (0x2032, 0x08, "<H", 0x0000, "Encoder Monitoring Mode"),
        (0x2032, 0x09, "<H", 0x0000, "Encoder Health Check"),
        (0x2032, 0x0C, "<H", 0x0000, "Back-EMF Feedback"),
        (0x2032, 0x0D, "<H", 0x4000, "Sin/Cos Error Window (max tolerance)"),
        (0x2065, 0x06, "<H", 0x0000, "Feedback Sensor Error Action"),
        (0x2036, 0x01, "<H", 0x0000, "Commutation Type"),
        (0x2036, 0x02, "<I", 0x00000000, "Commutation Polarity"),
        (0x2032, 0x05, "<H", 0x0000, "Encoder Offset"),
    ]
    
    # Optional writes: some AMC firmware versions protect these (read-only)
    # Skip if they fail — they're less critical for CST operation
    optional_writes = [
        (0x2036, 0x03, "<H", 0x0000, "Commutation Timing (read-only on some firmware)"),
        (0x2032, 0x03, "<H", 0x0000, "Sin/Cos Encoder Phase (read-only on some firmware)"),
        (0x2032, 0x04, "<H", 0x0000, "Commutation Encoder Config (read-only on some firmware)"),
    ]
    
    for obj, sub, fmt, value, desc in critical_writes:
        try:
            data = struct.pack(fmt, value)
            slave.sdo_write(obj, sub, data)
            successful_writes.append(f"  ✓ 0x{obj:04X}.{sub:02X} ({desc}) = 0x{value:X}")
        except Exception as exc:
            failed_writes.append(f"  ✗ 0x{obj:04X}.{sub:02X} ({desc}): {exc}")
    
    optional_failed = []
    for obj, sub, fmt, value, desc in optional_writes:
        try:
            data = struct.pack(fmt, value)
            slave.sdo_write(obj, sub, data)
            successful_writes.append(f"  ✓ 0x{obj:04X}.{sub:02X} ({desc}) = 0x{value:X}")
        except Exception as exc:
            optional_failed.append(f"  ⚠ 0x{obj:04X}.{sub:02X} ({desc}): SKIPPED (read-only)")
    
    # Print summary
    print("\n--- Feedback/Commutation Configuration ---")
    if successful_writes:
        print("Successful writes:")
        for msg in successful_writes:
            print(msg)
    
    if failed_writes:
        print("CRITICAL FAILED writes (blocking):")
        for msg in failed_writes:
            print(msg)
        raise RuntimeError(f"Critical encoder configuration writes failed—cannot proceed")
    
    if optional_failed:
        print("Optional writes skipped (read-only/protected on this firmware):")
        for msg in optional_failed:
            print(msg)
    
    print("--------------------------------------\n")

def _scan_motor_configuration(slave):
    """Scan 0x2032h, 0x2034h, 0x2036h objects for motor/encoder monitoring."""
    print("\n[MOTOR CONFIGURATION SCAN]")
    
    for obj in [0x2032, 0x2034, 0x2036]:
        try:
            obj_name = {0x2032: "Encoder Parameters", 0x2034: "Motor Parameters", 0x2036: "Commutation"}[obj]
            print(f"\n  0x{obj:04X} ({obj_name}):")
            
            for sub in range(0x01, 0x30):
                try:
                    data = slave.sdo_read(obj, sub)
                    if len(data) == 2:
                        value = struct.unpack("<H", data)[0]
                    elif len(data) == 4:
                        value = struct.unpack("<I", data)[0]
                    else:
                        continue
                    
                    if value != 0:
                        print(f"    {sub:02X}: 0x{value:08X}")
                except Exception:
                    pass
        except Exception as exc:
            print(f"  Scan error: {exc}")
    print()

def _verify_feedback_config_persistence(slave):
    """Verify that all encoder/feedback configuration SDO writes persisted after enable.
    Only checks parameters that are actually writable on the drive."""
    try:
        print("\n[CONFIG VERIFICATION - IMMEDIATELY AFTER DISABLE]")
        
        checks = [
            (0x2032, 0x01, "<H", 0x0000, "Encoder Present"),
            (0x2032, 0x06, "<H", 0x0000, "Encoder Enable"),
            (0x2032, 0x07, "<H", 0x0000, "Encoder Type"),
            (0x2032, 0x08, "<H", 0x0000, "Encoder Monitoring"),
            (0x2032, 0x09, "<H", 0x0000, "Encoder Health"),
            (0x2032, 0x0C, "<H", 0x0000, "Back-EMF Feedback"),
            (0x2032, 0x0D, "<H", 0x4000, "Error Window"),
            (0x2065, 0x06, "<H", 0x0000, "Feedback Error Action"),
            (0x2036, 0x01, "<H", 0x0000, "Commutation Type"),
            (0x2036, 0x02, "<I", 0x00000000, "Commutation Polarity"),
            (0x2032, 0x05, "<H", 0x0000, "Encoder Offset"),
        ]
        
        for obj, sub, fmt, expected, desc in checks:
            try:
                raw = slave.sdo_read(obj, sub)
                if fmt == "<I":
                    actual = struct.unpack(fmt, raw)[0]
                else:
                    actual = struct.unpack(fmt, raw)[0]
                status = "✓" if actual == expected else "✗"
                print(f"  {status} 0x{obj:04X}.{sub:02X} ({desc}): 0x{actual:X} (expect 0x{expected:X})")
                if actual != expected:
                    raise RuntimeError(f"Value mismatch: expected 0x{expected:X}, got 0x{actual:X}")
            except Exception as exc:
                print(f"  ✗ 0x{obj:04X}.{sub:02X} ({desc}): read failed ({exc})")
                raise

        print("  ✓ All writable encoder/feedback parameters verified\n")
    except Exception as exc:
        raise RuntimeError(f"Configuration persistence verification failed: {exc}")

# Event Action mapping for 0x2065:21 (Event Action: Communication Error)
EVENT_ACTIONS = {
    0x00: "No action",
    0x01: "Disable power bridge",
    0x02: "Disable positive direction",
    0x03: "Disable negative direction",
    0x04: "Dynamic Brake",
    0x05: "Positive stop",
    0x06: "Negative stop",
    0x07: "Stop",
    0x08: "Apply Brake then disable bridge",
    0x09: "Apply Brake then dynamic brake",
    0x0A: "Apply Brake and Disable bridge",
    0x0B: "Apply Brake and Dynamic Brake"
}


def _decode_modes_of_operation(mode):
    """Decode the Modes Of Operation Display value (0x6061:00)."""
    modes = {
        0: "No mode / Error",
        1: "Profile Position",
        3: "Profile Velocity",
        4: "Profile Torque",
        6: "Homing",
        7: "Interpolated Position",
        8: "Cyclic Synchronous Position",
        9: "Cyclic Synchronous Velocity",
        10: "Cyclic Synchronous Torque (CST)",
        -1: "Not assigned",
    }
    return modes.get(mode, f"Unknown (0x{mode:02X})")


def read_critical_diagnostics(slave):
    """Read critical diagnostic SDO objects to identify fault root cause.
    
    Returns a dictionary with the following keys:
    - 'modes_of_operation': Current mode (0x6061:00)
    - 'feedback_error_counter': Cumulative feedback sensor errors (0x2028:0F)
    - 'communication_error_counter': Cumulative communication errors (0x2028:2F)
    - 'communication_error_event_action': Event action on comm error (0x2065:21)
    - 'raw': Raw dict with uninterpreted values
    
    Each field is wrapped in try/except so one read failure doesn't block others.
    """
    diag = {
        'modes_of_operation': None,
        'feedback_error_counter': None,
        'communication_error_counter': None,
        'communication_error_event_action': None,
        'raw': {}
    }
    
    # 0x6061:00 — Modes Of Operation Display
    try:
        mode_raw = struct.unpack("<b", slave.sdo_read(0x6061, 0x00))[0]
        diag['modes_of_operation'] = _decode_modes_of_operation(mode_raw)
        diag['raw']['modes_of_operation'] = mode_raw
    except Exception as exc:
        diag['modes_of_operation'] = f"read failed: {exc}"
        diag['raw']['modes_of_operation'] = None
    
    # 0x2028:0F — Feedback Sensor Error Counter
    try:
        fb_counter = struct.unpack("<H", slave.sdo_read(0x2028, 0x0F))[0]
        diag['feedback_error_counter'] = fb_counter
        diag['raw']['feedback_error_counter'] = fb_counter
    except Exception as exc:
        diag['feedback_error_counter'] = f"read failed: {exc}"
        diag['raw']['feedback_error_counter'] = None
    
    # 0x2028:2F — Communication Error Counter
    try:
        comm_counter = struct.unpack("<H", slave.sdo_read(0x2028, 0x2F))[0]
        diag['communication_error_counter'] = comm_counter
        diag['raw']['communication_error_counter'] = comm_counter
    except Exception as exc:
        diag['communication_error_counter'] = f"read failed: {exc}"
        diag['raw']['communication_error_counter'] = None
    
    # 0x2065:21 — Event Action: Communication Error
    try:
        event_action_raw = struct.unpack("<H", slave.sdo_read(0x2065, 0x21))[0]
        action_bits = []
        for bit_val, bit_name in EVENT_ACTIONS.items():
            if event_action_raw & bit_val:
                action_bits.append(bit_name)
        event_action_str = " | ".join(action_bits) if action_bits else "No action (0x0000)"
        diag['communication_error_event_action'] = event_action_str
        diag['raw']['communication_error_event_action'] = event_action_raw
    except Exception as exc:
        diag['communication_error_event_action'] = f"read failed: {exc}"
        diag['raw']['communication_error_event_action'] = None
    
    return diag


def _print_critical_diagnostics(label, diag):
    """Print critical diagnostics in a formatted block."""
    print(f"\n--- Critical Diagnostics ({label}) ---")
    print(f"  Modes Of Operation Display (0x6061:00): {diag['modes_of_operation']}")
    print(f"  Feedback Sensor Error Counter (0x2028:0F): {diag['feedback_error_counter']}")
    print(f"  Communication Error Counter (0x2028:2F): {diag['communication_error_counter']}")
    raw_event_action = diag['raw'].get('communication_error_event_action')
    if raw_event_action is not None:
        print(f"  Event Action: Comm Error (0x2065:21): 0x{raw_event_action:04X}")
    print(f"    → {diag['communication_error_event_action']}")
    print("-------------------------------------------\n")


def _print_diagnostic_deltas(baseline, fault):
    """Compare and print counter deltas between baseline and fault diagnostics."""
    print("\n--- Diagnostic Counter Changes (baseline → fault) ---")
    
    fb_baseline = baseline['raw'].get('feedback_error_counter')
    fb_fault = fault['raw'].get('feedback_error_counter')
    if fb_baseline is not None and fb_fault is not None and isinstance(fb_baseline, int) and isinstance(fb_fault, int):
        delta_fb = fb_fault - fb_baseline
        print(f"  Feedback Sensor Errors:  {fb_baseline} → {fb_fault}  (Δ = {delta_fb:+d})")
    else:
        print(f"  Feedback Sensor Errors:  (unavailable for delta calculation)")
    
    comm_baseline = baseline['raw'].get('communication_error_counter')
    comm_fault = fault['raw'].get('communication_error_counter')
    if comm_baseline is not None and comm_fault is not None and isinstance(comm_baseline, int) and isinstance(comm_fault, int):
        delta_comm = comm_fault - comm_baseline
        print(f"  Communication Errors:    {comm_baseline} → {comm_fault}  (Δ = {delta_comm:+d})")
        if delta_comm > 0:
            print(f"    ⚠ Communication error(s) detected — likely EtherCAT watchdog timeout or frame loss")
    else:
        print(f"  Communication Errors:    (unavailable for delta calculation)")
    
    print("--------------------------------------------------\n")


def _exchange_and_read_statusword(master, slave):
    master.send_processdata()
    wkc = master.receive_processdata(15000)  # 15ms timeout for 10ms cycle + margin
    status_word = struct.unpack_from("<H", slave.input, 0)[0]
    return status_word, wkc


def run_enable_sequence(master, slave):
    """Fault-reset (if needed) and step the CiA402 state machine up to
    Operation Enabled via RxPDO Controlword writes. Raises RuntimeError if
    any step doesn't complete within ENABLE_STEP_TIMEOUT_S.
    """

    def wait_for_masked_state(target_masked, controlword):
        _write_output(slave, controlword)
        deadline = time.perf_counter() + ENABLE_STEP_TIMEOUT_S
        status_word, wkc = 0, 0
        while time.perf_counter() < deadline:
            status_word, wkc = _exchange_and_read_statusword(master, slave)
            if (status_word & CIA402_SW_MASK) == target_masked:
                return status_word
            time.sleep(CYCLE_TIME_S)
        raise RuntimeError(
            f"Drive did not reach statusword 0x{target_masked:02X} after "
            f"writing controlword 0x{controlword:04X} (last SW=0x{status_word:04X}, "
            f"WKC={wkc}/{master.expected_wkc})"
        )

    status_word, wkc = _exchange_and_read_statusword(master, slave)

    if status_word & CIA402_SW_FAULT_BIT:
        error_info = _read_fault_info(slave)
        print(
            f"Drive is faulted (SW=0x{status_word:04X}, WKC={wkc}/{master.expected_wkc}, "
            f"{error_info}); attempting reset..."
        )

        _write_output(slave, CIA402_CW_FAULT_RESET)
        deadline = time.perf_counter() + ENABLE_STEP_TIMEOUT_S
        while status_word & CIA402_SW_FAULT_BIT:
            if time.perf_counter() >= deadline:
                raise RuntimeError(
                    f"Fault reset failed (last SW=0x{status_word:04X}, "
                    f"WKC={wkc}/{master.expected_wkc}, {error_info})"
                )
            status_word, wkc = _exchange_and_read_statusword(master, slave)
            time.sleep(CYCLE_TIME_S)
        _write_output(slave, CIA402_CW_DISABLE_VOLTAGE)
        _exchange_and_read_statusword(master, slave)

    wait_for_masked_state(CIA402_SW_READY_TO_SWITCH_ON, CIA402_CW_SHUTDOWN)
    wait_for_masked_state(CIA402_SW_SWITCHED_ON, CIA402_CW_SWITCH_ON)

    # Current Torque (0x6071) will be used by the drive in Cyclic Synchronous
    # Torque mode -- switch to it via SDO before enabling operation.
    slave.sdo_write(CIA402_MODES_OF_OPERATION_INDEX, CIA402_MODES_OF_OPERATION_SUB_INDEX, struct.pack("<b", CIA402_MODE_CST))
    actual_mode = struct.unpack("<b", slave.sdo_read(CIA402_MODES_OF_OPERATION_DISPLAY_INDEX, CIA402_MODES_OF_OPERATION_DISPLAY_SUB_INDEX))[0]
    if actual_mode != CIA402_MODE_CST:
        raise RuntimeError(
            f"Drive rejected Cyclic Synchronous Torque mode (0x6061 reads {actual_mode})"
        )

    status_word = wait_for_masked_state(CIA402_SW_OPERATION_ENABLED, CIA402_CW_ENABLE_OPERATION)

    return status_word


def disable_drive(master, slave):
    """Best-effort Shutdown command to bring the drive out of Operation
    Enabled (e.g. before closing the master)."""
    _write_output(slave, CIA402_CW_SHUTDOWN)
    status_word, _wkc = _exchange_and_read_statusword(master, slave)
    return status_word


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
    drive_enabled = False
    sine_start_time = None   # perf_counter() timestamp when the drive was enabled
    baseline_diagnostics = None  # Captured immediately after enable for comparison on fault
    fault_detected_info = None  # Stores (elapsed_time, status_word, max_cycle_ms, max_cycle_elapsed) when fault detected; read on disable

    def handle_command(command):
        nonlocal log_state, log_file, log_path, log_byte_buffer, drive_enabled, sine_start_time, baseline_diagnostics, fault_detected_info

        action = command[0]

        if action == "enable":
            try:
                status_word = run_enable_sequence(master, slave)
                drive_enabled = True
                sine_start_time = time.perf_counter()
                # Capture baseline diagnostics immediately after successful enable
                baseline_diagnostics = read_critical_diagnostics(slave)
                _print_critical_diagnostics("after enable (baseline)", baseline_diagnostics)
                status_queue.put(("drive_enabled", status_word))
            except RuntimeError as exc:
                print(f"Drive enable failed: {exc}")
                status_queue.put(("drive_enable_error", str(exc)))
            return

        elif action == "disable":
            status_word = disable_drive(master, slave)
            drive_enabled = False
            sine_start_time = None
            
            # Verify feedback configuration persisted through operation (deferred SDO read — safe after disable)
            try:
                _verify_feedback_config_persistence(slave)
            except Exception as exc:
                print(f"[CONFIG VERIFICATION ERROR] {exc}")

            try:
                _scan_motor_configuration(slave)
            except Exception as exc:
                print(f"[MOTOR CONFIGURATION SCAN ERROR] {exc}")

            # If a fault was detected, read diagnostics now (deferred from operation)
            if fault_detected_info is not None:
                elapsed_time, fault_sw, fault_cycle_ms, fault_cycle_elapsed = fault_detected_info
                try:
                    extended_fault_info = _read_extended_fault_info(slave)
                    critical_fault_diag = read_critical_diagnostics(slave)
                    _print_critical_diagnostics("post-operation (fault diagnostics)", critical_fault_diag)
                    if baseline_diagnostics is not None:
                        _print_diagnostic_deltas(baseline_diagnostics, critical_fault_diag)
                    print(f"[FAULT INFO] t={elapsed_time:.3f}s SW=0x{fault_sw:04X} | {extended_fault_info}")
                    print(f"  Max cycle time: {fault_cycle_ms:.3f}ms at t={fault_cycle_elapsed:.3f}s")
                    status_queue.put(("drive_fault_secondary", extended_fault_info))
                except Exception as exc:
                    print(f"[ERROR reading fault diagnostics] {exc}")
                fault_detected_info = None
            else:
                baseline_diagnostics = None  # Clear baseline on normal disable
            
            status_queue.put(("drive_disabled", status_word))
            return

        elif action == "start":
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

    # Sliding window deque: stores (elapsed_seconds, actual_cycle_ms) tuples
    # for the last FAULT_WINDOW_S seconds to capture recent cycle performance
    cycle_time_window = deque(maxlen=int(CYCLE_TIME_S * 100) + 1)  # max ~200 entries for 2s @ 100Hz

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
        elapsed = now - start_time
        
        # Append cycle to sliding window (old entries auto-drop when maxlen reached)
        cycle_time_window.append((elapsed, actual_cycle_ms))

        #
        # Drive the current-loop sine wave reference while enabled
        #
        if drive_enabled and sine_start_time is not None:
            target_amps = SINE_AMPLITUDE_A * np.sin(2 * np.pi * SINE_FREQ_HZ * (now - sine_start_time))
            target_raw = _amps_to_raw_current(target_amps, k_p_amps)
            _write_output(slave, CIA402_CW_ENABLE_OPERATION, target_raw)

        #
        # PDO exchange
        #
        master.send_processdata()
        wkc = master.receive_processdata(15000)  # 15ms timeout for 10ms cycle + margin

        pdo = slave.input

        #
        # AMC default TPDO layout
        #
        status_word = struct.unpack_from("<H", pdo, 0)[0]
        position = struct.unpack_from("<i", pdo, 2)[0]
        velocity = struct.unpack_from("<i", pdo, 6)[0]
        raw_current = struct.unpack_from("<h", pdo, 10)[0]
        # Analog Input 2 (PAI-2 laser sensor) appended at byte offset 14
        # (after Digital Inputs which end at byte 13 per Table B.2)
        analog_input_2_raw = struct.unpack_from("<h", pdo, ANALOG_INPUT_2_TPDO_OFFSET)[0]

        current_amps = raw_current * k_p_amps / 8192.0
        
        #
        # Monitor for secondary faults during operation — PDO-only check, no blocking SDO reads
        # Diagnostics are read later in disable handler to avoid blocking the acquisition loop
        #
        if drive_enabled and (sample_count % 1 == 0):
            try:
                if status_word & CIA402_SW_FAULT_BIT:
                    # Find worst cycle within the last FAULT_WINDOW_S seconds
                    cutoff_time = elapsed - FAULT_WINDOW_S
                    recent_cycles = [cyc for et, cyc in cycle_time_window if et >= cutoff_time]
                    recent_max_ms = max(recent_cycles) if recent_cycles else actual_cycle_ms
                    
                    # Find elapsed time when that worst cycle occurred
                    recent_max_time = None
                    for et, cyc in cycle_time_window:
                        if cyc == recent_max_ms and et >= cutoff_time:
                            recent_max_time = et
                            break
                    
                    print(f"[FAULT DETECTED] t={elapsed:.3f}s SW=0x{status_word:04X}")
                    print(f"  Max cycle (last {FAULT_WINDOW_S}s): {recent_max_ms:.3f}ms at t={recent_max_time:.3f}s")
                    
                    # Store fault info for diagnostics read in disable handler
                    fault_detected_info = (elapsed, status_word, recent_max_ms, recent_max_time)
                    drive_enabled = False
            except Exception as exc:
                print(f"[ERROR checking fault] {exc}")

        with buffer_lock:
            buffer.append((elapsed, position, current_amps, analog_input_2_raw, velocity))

        #
        # Binary log write (only while logging is running)
        #
        if log_state == "RUNNING":
            log_byte_buffer += RECORD_STRUCT.pack(
                elapsed, actual_cycle_ms, current_amps, analog_input_2_raw, position, velocity
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
                f"AI2={analog_input_2_raw:+6d}  "
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

    # Best-effort: don't leave the drive Operation Enabled after the script exits.
    if drive_enabled:
        try:
            disable_drive(master, slave)
        except OSError:
            pass


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
                "analog_input_2_raw",
                "position_counts",
                "velocity_counts_per_sec"
            ])

            while True:
                chunk = src.read(RECORD_STRUCT.size)

                if not chunk:
                    break

                if len(chunk) != RECORD_STRUCT.size:
                    raise ValueError(f"'{dat_path}' contains a truncated record")

                elapsed, cycle_ms, current_amps, analog_input_2_raw, position, velocity = RECORD_STRUCT.unpack(chunk)

                writer.writerow([
                    f"{elapsed:.6f}",
                    f"{cycle_ms:.3f}",
                    f"{current_amps:.5f}",
                    analog_input_2_raw,
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

        if action == "enable":
            status_queue.put(("drive_enabled", CIA402_SW_OPERATION_ENABLED))
            return

        elif action == "disable":
            status_queue.put(("drive_disabled", 0x0000))
            return

        elif action == "start":
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
        # Simulate analog input 2 as a scaled, noisy version of position for testing
        analog_input_2_raw = int(position * 0.1 + SIM_NOISE_AMP * 100 * (2.0 * np.random.random() - 1.0))

        with buffer_lock:
            buffer.append((elapsed, position, current_amps, analog_input_2_raw, velocity))

        if log_state == "RUNNING":
            log_byte_buffer += RECORD_STRUCT.pack(
                elapsed, actual_cycle_ms, current_amps, analog_input_2_raw, position, velocity
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
    """Tkinter window with a 3x2 graph grid: scrolling position/current/velocity
    traces on the left (3 rows) sharing an adjustable time-axis window length,
    and their live FFTs (position and current) on the right (2 rows) sharing an
    adjustable max-frequency axis, plus binary (.dat) logging controls
    (start/pause/resume/stop, filename entry, convert to CSV).
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
        self.plotting_enabled = True  # Plots visible by default; disabled when drive is enabled
        self.drive_active = False     # Track if drive is currently enabled

        self.window_seconds = tk.DoubleVar(value=WINDOW_DEFAULT_S)
        self.fft_max_freq = tk.IntVar(value=FFT_FREQ_DEFAULT)
        self.filename_var = tk.StringVar(value=LOG_FILE)
        self.status_var = tk.StringVar(value="Not logging.")
        self.drive_status_var = tk.StringVar(value="Drive: unknown")

        root.title(
            "EtherCAT Drive Scope - Position & Current  [SIMULATION]"
            if sim_warning else
            "EtherCAT Drive Scope - Position & Current"
        )
        root.protocol("WM_DELETE_WINDOW", self.on_close)

        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = Figure(figsize=(11, 6), dpi=100)
        self.ax_position = self.figure.add_subplot(3, 2, 1)
        self.ax_current = self.figure.add_subplot(3, 2, 3, sharex=self.ax_position)
        self.ax_velocity = self.figure.add_subplot(3, 2, 5, sharex=self.ax_position)
        self.ax_fft_position = self.figure.add_subplot(3, 2, 2)
        self.ax_fft_current = self.figure.add_subplot(3, 2, 4, sharex=self.ax_fft_position)

        self.ax_position.set_ylabel("Position (counts)")
        self.ax_position.set_title("Position")
        self.ax_position.tick_params(labelbottom=False)

        self.ax_current.set_ylabel("Current (A)")
        self.ax_current.set_title("Current")
        self.ax_current.tick_params(labelbottom=False)

        self.ax_velocity.set_ylabel("Velocity (counts/s)")
        self.ax_velocity.set_xlabel("Time (s)")
        self.ax_velocity.set_title("Velocity")

        self.ax_fft_position.set_ylabel("Magnitude")
        self.ax_fft_position.set_title("Position FFT")
        self.ax_fft_position.tick_params(labelbottom=False)

        self.ax_fft_current.set_ylabel("Magnitude")
        self.ax_fft_current.set_xlabel("Frequency (Hz)")
        self.ax_fft_current.set_title("Current FFT")

        self.line_position, = self.ax_position.plot([], [], color="tab:blue")
        self.line_current, = self.ax_current.plot([], [], color="tab:orange")
        self.line_velocity, = self.ax_velocity.plot([], [], color="tab:purple")
        self.line_fft_position, = self.ax_fft_position.plot([], [], color="tab:green")
        self.line_fft_current, = self.ax_fft_current.plot([], [], color="tab:red")

        self.figure.tight_layout()

        # Blitting: mark every data line as "animated" so it is excluded from
        # the background snapshot. The background (axes frames, tick labels,
        # grid) is only re-rendered every FULL_REDRAW_EVERY frames; all other
        # frames restore the cached background and blit only the lines —
        # typically 10-20× faster than a full draw.
        for _line in (self.line_position, self.line_current, self.line_velocity,
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

        # Time-axis window slider (horizontal, right = max window)
        ttk.Label(controls_panel, text="Time window (s)").pack(anchor="w")
        self.slider = tk.Scale(
            controls_panel,
            from_=WINDOW_MIN_S,
            to=WINDOW_MAX_S,
            resolution=WINDOW_STEP_S,
            orient=tk.HORIZONTAL,
            variable=self.window_seconds,
        )
        self.slider.pack(fill=tk.X, expand=True)

        ttk.Separator(controls_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        # FFT max-frequency slider (horizontal, right = max frequency)
        ttk.Label(controls_panel, text="Max Freq (Hz)").pack(anchor="w")
        self.fft_freq_slider = tk.Scale(
            controls_panel,
            from_=FFT_FREQ_MIN,
            to=FFT_FREQ_MAX,
            resolution=FFT_FREQ_STEP,
            orient=tk.HORIZONTAL,
            variable=self.fft_max_freq,
        )
        self.fft_freq_slider.pack(fill=tk.X, expand=True)

        ttk.Separator(controls_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=6)

        # Drive enable/disable controls (CiA402 Controlword state machine)
        self.enable_button = ttk.Button(
            controls_panel, text="Enable Drive", command=self.on_enable_click
        )
        self.enable_button.pack(fill=tk.X)

        self.disable_button = ttk.Button(
            controls_panel, text="Disable Drive", command=self.on_disable_click, state=tk.DISABLED
        )
        self.disable_button.pack(fill=tk.X, pady=(4, 0))

        ttk.Label(
            controls_panel, textvariable=self.drive_status_var, wraplength=150, justify=tk.LEFT
        ).pack(fill=tk.X, pady=(4, 0))

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

    def on_enable_click(self):
        if MINIMAL_GUI_ON_DRIVE:
            self.figure.set_visible(False)        # Hide matplotlib figure to eliminate GIL contention
            self.slider.config(state=tk.DISABLED)          # Disable time window slider
            self.fft_freq_slider.config(state=tk.DISABLED)  # Disable FFT frequency slider
            self.plotting_enabled = False
            self.drive_active = True
        self.enable_button.config(state=tk.DISABLED)
        self.drive_status_var.set("Drive: enabling...")
        self.command_queue.put(("enable",))

    def on_disable_click(self):
        self.disable_button.config(state=tk.DISABLED)
        self.command_queue.put(("disable",))

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

            if event == "drive_enabled":
                self.disable_button.config(state=tk.NORMAL)
                self.drive_status_var.set(f"Drive: enabled (SW=0x{payload:04X})")

            elif event == "drive_enable_error":
                self.enable_button.config(state=tk.NORMAL)
                self.drive_status_var.set(f"Drive enable failed: {payload}")

            elif event == "drive_disabled":
                self.enable_button.config(state=tk.NORMAL)
                self.drive_status_var.set(f"Drive: disabled (SW=0x{payload:04X})")
                if MINIMAL_GUI_ON_DRIVE:
                    self.figure.set_visible(True)        # Re-enable plots for analysis
                    self.slider.config(state=tk.NORMAL)          # Re-enable sliders
                    self.fft_freq_slider.config(state=tk.NORMAL)
                    self.plotting_enabled = True
                    self.drive_active = False
                    self._needs_full_draw = True  # Force full redraw with current data

            elif event == "started":
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
            
            elif event == "drive_fault_secondary":
                self.enable_button.config(state=tk.NORMAL)
                self.drive_status_var.set(f"Drive: FAULTED during operation")
                self.status_var.set(f"Secondary Fault Diagnostics: {payload}")

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

        # Only perform plotting if enabled (skipped during drive operation to reduce GIL contention)
        if self.plotting_enabled and snapshot:
            window = self.window_seconds.get()
            now = snapshot[-1][0]
            cutoff = now - window

            visible = [s for s in snapshot if s[0] >= cutoff]

            times              = [s[0] for s in visible]
            positions          = [s[1] for s in visible]
            currents           = [s[2] for s in visible]
            analog_inputs_2    = [s[3] for s in visible]
            velocities         = [s[4] for s in visible]

            # Express x as "seconds before now" so xlim stays fixed at
            # [-window, 0] — a stable coordinate space that allows blitting
            # without the axes drifting between full redraws.
            rel_times = [t - now for t in times]

            self.line_position.set_data(rel_times, positions)
            self.line_current.set_data(rel_times, currents)
            self.line_velocity.set_data(rel_times, velocities)

            # Update live analog input 2 display (latest value in the status label)
            if analog_inputs_2:
                ai2_status = f"AI2: {analog_inputs_2[-1]:+6d}"
            else:
                ai2_status = "AI2: --"
            
            # # Create a composite status including drive status and analog input
            # current_drive_status = self.drive_status_var.get()
            # if "Drive:" in current_drive_status:
            #     # Extract just the drive status part and append AI2
            #     self.drive_status_var.set(f"{current_drive_status}  {ai2_status}")

            self._blit_counter += 1
            full_draw = self._needs_full_draw or (self._blit_counter % FULL_REDRAW_EVERY == 0)

            if full_draw:
                self._needs_full_draw = False
                self.ax_position.set_xlim(-window, 0.0)
                self.ax_position.relim()
                self.ax_position.autoscale_view(scalex=False, scaley=True)
                self.ax_current.relim()
                self.ax_current.autoscale_view(scalex=False, scaley=True)
                self.ax_velocity.relim()
                self.ax_velocity.autoscale_view(scalex=False, scaley=True)
                self._update_fft_plots(times, positions, currents)
                self.canvas.draw()
                self._blit_bg = self.canvas.copy_from_bbox(self.figure.bbox)
            else:
                # Fast path: restore cached background and blit only the lines.
                self.canvas.restore_region(self._blit_bg)
                self.ax_position.draw_artist(self.line_position)
                self.ax_current.draw_artist(self.line_current)
                self.ax_velocity.draw_artist(self.line_velocity)
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
