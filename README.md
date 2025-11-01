# ESPHome Ouman Component

This is an ESPHome component for communicating with Ouman heat pump controllers over their serial interface. Currently supports the Ouman Geopro series.

## Supported Features

- Temperature sensor readings
- Valve positions
- Operating hours
- Status indicators
- Heat pump settings
- Heating curve configuration

## Installation

In your ESPHome configuration, add:

```yaml
external_components:
  - source: github://MatiasPuhakka/esphome-geopro202s@main
    components: [ geopro_202s ]
```

## Basic Usage

```yaml
# Example configuration
uart:
  tx_pin: GPIO1
  rx_pin: GPIO3
  baud_rate: 4800
  data_bits: 8
  parity: NONE
  stop_bits: 1

ouman:
  id: my_ouman
  # Temperature sensors
  outside_temp:
    name: "Outside Temperature"
  supply_temp:
    name: "Supply Temperature"
  tank_top:
    name: "Tank Top Temperature"
  
  # Operating status
  compressor:
    name: "Compressor Running"
  
  # Heating curve
  heating_curve_minus20:
    name: "Heating Curve -20°C"
    min_value: 20
    max_value: 80
```

## Supported Devices

Currently tested with:
- Ouman Geopro 202S

## Protocol Documentation

The component implements the Ouman serial protocol with the following features:
- Temperature readings (0x04 messages)
- Valve positions (0x03 messages)
- Status values (0x02 messages)
- Configuration banks (0x21 messages)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)