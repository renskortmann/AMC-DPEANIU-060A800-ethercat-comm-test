# Plan: Verify & Harden Laser Position Sensor Readout in `test_PDO.py`

## Context

`test_PDO.py` is a working EtherCAT test harness that intentionally:
- Runs the drive in Cyclic Synchronous Torque (CST) mode
- Commands a sine-wave current to move the motor
- Logs/plots **Actual Current** (0x6077) and **Actual Position** (0x6064) at ~1 kHz

This is correct and intentional — **no changes to the motor-driving behavior are needed.**

The open question is whether the **"Position" channel** in this script actually reflects
the ±10V laser displacement sensor wired to **PAI-2** (AUX Encoder connector, C4), or
whether it is instead reporting the drive's primary motor-mounted feedback device
(encoder/Halls used for commutation).

### Why this is ambiguous today

- `0x6064` ("Actual Position") = `2012.01h` ("Position Measured") per the EtherCAT
  Communication Manual. Its description is generic: "the current measured position in
  counts." It reflects whatever DriveWare's **Position Feedback Source** is configured
  to use — this is a drive-side DriveWare setting, invisible to and unverified by this
  script.
- The drive also exposes dedicated analog input readback objects that are **not**
  currently read anywhere in the script:
  - `201A.02h` — Analog Input 2 Value (scaled, PDO-mappable)
  - `2022.02h` — Analog Input 2 ADC Raw Value (PDO-mappable)
- Neither the EtherCAT Communication Manual nor the DriveWare Software Manual (as
  reviewed) explicitly states that object-dictionary "Analog Input 2" corresponds to
  the physical **PAI-2** pin. This is a reasonable assumption (PAI-1 ↔ Analog Input 1,
  PAI-2 ↔ Analog Input 2) but is currently **unverified**.

## Goal

Add an independent, direct readout of the physical PAI-2 analog channel so the script
can **cross-check** that `Actual Position` (0x6064) is actually tracking the laser
sensor, rather than trusting the DriveWare feedback-source configuration blindly.

---

## Tasks

### 1. Add Analog Input 2 to the TxPDO read path

- [ ] In `connect_and_configure()` (or immediately after `master.config_map()`), extend
      the TxPDO mapping to include `201A.02h` (Analog Input 2 Value, 16-bit) in addition
      to the existing default-mapped objects. Do this via SDO writes to `1A00h` sub-indices
      (see EtherCAT Communication Manual §"1A00h: Transmit PDO Mapping" and
      Appendix B for the mapping-object write procedure), appending it as a new mapped
      entry rather than replacing any existing default entries.
  - Confirm the new byte offset this creates at the end of the existing TxPDO
    (default TxPDO occupies bytes 0–13, per Table B.2, so the new 16-bit Analog Input 2
    Value should land at byte offset 14, immediately after Digital Inputs).
  - Add a module-level constant, e.g. `ANALOG_INPUT_2_TPDO_OFFSET = 14`, instead of a
    hardcoded magic number inline.
- [ ] Update the `struct.unpack_from` calls in `acquisition_loop()` to also read:
  ```python
  analog_input_2_raw = struct.unpack_from("<h", pdo, ANALOG_INPUT_2_TPDO_OFFSET)[0]
  ```
- [ ] If remapping the TxPDO in code proves impractical (e.g. project file already
      fixed in DriveWare, or `master.config_map()` doesn't expose raw mapping-object
      writes cleanly via `pysoem`), fall back to an **SDO read once per second** (not
      once per 1 kHz cycle — SDO is slow) inside the existing "print once per second"
      block:
  ```python
  analog_input_2_raw = struct.unpack("<h", slave.sdo_read(0x201A, 0x02))[0]
  ```
  This is lower rate but sufficient purely as a correctness cross-check, not for
  control-loop use.

### 2. Surface the raw analog reading alongside Position

- [ ] Add `analog_input_2_raw` (or its converted voltage, if a conversion factor is
      documented — see Task 4) to the `buffer.append(...)` tuple in `acquisition_loop`.
- [ ] Update `RECORD_STRUCT` if this value should also be persisted to the `.dat` log
      file, and update `convert_dat_to_csv` (or equivalent) accordingly so the CSV
      export includes this new column.
- [ ] In the GUI (`ScopeGUI`), add a small text readout or a third small subplot showing
      the live Analog Input 2 raw/voltage value next to the existing Position and
      Current plots. This does not need FFT or blitting — a simple periodically-updated
      label is sufficient.

### 3. Cross-check procedure (manual verification step, not code)

- [ ] With the drive disabled (motor not moving), manually vary the laser sensor's
      target distance (e.g., move a reflective target closer/farther) and confirm:
  - The new Analog Input 2 readout changes accordingly.
  - `Actual Position` (0x6064) changes in the same direction and in a way consistent
    with the configured Scale/Offset.
  - If `Actual Position` does **not** move while Analog Input 2 clearly does, this
    confirms DriveWare's Position Feedback Source is **not** currently set to the
    analog input, and needs to be reconfigured (see DriveWare Software Manual,
    Loop Feedback → Position Feedback Source → Analog Input; select PAI-2 channel;
    set Scale/Offset). This is a DriveWare/drive configuration fix, not a script fix.
- [ ] Document the confirmed PAI-2 ↔ "Analog Input 2" mapping (or correct mapping, if
      it turns out to be Analog Input 1 or another channel) in a code comment near the
      new constant from Task 1, since this is not stated explicitly in AMC's manuals.

### 4. Add unit conversion for display (nice-to-have, not blocking)

- [ ] Currently `position` is displayed/plotted as raw counts only
      (`ax_position.set_ylabel("Position (counts)")`). Once the Scale factor used in
      DriveWare's Analog Input configuration is known, add a conversion constant
      (e.g. `COUNTS_PER_MM` or similar, matching whatever physical unit the laser
      sensor reports in) and expose a secondary axis or converted printout in
      real-world units (mm, in, etc.) for readability during testing.
- [ ] Do the same for the raw Analog Input 2 value if a volts-per-count or
      volts-per-LSB conversion is documented (see EtherCAT Communication Manual
      Appendix, "DAI" unit conversion, referenced from the `201A.02h` object
      description) — convert to volts for an intuitive sanity check against the
      sensor's known ±10V output range.

### 5. Verify configuration persistence (Store vs. Apply, and PDO mapping survival)

Background: DriveWare only guarantees a setting survives a power cycle if it was
explicitly **Stored to Drive** (not just Applied — Apply is live/volatile only).
Separately, the EtherCAT Communication Manual's object dictionary documents an
asymmetry in what's marked "Stored to NVM":

| Object | Stored to NVM per manual? |
|---|---|
| `1600.00h` (RPDO mapping count) | No |
| `1600.01h`–`1600.10h` (RPDO mapping slots) | Yes |
| `1A00.00h` (TPDO mapping count) | Yes |
| `1A00.01h`–`1A00.10h` (TPDO mapping slots) | Yes |

Whether the drive's stored TxPDO mapping (including the new Analog Input 2 entry
from Task 1) is actually what `pysoem`'s `master.config_map()` ends up using at
connection time — versus the master imposing its own default mapping — is not
something governed by AMC's documentation; it depends on `pysoem`'s auto-discovery
behavior. This must be verified empirically, not assumed.

- [ ] In `connect_and_configure()`, immediately after `master.config_map()` and before
      transitioning to OP state, add an SDO readback of the active TxPDO mapping:
  ```python
  tpdo_count = struct.unpack("<B", slave.sdo_read(0x1A00, 0x00))[0]
  mapped_entries = [
      struct.unpack("<I", slave.sdo_read(0x1A00, sub))[0]
      for sub in range(1, tpdo_count + 1)
  ]
  print(f"Active TxPDO mapping ({tpdo_count} entries): "
        + ", ".join(f"0x{e:08X}" for e in mapped_entries))
  ```
  Each 32-bit entry decodes as `(index << 16) | (sub_index << 8) | bit_length` per
  Table 1.1 in the manual — confirm the Analog Input 2 entry (`0x201A02` in the
  index/sub-index portion) is present in this list before trusting that
  `ANALOG_INPUT_2_TPDO_OFFSET` is valid.
- [ ] If the Analog Input 2 entry is **not** present after `config_map()` (i.e. the
      master reset the mapping to factory default rather than reusing the
      DriveWare-configured/stored one), do not rely on DriveWare-side persistence.
      Instead, have `connect_and_configure()` explicitly (re)configure the full desired
      TxPDO mapping via SDO writes to `1A00.00h` (set to 0), `1A00.01h`–`1A00.06h` (or
      however many entries), then `1A00.00h` again (set to final count) — all while the
      slave is in Pre-Operational state, per the manual's "PDO Configuration" section —
      before calling `master.config_map()`. This makes the script self-sufficient and
      not dependent on whatever mapping state DriveWare last left on the drive.
- [ ] Separately confirm general (non-PDO) configuration persistence: after power
      cycling the drive once (with DriveWare disconnected), reconnect with the Python
      script and confirm the Position Feedback Source / Scale / Offset behavior from
      Task 3 still holds (Analog Input 2 still tracks the laser sensor as expected).
      This confirms those settings were actually Stored (not just Applied) in
      DriveWare.

### 6. Regression check

- [ ] Confirm the existing default TxPDO fields (Status Word, Actual Position, Actual
      Velocity, Actual Current) still parse correctly at their original offsets (0, 2,
      6, 10) after adding the new mapped object — appending should not shift existing
      offsets, but verify this empirically against a live PDO exchange before trusting
      it. This is the same readback mechanism added in Task 5 — reuse it rather than
      duplicating logic.
- [ ] Confirm `master.expected_wkc` / working counter still validates correctly after
      the TxPDO size increases (`WKC` printed each second in the existing status line).
- [ ] Run the existing enable → sine current → log → convert-to-CSV flow end-to-end
      once more after these changes to confirm no regressions in motor motion or
      logging behavior.

---

## Out of scope for this task

- Changing the drive's control mode away from Cyclic Synchronous Torque — the
  motor-driving current sine wave is intentional and should not be modified.
- Tuning the position loop gains — unrelated to this verification task.
- Any change to `run_enable_sequence`, the CiA402 state machine handling, or
  fault-reset logic — these are unaffected by this work.
