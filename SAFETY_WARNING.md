# ⚠️ SAFETY WARNING - Write Functionality

## ⚠️ UNVERIFIED PROTOCOL - USE AT YOUR OWN RISK ⚠️

The **write functionality** for bank settings is **NOT VERIFIED** and may not work correctly or could potentially cause issues with your heat pump controller.

## What's Unverified

1. **Write Command Byte**: We assumed `0x82` (read uses `0x81`), but this is **NOT CONFIRMED**
2. **Write Message Format**: The format `[0x02, 0x82, 0x03, bank_id, offset, value, crc]` is **ASSUMED**
3. **No Documentation**: There are no examples or documentation of write commands in the codebase
4. **No Testing**: This functionality has **NOT been tested** with an actual device

## Potential Risks

- ❌ **Incorrect values** could be written to the controller
- ❌ **Wrong protocol** might send invalid commands that confuse the controller
- ❌ **Safety-critical settings** (temperatures, limits) could be changed incorrectly
- ❌ **System damage** is possible if critical settings are modified incorrectly

## Recommended Testing Approach

If you decide to test the write functionality:

### 1. **Start with Read-Only First** ✅
   - Use only sensors (read-only) until you verify the system works correctly
   - Monitor all values for several days to understand normal operation

### 2. **Enable Verbose Logging** 📋
   ```yaml
   logger:
     level: VERBOSE  # See all write commands in logs
   ```

### 3. **Test with Non-Critical Settings First** 🧪
   Start with settings that are **NOT safety-critical**:
   - `l1_night_effect` (night reduction)
   - `l1_autumn_dry` (autumn dry mode)
   - Avoid testing: temperature limits, tank temps, compressor locks

### 4. **Test One Setting at a Time** 🔬
   - Write ONE value
   - Wait and verify it was accepted (read back)
   - Check logs for any errors or unexpected responses

### 5. **Verify Write Success** ✔️
   - After writing, immediately read back the bank value
   - Compare written value vs. read value
   - If they don't match, the write protocol is likely wrong

### 6. **Keep Backup Settings** 💾
   - Document your current settings before testing
   - Have a way to restore defaults if needed
   - Consider if your device has a factory reset option

### 7. **Monitor System Behavior** 👀
   - Watch for unexpected behavior after writes
   - Monitor temperatures and operation closely
   - Be ready to power cycle or reset if needed

## How to Test Safely

```yaml
logger:
  level: VERBOSE  # Enable detailed logging

geopro_202s:
  id: geopro
  # First, just test ONE non-critical setting
  l1_night_effect:
    name: "L1 Night Effect"
    min_value: -10
    max_value: 10
    step: 1
```

After changing a value:
1. Check ESPHome logs for write command details
2. Immediately read back the bank (should happen automatically after 60s)
3. Verify the value matches what you wrote
4. Monitor system operation for several minutes

## What to Look For

### ✅ Signs Write Protocol Works:
- Value changes match what you wrote
- Device responds normally
- No error messages in logs
- System continues operating correctly

### ❌ Signs Write Protocol is Wrong:
- Written value doesn't match read value
- Device stops responding
- Error messages or unexpected responses
- System behaves unexpectedly

## Recommendation

**For now, use READ-ONLY sensors only** until:
- The write protocol can be verified through documentation
- Or someone can reverse-engineer it by monitoring actual write commands
- Or Ouman provides official protocol documentation

## Contributing

If you successfully test write functionality:
- Please document the exact protocol format
- Share any logs showing successful writes
- Update the code with verified protocol details
- Add this information to help others!

## Current Status

- ✅ **Read functionality**: VERIFIED and working
- ⚠️ **Write functionality**: UNVERIFIED - USE WITH CAUTION

