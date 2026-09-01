Looking at this fault diagnostic output, I can extract key information:

## Status Word Analysis

**SW=0x0228 (Fault detected):**
- Bit 3 (0x0008) = Fault flag is SET ✓
- Masked state: 0x0228 & 0x006F = 0x0020 (non-standard state)
- The drive has faulted but is in an unusual state (not standard CiA402 states)

## Error Register Analysis

**0x1001=['None']:**
- Error Register = 0x00 (all bits clear)
- **This is the critical clue** — no standard error bits are set
- This rules out: over-current, over-voltage, thermal, communication errors
- **The fault is NOT from standard CoE error conditions**

## Drive Protection Status (0x2002h)

The non-zero values in 0x2002 sub-indices point to **protection-level faults** (different from error register):

| Register | Value | Bits Set | Likely Meaning |
|----------|-------|----------|----------------|
| 0x2002.03 | 0x0440 | Bits 10, 6 | Drive Protection Status — likely **velocity/acceleration limit** or **position limit** |
| 0x2002.04 | 0x0402 | Bits 10, 1 | System Protection Status — protection event active |
| 0x2002.05 | 0x0041 | Bits 6, 0 | Drive Status 1 — operational state indicator |
| 0x2002.07 | 0x0001 | Bit 0 | Configuration Status — likely valid |

## Root Cause: Velocity/Acceleration Limit Exceeded

**Most likely diagnosis:** The sine-wave current command (2.0A @ 10Hz) is pushing the motor to velocities or accelerations that **exceed the drive's configured limits**. 

Evidence:
- Fault occurs at **t=10.602s** (well into operation, not at startup)
- **No error register bits** (rules out electrical faults)
- **0x2002.03 and 0x2002.04 protection status set** (indicates protection threshold crossed)
- Error is **sustained** (drives to fault state and stays there)

## Why This Happens

In **CST (Cyclic Synchronous Torque) mode**:
- You command current/torque directly
- The motor's velocity and position depend on **load and inertia**
- With 2.0A sine-wave commands at 10Hz on **low/no load**, the motor accelerates to high speeds
- Drive's firmware has built-in velocity limits for safety (encoder sync, mechanical limits, etc.)
- After ~10 seconds, the accumulating displacement/velocity triggers the protection threshold

## Solutions

**Option 1 (Quick test):** Reduce SINE_AMPLITUDE_A from 2.0 to 0.5–1.0 A to lower peak accelerations

**Option 2 (Better):** Configure drive's velocity/position limits via SDO before enable:
- Read current limits from drive (0x6081 = Profile Velocity, 0x607D = Max Position, 0x607E = Min Position)
- Or reduce command amplitude to stay within defaults

**Option 3 (Diagnostic):** Add monitoring to read velocity in real-time and confirm it's climbing toward a limit

**Action:** Try reducing `SINE_AMPLITUDE_A` to 0.5A and re-test. If fault disappears, this confirms velocity-limit hypothesis.