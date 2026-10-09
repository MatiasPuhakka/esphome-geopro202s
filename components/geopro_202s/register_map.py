"""The Register map: every config key the component accepts, one row per key.

`__init__` walks VALUES to build CONFIG_SCHEMA and to register each configured
key with the hub. Add a key by adding a row here; the hub needs no change.
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


class PollGroup(Enum):
    """Which cycle reads a row's address. Mirrors PollGroup in poll_scheduler.h."""

    VALUE = "VALUE"  # every value_interval
    BANK = "BANK"  # every bank_interval


@dataclass(frozen=True)
class DecodeRule:
    """How the hub turns a value's bytes into a number. Mirrors DecodeRule in value_decoder.h."""

    width: int  # bytes, big-endian
    signed: bool
    divisor: int = 1  # the raw number is divided by this
    mask: int = 0  # when set, the value is whether any of these bits is set

    def __post_init__(self):
        assert self.width in (1, 2), "width must be 1 or 2 bytes"
        assert self.divisor > 0, "divisor must be positive"
        assert 0 <= self.mask < 1 << (8 * self.width), "mask must fit the value's width"

    @property
    def is_binary(self):
        return self.mask != 0


S8 = DecodeRule(width=1, signed=True)
U8 = DecodeRule(width=1, signed=False)
U16 = DecodeRule(width=2, signed=False)
CENTI_S16 = DecodeRule(width=2, signed=True, divisor=100)


def status_bit(mask):
    """One bit of the 16-bit status word, published as a boolean."""
    return DecodeRule(width=2, signed=False, mask=mask)


@dataclass(frozen=True)
class Value:
    key: str
    # The address read for this value (for settings, the bank), where the value
    # starts in the reply's data, and how to decode it. Rows may share an address.
    address: int
    decode: DecodeRule
    offset: int = 0
    group: PollGroup = PollGroup.VALUE
    # Entity options. None leaves the ESPHome default in place.
    unit: Optional[str] = None
    device_class: Optional[str] = None
    state_class: Optional[str] = None
    accuracy: Optional[int] = None
    icon: Optional[str] = None

    @property
    def is_binary(self):
        """Binary sensor rather than sensor."""
        return self.decode.is_binary

    @property
    def schema_options(self):
        """Keyword arguments for sensor_schema() or binary_sensor_schema()."""
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
        key, address, CENTI_S16,
        unit=UNIT_CELSIUS, device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT, accuracy=2, icon="mdi:thermometer",
    )


def _valve(key, address):
    # Only 0-10 V / 2-10 V motors report a position; a 3-point motor reads 0 %.
    return Value(
        key, address, U8,
        unit=UNIT_PERCENT, state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon="mdi:valve",
    )


def _hours(key, address):
    return Value(
        key, address, U16,
        unit=UNIT_HOUR, device_class=DEVICE_CLASS_DURATION,
        state_class=STATE_CLASS_TOTAL_INCREASING, accuracy=0, icon="mdi:clock",
    )


STATUS_WORD = Value("status_word", 0x2D, U16, state_class=STATE_CLASS_MEASUREMENT, accuracy=0)


def _status_bit(key, mask, icon):
    return Value(
        key, STATUS_WORD.address, status_bit(mask), offset=STATUS_WORD.offset,
        device_class=DEVICE_CLASS_RUNNING, icon=icon,
    )


def _bank(key, bank, offset, unit, device_class, icon, decode=S8):
    return Value(
        key, bank, decode, offset=offset, group=PollGroup.BANK,
        unit=unit, device_class=device_class,
        state_class=STATE_CLASS_MEASUREMENT, accuracy=0, icon=icon,
    )


_TEMP_ICON = "mdi:temperature-celsius"

VALUES = (
    # Measurements
    _temperature("outside_temp", 0x12),
    _temperature("l1_room", 0x15),
    _temperature("l1_supply", 0x14),
    _temperature("free_measurement", 0x1B),
    _temperature("tank_top_in", 0x18),
    _temperature("tank_top", 0x21),
    _temperature("tank_middle", 0x17),
    _temperature("tank_bottom", 0x22),
    _temperature("brine", 0x19),
    _valve("valve_l1", 0x31),
    _valve("valve_dhw", 0x33),
    _hours("hours_eh", 0x3A),
    _hours("hours_comp", 0x3B),
    STATUS_WORD,

    # Status word bits
    _status_bit("compressor", 0x10, "mdi:engine"),
    _status_bit("el_heater", 0x08, "mdi:radiator"),
    _status_bit("digi1", 0x01, "mdi:numeric-1-box"),
    _status_bit("digi2", 0x02, "mdi:numeric-2-box"),
    _status_bit("digi3", 0x04, "mdi:numeric-3-box"),

    # Bank 0x0C: heating circuit L1
    _bank("l1_minus20", 0x0C, 0, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:chart-line"),
    _bank("l1_zero", 0x0C, 1, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:chart-line"),
    _bank("l1_plus20", 0x0C, 2, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:chart-line"),
    _bank("l1_min_limit", 0x0C, 3, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("l1_max_limit", 0x0C, 4, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("l1_night_effect", 0x0C, 5, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("l1_autumn_dry", 0x0C, 14, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("l1_out_temp_delay", 0x0C, 19, UNIT_HOUR, DEVICE_CLASS_DURATION, "mdi:clock"),
    _bank("l1_pre_increase", 0x0C, 23, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),

    # Bank 0x2C: L1 settings
    _bank("l1_summer_close", 0x2C, 8, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),

    # Bank 0x0B: heat pump settings
    _bank("winter_temp", 0x0B, 1, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("summer_temp", 0x0B, 2, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("bottom_diff", 0x0B, 3, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("top_diff", 0x0B, 4, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("tank_min", 0x0B, 5, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("delay_time", 0x0B, 6, UNIT_MINUTE, DEVICE_CLASS_DURATION, "mdi:clock"),
    _bank("top_eh_diff", 0x0B, 7, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("extra_heating", 0x0B, 8, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON),
    _bank("extra_time", 0x0B, 9, UNIT_HOUR, DEVICE_CLASS_DURATION, "mdi:clock"),
    _bank("hp_mode", 0x0B, 10, None, None, "mdi:gauge"),
    _bank("brine_alert", 0x0B, 11, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, _TEMP_ICON, decode=S8),
    _bank("dhw_pre", 0x0B, 12, UNIT_PERCENT, None, "mdi:valve"),
    _bank("dhw_lock", 0x0B, 13, UNIT_SECOND, DEVICE_CLASS_DURATION, "mdi:clock", decode=U8),
    _bank("comp_lock", 0x0B, 14, UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:thermometer-off"),
)

assert len({value.key for value in VALUES}) == len(VALUES), "config keys must be unique"
