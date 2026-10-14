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

These terms use the Finnish labels from the Käsikirja, transcribed in [`manuals/kasikirja.md`](manuals/kasikirja.md). `docs/controller.md` has the rules that use them, with page numbers.

**M-number**:
One of the Controller's measurement inputs, M1 to M11 (Mittaus 1–11, terminals Mitt.1–Mitt.11; Käsikirja pp. [10](manuals/kasikirja.md#s10), [39](manuals/kasikirja.md#s39)). The manual also calls the valve-motor outputs M1–M3 ([p. 28](manuals/kasikirja.md#s28)); this glossary calls those Moott. L1, Moott. L2 and Moott. JV. The Register map reads these Addresses:

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
Which heat sources the ML circuit may use: Kompr.+sähköv. (0), Kompressori (1) or Sähkövastus (2). The manual's menu is ML Ohjaustavat ([p. 21](manuals/kasikirja.md#s21)); this is its singular.
_Avoid_: heat pump mode

**Run**:
One stretch of a Status bit being on. A compressor run is the Controller calling for the compressor; `tools/runs.py` finds them, and `tools/cycles.py` lists them with the idle time before each.
_Avoid_: on-cycle

**Start**:
The compressor beginning to draw current, seen as the lowest Shelly phase current rising above 4 A. A run without breaks has one start.
_Avoid_: run (a run can hold several starts)

**Break**:
A stretch inside a run where the compressor drew no current while the Status bit stayed on, as in the chatter of 2026-10-07 to 2026-10-09.
_Avoid_: trip, stop

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

**False start**:
A 0x02 on the bus that doesn't begin a Frame, from line noise or from the tail of a Reply the Node caught partway, as at boot. Since 0x02 is never escaped, it looks like a start byte until the bytes after it fail to make a Frame.
_Avoid_: stale frame (the bytes a false start leaves held)

**Bus error**:
Something the Session counts: a Frame whose Checksum fails, a received byte that ends up in no Frame (including the bytes of a False start dropped after a silence), a timeout, or a Reply that decodes no Values. After a timeout the Poll scheduler sends the Read request once more (a retry) or drops it until its next cycle (a give-up), so every timeout is one or the other. A Reply that decodes nothing still answers its Read request. A Frame with a Command byte other than 0x06, such as the Node's own Read request echoed back, is not a bus error. The Hub logs the counts at WARN at most once per bank interval, and only when one is non-zero.
_Avoid_: comms error, fault

**Address**:
The 16-bit number a Read request asks for; either a single Value or a Bank.
_Avoid_: id, sensor id, register

**Missed cycle**:
A cycle of an Address's Poll group that ended with the Poll scheduler giving up on it, so the Node got no Reply for the Address. Each cycle can miss an Address once. With the Controller silent a cycle runs past its interval, since each give-up costs two Reply timeouts, so the next one starts when the queue empties.
_Avoid_: miss, missed poll, dropped read

**Stale**:
An Address with two Missed cycles in a row and no Reply for it in between. The Session reports every entry registered at it, once, and the Hub shows those entries as unknown in Home Assistant until the next decoded Reply. A Reply that decodes nothing still ends the run of Missed cycles. The reason for two cycles is in `session.h`.
_Avoid_: unavailable (what Home Assistant shows when the Node itself is gone), timed out

**Address kind**:
Whether an Address holds a single Value or a Bank. It sets the Reply's data length: 31 bytes for a Bank, and for a single Value, its offset plus its byte width.
_Avoid_: address type

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
The single table that lists every Value with its config key, Entity kind, Address or Bank offset, Address kind, Decode rule, Poll group and entity metadata. It checks its rows when it loads.
_Avoid_: value table, sensor table

**Decode rule**:
How a Value's bytes become a number: byte width, signedness, divisor and Status bit mask. A Status bit decodes to 1 or 0.
_Avoid_: format, conversion

**Entity kind**:
The ESPHome platform a Value publishes on: sensor or binary sensor. Each Register map row names its own. Home Assistant knows an entity by its kind and name, so changing a kind orphans the entity's history ([ADR 0004](docs/adr/0004-entity-ids-stay-stable.md)).
_Avoid_: platform type, entity type

**Poll group**:
Which reading cycle reads an Address: the value cycle, every value interval, or the bank cycle, every bank interval. It sets cadence only. Banks are in the bank cycle by default, but a Bank read in the value cycle decodes the same.
_Avoid_: priority, queue

## Parts of the Component

**Frame codec**:
The part of the Component that owns the wire format: building Read requests and finding checksum-verified Frames in received bytes.
_Avoid_: parser, protocol handler

**Poll scheduler**:
The part of the Component that decides which Address to request next, with one Read request in flight at a time.
_Avoid_: poller, request queue

**Session**:
The part of the Component that turns received bytes and the time into Read requests and decoded Values. It composes the Frame codec, Poll scheduler and value decoder, owns the Register map entries, decides what counts as a Reply and when a request is done, counts Bus errors, and decides when an Address is Stale. It has no clock and no ESPHome includes. Each decoded Value carries the id of its entry, and a Stale Address is reported as the ids of its entries.
_Avoid_: driver, transport

**Hub**:
The ESPHome-facing class (`Geopro202sComponent`). It moves UART bytes and the time into the Session, sends the Read requests the Session returns, publishes the Values it hands back, and makes the entities of the entries it reports Stale unknown. A Missed cycle arrives with no bytes, so the Hub publishes what the Session's request path returns as well as what its feed does. It is the only code that touches the UART or an entity.
_Avoid_: adapter, controller (that is the Ouman unit)

