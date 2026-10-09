# Geopro 202S integration

An ESPHome component that reads values from an Ouman Geopro 202S heat pump controller over its serial bus and publishes them to Home Assistant. It only reads; it never changes a setting.

## Hardware

**Controller**:
The Ouman Geopro 202S that runs the heat pump and answers on the serial bus.
_Avoid_: heat pump (the machine the Controller runs), device

**Node**:
The ESP32 running ESPHome that talks to the Controller and to Home Assistant.
_Avoid_: device, ESP

**Component**:
The `geopro_202s` ESPHome external component that the Node runs.
_Avoid_: module, YAML protocol copy (the older implementation in `geopro.yaml`)

## Wire protocol

**Frame**:
One unit on the serial bus: start byte 0x02, command byte, Length byte, a 16-bit Address followed by data, and a Checksum.
_Avoid_: message, packet

**Read request**:
A Frame the Node sends to ask the Controller for the data at one Address.
_Avoid_: query, poll

**Reply**:
The Frame the Controller sends back for a Read request, carrying the Address and its data.
_Avoid_: response, answer

**Length byte**:
The third byte of a Frame: the number of Address and data bytes that follow.
_Avoid_: message type, type byte

**Checksum**:
The last byte of a Frame: the low byte of the sum of every byte from the command byte up to the Checksum.
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
