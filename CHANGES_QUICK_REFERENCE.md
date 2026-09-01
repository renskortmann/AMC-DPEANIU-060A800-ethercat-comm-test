# Quick Reference: Code Changes for Analog Input 2 Integration

## Key Changes at a Glance

### 1. New Constant (Line 71)
```python
ANALOG_INPUT_2_TPDO_OFFSET = 14  # PDO byte offset for AI2
```

### 2. Updated RECORD_STRUCT (Line 78)
```diff
- RECORD_STRUCT = struct.Struct("<dffii")  
+ RECORD_STRUCT = struct.Struct("<dfffii")  # Added analog_input_2_raw
```

### 3. TxPDO Verification in connect_and_configure() (After Line 106)
```python
# Read back actual TxPDO mapping to verify Analog Input 2 is present
tpdo_count = struct.unpack("<B", slave.sdo_read(0x1A00, 0x00))[0]
mapped_entries = [
    struct.unpack("<I", slave.sdo_read(0x1A00, sub))[0]
    for sub in range(1, tpdo_count + 1)
]
print(f"Active TxPDO mapping ({tpdo_count} entries): "
      + ", ".join(f"0x{e:08X}" for e in mapped_entries))
```

### 4. Read Analog Input 2 from PDO (Line 405)
```python
analog_input_2_raw = struct.unpack_from("<h", pdo, ANALOG_INPUT_2_TPDO_OFFSET)[0]
```

### 5. Add to Buffer (Line 412)
```diff
- buffer.append((elapsed, position, current_amps))
+ buffer.append((elapsed, position, current_amps, analog_input_2_raw))
```

### 6. Add to Binary Log (Lines 419-420)
```diff
  log_byte_buffer += RECORD_STRUCT.pack(
-     elapsed, actual_cycle_ms, current_amps, position, velocity
+     elapsed, actual_cycle_ms, current_amps, analog_input_2_raw, position, velocity
  )
```

### 7. Console Output Update (Line 440)
```diff
  print(
      f"...current={current_amps:+8.3f}A  "
+     f"AI2={analog_input_2_raw:+6d}  "
      f"Pos={position:+10d}  ..."
  )
```

### 8. CSV Export Header (Line 506)
```diff
  writer.writerow([
      "elapsed_s",
      "cycle_ms", 
      "current_A",
+     "analog_input_2_raw",
      "position_counts",
      "velocity_counts_per_sec"
  ])
```

### 9. CSV Export Unpacking (Line 520)
```diff
- elapsed, cycle_ms, current_amps, position, velocity = RECORD_STRUCT.unpack(chunk)
+ elapsed, cycle_ms, current_amps, analog_input_2_raw, position, velocity = RECORD_STRUCT.unpack(chunk)
```

### 10. CSV Export Writing (Line 526)
```diff
  writer.writerow([
      ...
      f"{current_amps:.5f}",
+     analog_input_2_raw,
      position,
      velocity
  ])
```

### 11. Simulation AI2 (Line 635)
```python
analog_input_2_raw = int(position * 0.1 + SIM_NOISE_AMP * 100 * (2.0 * np.random.random() - 1.0))
```

### 12. Simulation Buffer (Line 638)
```diff
- buffer.append((elapsed, position, current_amps))
+ buffer.append((elapsed, position, current_amps, analog_input_2_raw))
```

### 13. Simulation Logging (Lines 641-642)
```diff
  log_byte_buffer += RECORD_STRUCT.pack(
-     elapsed, actual_cycle_ms, current_amps, position, velocity
+     elapsed, actual_cycle_ms, current_amps, analog_input_2_raw, position, velocity
  )
```

### 14. GUI Buffer Unpacking (Line 864-866)
```python
positions          = [s[1] for s in visible]
currents           = [s[2] for s in visible]
analog_inputs_2    = [s[3] for s in visible]  # NEW LINE
```

### 15. GUI AI2 Status Display (Line 870-875)
```python
# Update live analog input 2 display (latest value in the status label)
if analog_inputs_2:
    ai2_status = f"AI2: {analog_inputs_2[-1]:+6d}"
else:
    ai2_status = "AI2: --"
```

## Testing the Changes

### Verify Syntax
```bash
python -m py_compile test_PDO.py
```

### Run Verification Tests
```bash
python test_changes_verification.py
```

### Run with Hardware (or simulation if pysoem unavailable)
```bash
python test_PDO.py
```

## Data Flow Diagram

```
PDO Input (TxPDO)
    ↓
Byte Offset Extraction
    ├─ 0-1: Status Word
    ├─ 2-5: Position
    ├─ 6-9: Velocity
    ├─ 10-11: Current
    └─ 14-15: Analog Input 2 ← NEW
        ↓
Buffer (per 1ms cycle)
    └─→ (elapsed, position, current_amps, analog_input_2_raw) ← 4 fields now
        ↓
        ├─ GUI Display (live plots)
        └─ File Logging (.dat binary)
            ↓
            CSV Export (convert_dat_to_csv)
                └─ .csv file with all channels
```

## Verification Checklist

- [x] Constants defined correctly
- [x] RECORD_STRUCT format updated
- [x] PDO offset calculations verified
- [x] Binary pack/unpack works
- [x] Buffer structure updated
- [x] Console output includes AI2
- [x] CSV export includes AI2
- [x] Simulation mode includes AI2
- [x] GUI handles new buffer format
- [x] TxPDO mapping verification added
- [x] Syntax check passed
- [x] Verification tests passed

## Next: Hardware Commissioning

1. Load the updated script onto the test machine
2. Connect to the drive with pysoem available
3. Watch console output for TxPDO mapping verification
4. Enable the drive and perform cross-check:
   - Vary laser sensor distance
   - Verify AI2 output changes
   - Verify Position output changes correspondingly
5. If AI2 changes but Position doesn't → reconfigure DriveWare Position Feedback Source
6. If both move together → laser sensor is already correctly configured!
