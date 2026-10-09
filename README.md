# ESPHome Geopro 202S Component

This is an ESPHome component for communicating with Ouman Geopro 202S heat pump controllers over their serial interface.

## Supported Features

- **Temperature Sensors** - 9 sensors including outside, supply, tank, and brine temperatures
- **Valve Positions** - L1 and DHW (domestic hot water) valve positions (voltage-controlled motors only, see [Valve positions](#valve-positions))
- **Operating Hours** - Electric heater and compressor runtime counters
- **Status Indicators** - Binary sensors for compressor and electric heater status
- **Configuration Banks** - Read-only sensors for all 24 configuration values:
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

  # Poll intervals (optional, defaults shown)
  value_interval: 10s
  bank_interval: 60s

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

See `example/geopro202s.yaml` for a complete configuration example. It lists every sensor, with the valve positions commented out.

### Valve positions

`valve_l1` (address 0x31) and `valve_dhw` (address 0x33) only report a real position if that valve's motor is voltage-controlled (0-10 V or 2-10 V). A 3-point motor is pulsed open or closed, and the controller doesn't know where it is, so the value always reads 0 %. The manual's display legend matches this: it shows a 0-100 % bar for a voltage-controlled motor and only ▲/▼ arrows for a 3-point one.

Check each motor separately:

- **L1** - Huoltotila → Moottorivalinta shows the motor type for each circuit: 3-tila/aika, 0-10V or 2-10V.
- **DHW (JV)** - In Huoltotila → JV ohjaustapa → Käsiajo sähk., a 3-point motor shows only the drive direction, with no percentage.

Leave out the key for any valve with a 3-point motor. The example config has both keys commented out for this reason.

## Protocol Documentation

Every frame, request or reply, has the same shape:

```
02 <command> <length> <address hi> <address lo> <data...> <checksum>
```

- `02` is the start byte. The protocol does not escape it, so 0x02 can also appear in the address, data or checksum.
- `<command>` is 0x81 in a read request and 0x06 in a reply.
- `<length>` counts the address and data bytes, so a frame is `length + 4` bytes long. Valid lengths are 0x02 to 0x21.
- `<checksum>` is the low byte of the sum of every byte from the command byte up to the checksum.

A read request is `02 81 02 <address hi> <address lo> <checksum>`. The reply's data length depends on what was read:

- **1 byte** - Valve positions
- **2 bytes** - Temperature readings and status values
- **31 bytes** - Configuration bank readings (banks 0x0C, 0x2C, 0x0B)

The wire format lives in `frame.h`/`frame.cpp`, which have no ESPHome dependencies. Run their host tests with `make test`.

### Register map

Every config key is one row in the Register map, `register_map.py`: the address to read (for a setting, its bank), where the value starts in the reply's data, and a decode rule. The rule gives the width (1 or 2 bytes, big-endian), whether the value is signed, a divisor, and, for a status bit, a mask. Current rules:

- **Temperatures** - signed 16-bit, divided by 100
- **Valve positions** - unsigned 8-bit
- **Hour counters and the status word** - unsigned 16-bit
- **Status bits** - the status word (0x2D) masked, published as a binary sensor
- **Bank settings** - one byte at the setting's offset, signed unless noted

Several rows can share an address. The status word sensor and the five status bits all read 0x2D, which is requested once per cycle and decoded for every row from one reply. Status bits work without the `status_word` sensor.

Adding a value takes one row and no C++ change. The hub registers each row with `register_value()` and passes every reply to the decoder in `value_decoder.h`/`value_decoder.cpp`, which has no ESPHome dependencies and is covered by `make test`.

### Polling

The component reads every configured address once at startup, then reads values (temperatures, valves, hour counters, the status word) every `value_interval` (default 10 s) and configuration banks every `bank_interval` (default 60 s). Both take an ESPHome time period such as `30s` or `5min` and must be greater than zero. Each address is read once per cycle, however many values share it.

Only one request is on the bus at a time. The next request goes out 50 ms after the previous one got its reply. A request with no reply within 500 ms is sent once more; if that also goes unanswered, the component moves on and tries the address again next cycle. A reply only counts if it is for the address that was asked for.

This logic lives in `poll_scheduler.h`/`poll_scheduler.cpp`, which also have no ESPHome dependencies and are covered by `make test`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
