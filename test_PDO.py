import struct
import time
import csv

import pysoem

# ------------ CONFIGURATION ------------
ADAPTER_NAME = r"\\Device\\NPF_{FEDAB1B5-C8AC-4C77-9EAB-A081EF22B39C}"

LOG_FILE = "motor_current_log.csv"

CYCLE_TIME_S = 0.001      # 1 ms target cycle
PRINT_INTERVAL_S = 1.0    # print once per second
CSV_BATCH_SIZE = 100      # write every 100 samples
# ---------------------------------------


def main():

    master = pysoem.Master()
    master.open(ADAPTER_NAME)

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
    master.write_state()

    master.state_check(pysoem.OP_STATE, 50000)

    if master.state != pysoem.OP_STATE:
        raise RuntimeError("Failed to reach OP state")

    print("EtherCAT operational.")

    with open(LOG_FILE, "w", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            "elapsed_s",
            "cycle_ms",
            "current_A",
            "position_counts",
            "velocity_counts_per_sec"
        ])

        sample_buffer = []

        start_time = time.perf_counter()
        next_cycle = start_time

        last_print = start_time
        last_loop_time = start_time

        sample_count = 0

        try:

            while True:

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
                master.receive_processdata(2000)

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

                sample_buffer.append([
                    f"{elapsed:.6f}",
                    f"{actual_cycle_ms:.3f}",
                    f"{current_amps:.5f}",
                    position,
                    velocity
                ])

                sample_count += 1

                #
                # Batch CSV writes
                #
                if len(sample_buffer) >= CSV_BATCH_SIZE:
                    writer.writerows(sample_buffer)
                    sample_buffer.clear()

                #
                # Print once per second
                #
                if (now - last_print) >= PRINT_INTERVAL_S:

                    avg_freq = sample_count / elapsed

                    print(
                        f"t={elapsed:8.3f}s  "
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

        except KeyboardInterrupt:

            print("\nStopping logger...")

            if sample_buffer:
                writer.writerows(sample_buffer)

    master.close()


if __name__ == "__main__":
    main()
