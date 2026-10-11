# Geopro 202S integration

An ESPHome component that reads values from an Ouman Geopro 202S heat pump controller over its serial bus and publishes them to Home Assistant. It only reads; it never changes a setting ([ADR 0003](docs/adr/0003-read-only-component.md)).

## Hardware

**Controller**:
The Ouman Geopro 202S that runs the heat pump and answers on the serial bus.
_Avoid_: heat pump (the machine the Controller runs), device

**Node**:
The ESP32 running ESPHome that talks to the Controller and to Home Assistant.
_Avoid_: device, ESP

**Component**:
The `geopro_202s` ESPHome external component that the Node runs.
_Avoid_: module, YAML protocol copy (the older implementation in YAML that the Component replaced)

## Plant

These terms use the Finnish labels from the Käsikirja (`manuals/Geopro 202S Käsikirja.pdf`). `docs/controller.md` has the rules that use them, with page numbers.

**M-number**:
One of the Controller's measurement inputs, M1 to M11 (Mittaus 1–11, terminals Mitt.1–Mitt.11; Käsikirja pp. 10, 39). The manual also calls the valve-motor outputs M1–M3 (p. 28); this glossary calls those Moott. L1, Moott. L2 and Moott. JV. The Register map reads these Addresses:

| M | Display label | Measures | Address |
|---|---|---|---|
| M1 | Ulkolämpö | outdoor temperature | 0x12 |
| M2 | L1 Menovesi | L1 supply water | 0x14 |
| M3 | L1 Huone | L1 room temperature | 0x15 |
| M4 | VaraajaKeski | tank middle | 0x17 |
| M5 | L2 Menovesi | L2 supply water | not read |
| M6 | Mittaus 6 | free measurement | 0x1B |
| M7 | Yläosa tulo | water into the tank top, after the tulistin and the electric heater | 0x18 |
| M8 | Maaliuos | brine | 0x19 |
| M9 | VaraajaYlä | tank top | 0x21 |
| M10 | VaraajaAla | tank bottom | 0x22 |
| M11 | Kompr.käynti | compressor running feedback (a contact, not a temperature) | not read |

_Avoid_: sensor number, sensor id

**ML**:
The Controller's ground-source heating circuit (maalämmitys), which heats the tank with the compressor and the electric heater.
_Avoid_: heat pump circuit

**JV**:
The ML circuit's diverting valve (jakoventtiili), which sends the condenser's water to the tank top or the tank middle.
_Avoid_: DHW valve

**VaraajaYlä**:
The tank-top setpoint the Controller computes from the outdoor temperature, running from Var.ylä kesä at +20 °C to Var.ylä talvi at −20 °C.
_Avoid_: tank top temperature (that is M9, which the Mittaukset display also labels VaraajaYlä)

**VaraajaYläEro**:
The differential (eroalue) the Controller uses when it heats the tank top. M9 falls this far below VaraajaYlä before the compressor starts.
_Avoid_: top difference

**VaraajaAlaEro**:
The differential (eroalue) the Controller uses when it heats the lower part of the tank.
_Avoid_: bottom difference

**VaraajaAlaMin**:
The lowest tank-bottom temperature the Controller keeps, whatever the heating circuits ask for.
_Avoid_: tank minimum

**Kompr.esto**:
The M10 temperature at which the Controller always stops the compressor.
_Avoid_: compressor lock

**ML Ohjaustapa**:
Which heat sources the ML circuit may use: Kompr.+sähköv. (0), Kompressori (1) or Sähkövastus (2). The manual's menu is ML Ohjaustavat (p. 21); this is its singular.
_Avoid_: heat pump mode

## Wire protocol

**Frame**:
One unit on the serial bus: start byte 0x02, Command byte, Length byte, a 16-bit Address followed by data, and a Checksum. 0x02 is never escaped, so it can appear anywhere in a Frame, and only the Length byte marks where the Frame ends.
_Avoid_: message, packet

**Read request**:
A Frame the Node sends to ask the Controller for the data at one Address.
_Avoid_: query, poll

**Reply**:
The Frame the Controller sends back for a Read request, carrying the Address and its data.
_Avoid_: response, answer

**Command byte**:
The second byte of a Frame: 0x81 in a Read request, 0x06 in a Reply.
_Avoid_: ACK byte, opcode

**Length byte**:
The third byte of a Frame: the number of Address and data bytes that follow.
_Avoid_: message type, type byte

**Checksum**:
The last byte of a Frame: the low byte of the sum of every byte from the Command byte up to the Checksum.
_Avoid_: CRC

**Address**:
The 16-bit number a Read request asks for; either a single Value or a Bank.
_Avoid_: id, sensor id, register

**Bank**:
An Address whose Reply carries 31 data bytes holding many settings at fixed offsets.
_Avoid_: block, page

**Status word**:
The 16-bit Value at Address 0x2D whose bits report what the heat pump is running.
_Avoid_: status variable, Tila Muuttuja

**Status bit**:
One bit of the Status word, published as on or off (for example the compressor or the electric heater).
_Avoid_: status flag, bitmask

## Values

**Value**:
One quantity the Component publishes as one Home Assistant entity, such as a temperature, a valve position, an hour counter, a Bank setting or a Status bit.
_Avoid_: sensor (an ESPHome entity type), parameter

**Register map**:
The single table that lists every Value with its config key, Address or Bank offset, Decode rule and entity metadata.
_Avoid_: value table, sensor table

**Decode rule**:
How a Value's bytes become a number or a boolean: byte width, signedness, divisor and Status bit mask.
_Avoid_: format, conversion

**Poll group**:
Which reading cycle an Address belongs to: Values, read every value interval, or Banks, read every bank interval.
_Avoid_: priority, queue

## Parts of the Component

**Frame codec**:
The part of the Component that owns the wire format: building Read requests and finding checksum-verified Frames in received bytes.
_Avoid_: parser, protocol handler

**Poll scheduler**:
The part of the Component that decides which Address to request next, with one Read request in flight at a time.
_Avoid_: poller, request queue
