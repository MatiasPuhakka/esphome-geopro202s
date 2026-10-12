"""The Register map: every config key the component accepts, one row per key.

`__init__` walks VALUES to build CONFIG_SCHEMA and to register each configured
key with the hub. Add a key by adding a row here; the hub needs no change.

The comment above each row says where its meaning comes from: the Käsikirja
(`manuals/Geopro 202S Käsikirja.pdf`) label and page, and for a measurement its
M-number (CONTEXT.md lists them). Pages are PDF page indexes, as in
docs/controller.md. "Observed" marks what comes from the Node or the owner
rather than the manual, with the issue or log it comes from. The bottom of this
file lists the Bank bytes no row reads yet.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from esphome.const import (
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_RUNNING,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_CELSIUS,
    UNIT_HOUR,
    UNIT_MINUTE,
    UNIT_PERCENT,
    UNIT_SECOND,
)


class EntityKind(Enum):
    """The ESPHome platform a Value publishes on. Home Assistant keys each entity on its
    platform and name, so changing a row's entity kind orphans its entity
    (docs/adr/0004). Each value is the platform's ESPHome name, which AUTO_LOAD and the
    entity contract use; __init__.py's _PLATFORMS gives each kind its schema and entity
    constructor."""

    SENSOR = "sensor"
    BINARY_SENSOR = "binary_sensor"


class PollGroup(Enum):
    """Which cycle reads a row's address; it sets cadence only. Mirrors PollGroup in poll_scheduler.h."""

    VALUE = "VALUE"  # every value_interval
    BANK = "BANK"  # every bank_interval


# Data bytes in a Bank's Reply. Mirrors BANK_DATA_LENGTH in value_decoder.h.
BANK_DATA_LENGTH = 31


class AddressKind(Enum):
    """What a row's address holds, which sets its Reply's data length.

    Mirrors AddressKind in value_decoder.h.
    """

    SINGLE_VALUE = "SINGLE_VALUE"  # the data ends where the value ends
    BANK = "BANK"  # BANK_DATA_LENGTH bytes of settings


@dataclass(frozen=True)
class DecodeRule:
    """How the hub turns a value's bytes into a number. Mirrors DecodeRule in value_decoder.h."""

    width: int  # bytes, big-endian
    signed: bool
    divisor: int = 1  # the raw number is divided by this
    mask: int = 0  # when set, the value is 1 if any of these bits is set and 0 if none is

    def __post_init__(self):
        assert self.width in (1, 2), "width must be 1 or 2 bytes"
        assert self.divisor > 0, "divisor must be positive"
        assert 0 <= self.mask < 1 << (8 * self.width), "mask must fit the value's width"


S8 = DecodeRule(width=1, signed=True)
U8 = DecodeRule(width=1, signed=False)
U16 = DecodeRule(width=2, signed=False)
CENTI_S16 = DecodeRule(width=2, signed=True, divisor=100)


def status_bit(mask):
    """One bit of the 16-bit status word, decoded as 1 when set and 0 when not."""
    return DecodeRule(width=2, signed=False, mask=mask)


@dataclass(frozen=True)
class Value:
    # The config key and the entity kind. Home Assistant knows the entity by its kind
    # and its name in node.yaml.
    key: str
    entity_kind: EntityKind
    # The address read for this value (for settings, the bank), where the value
    # starts in the reply's data, how to decode it, what the address holds and
    # which cycle reads it. Rows may share an address; check_rows() says how.
    address: int
    decode: DecodeRule
    offset: int = 0
    address_kind: AddressKind = AddressKind.SINGLE_VALUE
    group: PollGroup = PollGroup.VALUE
    # Entity options. None leaves the ESPHome default in place.
    unit: Optional[str] = None
    device_class: Optional[str] = None
    state_class: Optional[str] = None
    accuracy: Optional[int] = None
    icon: Optional[str] = None

    def __post_init__(self):
        assert isinstance(self.entity_kind, EntityKind), f"{self.key}: entity_kind must be an EntityKind"

    @property
    def end(self):
        """Where the value ends in the Reply's data: its offset plus its width."""
        return self.offset + self.decode.width

    @property
    def reply_length(self):
        """Data bytes in the Reply from this row's address."""
        if self.address_kind is AddressKind.BANK:
            return BANK_DATA_LENGTH
        return self.end

    @property
    def schema_options(self):
        """Keyword arguments for the entity kind's schema, such as sensor_schema()."""
        options = {
            "unit_of_measurement": self.unit,
            "device_class": self.device_class,
            "state_class": self.state_class,
            "accuracy_decimals": self.accuracy,
            "icon": self.icon,
        }
        return {name: option for name, option in options.items() if option is not None}


def _temperature(key, address):
    return Value(
        key, EntityKind.SENSOR, address, CENTI_S16,
        unit=UNIT_CELSIUS, device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT, accuracy=2, icon="mdi:thermometer",
    )


def _valve(key, address):
    # Only 0-10 V / 2-10 V motors report a position (Käsikirja pp. 27, 28); a
    # 3-point motor reads 0 %.
    return Value(
        key, EntityKind.SENSOR, address, U8,
        unit=UNIT_PERCENT, state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon="mdi:valve",
    )


def _hours(key, address):
    return Value(
        key, EntityKind.SENSOR, address, U16,
        unit=UNIT_HOUR, device_class=DEVICE_CLASS_DURATION,
        state_class=STATE_CLASS_TOTAL_INCREASING, accuracy=0, icon="mdi:clock",
    )


STATUS_WORD = Value("status_word", EntityKind.SENSOR, 0x2D, U16, state_class=STATE_CLASS_MEASUREMENT, accuracy=0)


def _status_bit(key, mask, icon):
    return Value(
        key, EntityKind.BINARY_SENSOR, STATUS_WORD.address, status_bit(mask), offset=STATUS_WORD.offset,
        device_class=DEVICE_CLASS_RUNNING, icon=icon,
    )


# Bank settings, one helper per type of setting: each reads the byte at `offset` in
# `bank` and sets its own presentation. All four publish with state class measurement
# and no decimals today; #26 decides whether that changes.
def _bank_setting(key, bank, offset, decode, **entity_options):
    return Value(
        key, EntityKind.SENSOR, bank, decode,
        offset=offset, address_kind=AddressKind.BANK, group=PollGroup.BANK, **entity_options,
    )


_TEMP_ICON = "mdi:temperature-celsius"


def _bank_temperature(key, bank, offset, icon=_TEMP_ICON, decode=S8):
    return _bank_setting(
        key, bank, offset, decode,
        unit=UNIT_CELSIUS, device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon=icon,
    )


def _bank_duration(key, bank, offset, unit, decode=S8):
    return _bank_setting(
        key, bank, offset, decode,
        unit=unit, device_class=DEVICE_CLASS_DURATION,
        state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon="mdi:clock",
    )


def _bank_percentage(key, bank, offset, icon):
    return _bank_setting(
        key, bank, offset, S8,
        unit=UNIT_PERCENT, state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon=icon,
    )


def _bank_mode(key, bank, offset):
    """A setting whose number picks one of a menu's choices."""
    return _bank_setting(key, bank, offset, S8, state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon="mdi:gauge")


VALUES = (
    # Measurements, from the Mittaukset display and its table (p. 10)
    # M1 Ulkolämpö, p. 10
    _temperature("outside_temp", 0x12),
    # M3 L1 Huone, p. 10
    _temperature("l1_room", 0x15),
    # M2 L1 Menovesi, p. 10
    _temperature("l1_supply", 0x14),
    # M6 Mittaus 6, p. 10
    _temperature("free_measurement", 0x1B),
    # M7 Yläosa tulo, p. 10
    _temperature("tank_top_in", 0x18),
    # M9 VaraajaYlä, p. 10
    _temperature("tank_top", 0x21),
    # M4 VaraajaKeski, p. 10
    _temperature("tank_middle", 0x17),
    # M10 VaraajaAla, p. 10
    _temperature("tank_bottom", 0x22),
    # M8 Maaliuos, p. 10
    _temperature("brine", 0x19),
    # Asento % of the L1 valve motor (Moott. L1), p. 27. Observed: this unit's L1
    # motor is 3-point and reads 0 % (#16).
    _valve("valve_l1", 0x31),
    # Asento % of the JV motor (Moott. JV), pp. 27, 28. Observed: this unit's JV
    # motor is 3-point and reads 0 % (#16).
    _valve("valve_dhw", 0x33),
    # Sähköv.Aika, p. 10; a counter, not an M-number. Observed: never published 0
    # in the Node logs of 2026-10-09 (#10).
    _hours("hours_eh", 0x3A),
    # Kompr.Aika, p. 10; a counter, not an M-number. Observed: never published 0
    # in the Node logs of 2026-10-09 (#10).
    _hours("hours_comp", 0x3B),
    # Not in the manual. Observed: 0xFE07 at idle (2026-10-09 trace). docs/controller.md,
    # Status word, has what each bit did.
    STATUS_WORD,

    # Status word bits. The manual doesn't describe the Status word, so every bit
    # here is observed.
    # Observed: the only bit that changed during compressor runs (Node logs from
    # 2026-10-07, not in the repo). Rele 2 switches the compressor (p. 39).
    _status_bit("compressor", 0x10, "mdi:engine"),
    # Observed: went on when S1 joined a compressor run (Node log from 2026-10-08,
    # not in the repo). Rele 1 switches the electric heater (p. 39).
    _status_bit("el_heater", 0x08, "mdi:radiator"),
    # digi1-digi3: p. 39 wires Dig 1 to the Lisälämpöpainike, Dig 2 to
    # Kompressorin ylivirtaussuoja and Dig 3 to Sähkövastuksen ylikuumenemissuoja,
    # and p. 20 lists their alarms. Observed: all three bits read on at idle
    # (Status word 0xFE07, 2026-10-09 trace), so which input each bit reports, and
    # whether on means a closed contact, is unverified.
    _status_bit("digi1", 0x01, "mdi:numeric-1-box"),
    _status_bit("digi2", 0x02, "mdi:numeric-2-box"),
    _status_bit("digi3", 0x04, "mdi:numeric-3-box"),

    # Bank 0x0C: heating circuit L1. Every row matched the Controller's display on
    # 2026-10-09 (#10).
    # L1 Käyrä -20, Säätökäyrien as, p. 6
    _bank_temperature("l1_minus20", 0x0C, 0, "mdi:chart-line"),
    # L1 Käyrä 0, p. 6
    _bank_temperature("l1_zero", 0x0C, 1, "mdi:chart-line"),
    # L1 Käyrä +20, p. 6
    _bank_temperature("l1_plus20", 0x0C, 2, "mdi:chart-line"),
    # Minimiraja, L1 Aset.arvot, p. 8
    _bank_temperature("l1_min_limit", 0x0C, 3),
    # Maksimiraja, L1 Aset.arvot, p. 8
    _bank_temperature("l1_max_limit", 0x0C, 4),
    # Yöalennus v. (Yöalennus vaikutus), L1 Aset.arvot, p. 8
    _bank_temperature("l1_night_effect", 0x0C, 5),
    # Syyskuivaus, L1 Aset.arvot, pp. 8, 9
    _bank_temperature("l1_autumn_dry", 0x0C, 14),
    # Ulkol.hidas (Ulkolämpötilan hidastus), huoltotila L1 Asetusarvot, p. 26
    _bank_duration("l1_out_temp_delay", 0x0C, 19, UNIT_HOUR),
    # Esikorotus h, huoltotila L1 Asetusarvot, p. 26: the duration (0-5 h), not the
    # user menu's Esikorotus amount in °C (p. 9). Observed: setting it from 0 h to
    # 1 h at the display moved the Value from 0 to 1 on 2026-10-09 (#10, #21).
    _bank_duration("l1_pre_increase", 0x0C, 23, UNIT_HOUR),

    # Bank 0x2C: L1 settings. Every row matched the Controller's display on
    # 2026-10-09 (#10).
    # Vent.kesäsulk (venttiilin kesäsulkeutuminen), L1 Aset.arvot, pp. 8, 9
    _bank_temperature("l1_summer_close", 0x2C, 8),

    # Bank 0x0B: ML settings, p. 21 (the Settings table in docs/controller.md).
    # Every row matched the Controller's display on 2026-10-09 (#10).
    # Var.ylä talvi, p. 21
    _bank_temperature("winter_temp", 0x0B, 1),
    # Var.ylä kesä, p. 21
    _bank_temperature("summer_temp", 0x0B, 2),
    # VaraajaAlaEro, pp. 21, 26
    _bank_temperature("bottom_diff", 0x0B, 3),
    # VaraajaYläEro, pp. 21, 26
    _bank_temperature("top_diff", 0x0B, 4),
    # VaraajaAlaMin, p. 21
    _bank_temperature("tank_min", 0x0B, 5),
    # SV_viiveaika, p. 21
    _bank_duration("delay_time", 0x0B, 6, UNIT_MINUTE),
    # VarYläEroSv, p. 21
    _bank_temperature("top_eh_diff", 0x0B, 7),
    # Lisälämmitys, p. 21
    _bank_temperature("extra_heating", 0x0B, 8),
    # Lisäläm.aika, p. 21
    _bank_duration("extra_time", 0x0B, 9, UNIT_HOUR),
    # ML Ohjaustapa, the ML Ohjaustavat screen, pp. 13, 21: Kompr.+sähköv.,
    # Kompressori or Sähkövastus, with no codes given. The codes follow the menu
    # order: 0 Kompr.+sähköv., 1 Kompressori, 2 Sähkövastus. The owner confirmed
    # them on 2026-10-11; 0 also matched the display in #10.
    _bank_mode("hp_mode", 0x0B, 10),
    # Maaliuos häl, pp. 21, 26
    _bank_temperature("brine_alert", 0x0B, 11),
    # JV Esiavaus, pp. 21, 26
    _bank_percentage("dhw_pre", 0x0B, 12, "mdi:valve"),
    # JV Esto, pp. 21, 26
    _bank_duration("dhw_lock", 0x0B, 13, UNIT_SECOND, decode=U8),
    # Kompr.esto, pp. 21, 23
    _bank_temperature("comp_lock", 0x0B, 14, "mdi:thermometer-off"),
)

# Bank bytes no row reads yet: each was non-zero in the 2026-10-09 trace
# (tests/traces/node-2026-10-09.log), and nobody has matched it to a setting.
# Every non-zero byte of Bank 0x0B has a row. Each byte is shown in hex and
# unsigned, with the signed reading after a slash when the top bit is set.
#
#   Bank 0x0C, offset: byte
#     7: 0x28 40    8: 0x0A 10    9: 0x1E 30    10: 0x05 5     11: 0x0F 15
#     12: 0x46 70   13: 0xFA 250/-6             16: 0x64 100   18: 0x64 100
#     20: 0x05 5    22: 0x01 1    26: 0x4B 75
#
#   Bank 0x2C, offset: byte
#     5: 0x03 3     6: 0xE7 231/-25             9: 0x0B 11     10: 0x0A 10
#     12: 0x01 1    15: 0xF1 241/-15            16: 0x4B 75    19: 0x03 3
#     20: 0x84 132/-124                         24: 0x64 100   28: 0x06 6


def check_rows(values):
    """Raises ValueError, naming the rows, when `values` breaks one of these rules.

    Config keys are unique. A Bank row ends within the Bank's data, or it never
    decodes. Rows that share an address share one Reply, so they agree on its
    data length; a row that disagrees never decodes. They also agree on their
    Poll group, so the address is read in one cycle.
    """
    keys = [value.key for value in values]
    repeated = sorted({key for key in keys if keys.count(key) > 1})
    if repeated:
        raise ValueError(f"config keys must be unique: {', '.join(repeated)}")
    first_at = {}
    for value in values:
        if value.address_kind is AddressKind.BANK and value.end > BANK_DATA_LENGTH:
            raise ValueError(
                f"{value.key}: offset {value.offset} + {value.decode.width} byte(s) runs past "
                f"the {BANK_DATA_LENGTH} data bytes of Bank 0x{value.address:02X}"
            )
        first = first_at.setdefault(value.address, value)
        if value.reply_length != first.reply_length:
            raise ValueError(
                f"{first.key} and {value.key} share Address 0x{value.address:02X} but expect "
                f"{first.reply_length} and {value.reply_length} data bytes in its Reply"
            )
        if value.group is not first.group:
            raise ValueError(
                f"{first.key} and {value.key} share Address 0x{value.address:02X} but are in "
                f"Poll groups {first.group.value} and {value.group.value}"
            )


check_rows(VALUES)
