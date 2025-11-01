# Feature Comparison: Inline YAML vs Component Implementation

## ✅ Temperature Sensors (0x04 messages)

Both implementations support the same temperature sensors:

| Sensor ID | Name             | Inline YAML | Component |
| --------- | ---------------- | ----------- | --------- |
| 0x12      | Outside temp     | ✅          | ✅        |
| 0x15      | L1 room temp     | ✅          | ✅        |
| 0x14      | L1 supply temp   | ✅          | ✅        |
| 0x1B      | Free measurement | ✅          | ✅        |
| 0x18      | Tank top input   | ✅          | ✅        |
| 0x21      | Tank top         | ✅          | ✅        |
| 0x17      | Tank middle      | ✅          | ✅        |
| 0x22      | Tank bottom      | ✅          | ✅        |
| 0x19      | Brine            | ✅          | ✅        |

**Status: ✅ Match**

## ✅ Valve Position Sensors (0x03 messages)

Both implementations support the same valve sensors:

| Sensor ID | Name      | Inline YAML | Component |
| --------- | --------- | ----------- | --------- |
| 0x31      | L1 valve  | ✅          | ✅        |
| 0x33      | DHW valve | ✅          | ✅        |

**Status: ✅ Match**

## ✅ Hour Counter Sensors (0x04 messages, raw values)

Both implementations support the same hour counters:

| Sensor ID | Name                  | Inline YAML | Component |
| --------- | --------------------- | ----------- | --------- |
| 0x3A      | Electric heater hours | ✅          | ✅        |
| 0x3B      | Compressor hours      | ✅          | ✅        |

**Status: ✅ Match**

## ✅ Status Word Sensor

Both implementations support status word:

| Sensor ID | Name        | Inline YAML | Component |
| --------- | ----------- | ----------- | --------- |
| 0x2D      | Status word | ✅          | ✅        |

**Status: ✅ Match**

## ⚠️ Binary Sensors (Status Bits)

Comparison of binary sensors:

| Bit Mask | Name            | Inline YAML | Component | Notes              |
| -------- | --------------- | ----------- | --------- | ------------------ |
| 0x10     | Compressor      | ✅          | ✅        |                    |
| 0x08     | Electric heater | ✅          | ✅        |                    |
| 0x04     | Digi3           | ❌          | ✅        | Not in inline YAML |
| 0x02     | Digi2           | ❌          | ✅        | Not in inline YAML |
| 0x01     | Digi1           | ❌          | ✅        | Not in inline YAML |

**Status: ⚠️ Component has MORE features (Digi1-3)**

## ❌ Configuration Bank Readings (0x21 messages)

**MAJOR MISSING FEATURE in Component Implementation**

### Bank 0x0C - Heating Circuit Settings (9 values)

| Parameter             | Inline YAML | Component |
| --------------------- | ----------- | --------- |
| L1 -20°C point        | ✅          | ❌        |
| L1 0°C point          | ✅          | ❌        |
| L1 +20°C point        | ✅          | ❌        |
| L1 Night effect       | ✅          | ❌        |
| L1 Min limit          | ✅          | ❌        |
| L1 Max limit          | ✅          | ❌        |
| L1 Autumn dry         | ✅          | ❌        |
| L1 Outside temp delay | ✅          | ❌        |
| L1 Pre-increase       | ✅          | ❌        |

### Bank 0x2C - L1 Settings (1 value)

| Parameter       | Inline YAML | Component |
| --------------- | ----------- | --------- |
| L1 Summer close | ✅          | ❌        |

### Bank 0x0B - Heat Pump Settings (15 values)

| Parameter            | Inline YAML | Component |
| -------------------- | ----------- | --------- |
| Control mode         | ✅          | ❌        |
| Tank bottom min      | ✅          | ❌        |
| EH delay time        | ✅          | ❌        |
| Tank top summer      | ✅          | ❌        |
| Tank top winter      | ✅          | ❌        |
| Extra heating        | ✅          | ❌        |
| Extra heating time   | ✅          | ❌        |
| Compressor lock time | ✅          | ❌        |
| Tank top EH diff     | ✅          | ❌        |
| Tank bottom diff     | ✅          | ❌        |
| Tank top diff        | ✅          | ❌        |
| DHW pre-open         | ✅          | ❌        |
| DHW lock time        | ✅          | ❌        |
| Brine alert          | ✅          | ❌        |

**Status: ❌ Component MISSING all 25 configuration bank sensors**

## Summary

### ✅ Features Present in Both

- 9 Temperature sensors
- 2 Valve position sensors
- 2 Hour counter sensors
- 1 Status word sensor
- 2 Binary sensors (compressor, electric heater)

### ⚠️ Features Only in Component

- 3 Additional binary sensors (Digi1, Digi2, Digi3)

### ❌ Features Only in Inline YAML

- **25 Configuration bank sensors** from banks 0x0C, 0x2C, and 0x0B
- These include all heating curve settings, heat pump configuration parameters, and tank settings

## Conclusion

The component implementation is **missing critical functionality** for reading configuration banks. The inline YAML implementation has:

- Complete bank reading support with parsing for all 3 banks
- Automatic polling of banks every 60 seconds
- All 25 configuration parameters exposed as sensors

To achieve feature parity, the component needs:

1. Bank reading protocol support (TYPE_BANK = 0x21)
2. Parsing logic for banks 0x0C, 0x2C, and 0x0B
3. Configuration schema for bank sensors
4. Scheduling logic for bank reading requests
