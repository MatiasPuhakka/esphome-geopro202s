# ESPHome Geopro 202S Component

This is an ESPHome component for communicating with Ouman Geopro 202S heat pump controllers over their serial interface.

## Supported Features

- **Temperature Sensors** - 9 sensors including outside, supply, tank, and brine temperatures
- **Valve Positions** - L1 and DHW (domestic hot water) valve positions
- **Operating Hours** - Electric heater and compressor runtime counters
- **Status Indicators** - Binary sensors for compressor and electric heater status
- **Configuration Banks** - Read-only sensors for all 25 configuration parameters:
  - Bank 0x0C: Heating circuit settings (L1 curve points, limits, delays)
  - Bank 0x2C: L1 settings (summer close temperature)
  - Bank 0x0B: Heat pump settings (tank temperatures, delays, lock times)
- **Default Icons** - All sensors come with appropriate Material Design Icons

## Installation

In your ESPHome configuration, add:

```yaml
external_components:
  - source: github://MatiasPuhakka/esphome-geopro202s@main
    components: [geopro_202s]
```

## Basic Usage

```yaml
# Required: Configure UART for serial communication
uart:
  tx_pin: GPIO4
  rx_pin: GPIO16
  baud_rate: 4800
  data_bits: 8
  parity: NONE
  stop_bits: 1

# Main component configuration
geopro_202s:
  id: geopro

  # Temperature sensors (all optional - only include what you need)
  outside_temp:
    name: "Outside Temperature"
  l1_supply:
    name: "L1 Supply Temperature"
  tank_top:
    name: "Tank Top Temperature"

  # Binary status sensors
  compressor:
    name: "Compressor Running"
  el_heater:
    name: "Electric Heater Active"

  # Configuration bank sensors (optional, read-only)
  l1_minus20:
    name: "L1 -20°C Point"
  summer_temp:
    name: "Tank Summer Temperature"
```

See `example/geopro202s.yaml` for a complete configuration example with all available sensors.

## Protocol Documentation

The component implements the Geopro 202S serial protocol with the following message types:

- **0x04 messages** - Temperature readings and status values
- **0x03 messages** - Valve positions
- **0x21 messages** - Configuration bank readings (banks 0x0C, 0x2C, 0x0B)

The component automatically polls sensors every 10 seconds and configuration banks every 60 seconds.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
