"""
Logs actual motor current and position from an ADVANCED Motion Controls
DPE EtherCAT drive.

Uses SDO reads (mailbox communication, available in PRE-OP state) rather
than cyclic PDO exchange -- simpler to set up, but limited to roughly
tens of Hz rather than kHz-rate logging.

Object reference (from AMC EtherCAT Communication Manual):
  6077h     Actual Current        Int16,  units = DC1,  scale = 2^13 / K_P
  20D8.0Ch  Maximum Peak Current  UInt16, units = PBC,   scale = value / 10 (amps)
  K_P = the drive's Maximum Peak Current in amps (read once at startup)

  6064h     Actual Position       Int32,  units = counts (no scaling needed --
            reads the measured position of the primary feedback device
            directly in encoder counts)

Requires: pip install pysoem
"""

import struct
import time
import csv

import pysoem

# -------- CONFIGURE THIS --------
ADAPTER_NAME = r"\Device\NPF_{FEDAB1B5-C8AC-4C77-9EAB-A081EF22B39C}"  # from slaveinfo / Npcap
LOG_FILE = "motor_current_log.csv"
POLL_INTERVAL_S = 0.05  # SDO reads are mailbox-based; ~20 Hz is a reasonable default
# ---------------------------------


def main():
    master = pysoem.Master()
    master.open(ADAPTER_NAME)

    if master.config_init() <= 0:
        raise RuntimeError("No EtherCAT slaves found. Check cabling and adapter name.")

    slave = master.slaves[0]
    print(f"Connected to slave: {slave.name}")

    # Read K_P (Maximum Peak Current) once -- object 20D8h, subindex 0Ch
    raw_max_peak = struct.unpack("<H", slave.sdo_read(0x20D8, 0x0C))[0]
    k_p_amps = raw_max_peak / 10.0  # PBC units: raw value is in 0.1 A steps
    print(f"Drive Maximum Peak Current (K_P): {k_p_amps} A")

    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["elapsed_s", "actual_current_A", "actual_position_counts"])

        print("Logging actual motor current... Press Ctrl+C to stop.")
        start_time = time.time()
        try:
            while True:
                # Object 6077h: Actual Current (Int16, DC1 units)
                raw_current = struct.unpack("<h", slave.sdo_read(0x6077, 0x00))[0]
                current_amps = raw_current * k_p_amps / 8192.0  # 2^13 = 8192

                # Object 6064h: Actual Position (Int32, plain counts -- no scaling)
                position_counts = struct.unpack("<i", slave.sdo_read(0x6064, 0x00))[0]

                elapsed = time.time() - start_time
                writer.writerow([f"{elapsed:.3f}", f"{current_amps:.4f}", position_counts])
                f.flush()

                print(f"t={elapsed:7.2f}s   current={current_amps:+.3f} A   position={position_counts:+d} counts")
                time.sleep(POLL_INTERVAL_S)

        except KeyboardInterrupt:
            print("\nLogging stopped by user.")

    master.close()


if __name__ == "__main__":
    main()