import logging
from pathlib import Path

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, sensor, text_sensor, uart
from esphome.const import CONF_ID, ENTITY_CATEGORY_DIAGNOSTIC
from esphome.core import HexInt

from .register_map import VALUES, EntityKind
from .revision import UNKNOWN, component_revision

_LOGGER = logging.getLogger(__name__)

# Each entity kind's ESPHome platform: the schema for its config and the coroutine that
# creates its entity. Codegen picks a platform here and nowhere else; publish_value() in
# geopro_202s_protocol.h is the C++ side. The README lists what adding a kind takes.
_PLATFORMS = {
    EntityKind.SENSOR: (sensor.sensor_schema, sensor.new_sensor),
    EntityKind.BINARY_SENSOR: (binary_sensor.binary_sensor_schema, binary_sensor.new_binary_sensor),
}
assert set(_PLATFORMS) == set(EntityKind), "every EntityKind needs a platform in _PLATFORMS"

DEPENDENCIES = ['uart']
# Every entity kind's platform, and text_sensor for the component revision.
AUTO_LOAD = sorted({entity_kind.value for entity_kind in EntityKind} | {'text_sensor'})

geopro_202s_ns = cg.esphome_ns.namespace('geopro_202s')
Geopro202sComponent = geopro_202s_ns.class_('Geopro202sComponent', cg.Component, uart.UARTDevice)
DecodeRuleStruct = geopro_202s_ns.struct('DecodeRule')
PollGroup = geopro_202s_ns.enum('PollGroup', is_class=True)
AddressKind = geopro_202s_ns.enum('AddressKind', is_class=True)


def _decode_rule(rule):
    # A constructor call, not designated initializers: those are standard only
    # from C++20, and ESPHome's Arduino ESP32 builds use C++11.
    return DecodeRuleStruct(rule.width, rule.signed, rule.divisor, HexInt(rule.mask))


CONF_VALUE_INTERVAL = 'value_interval'
CONF_BANK_INTERVAL = 'bank_interval'
CONF_COMPONENT_REVISION = 'component_revision'

# A zero interval would poll without pause, so require more than zero.
_poll_interval = cv.All(cv.positive_not_null_time_period, cv.positive_time_period_milliseconds)


def _entity_schema(value):
    schema, _ = _PLATFORMS[value.entity_kind]
    return schema(**value.schema_options)


CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(Geopro202sComponent),
        cv.Optional(CONF_VALUE_INTERVAL, default='10s'): _poll_interval,
        cv.Optional(CONF_BANK_INTERVAL, default='60s'): _poll_interval,
        cv.Optional(CONF_COMPONENT_REVISION): text_sensor.text_sensor_schema(
            entity_category=ENTITY_CATEGORY_DIAGNOSTIC, icon='mdi:source-commit'),
        **{cv.Optional(value.key): _entity_schema(value) for value in VALUES},
    })
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)

# The Controller's bus runs at 4800 baud, 8N1, and the hub both sends and receives.
FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema(
    'geopro_202s',
    baud_rate=4800,
    require_tx=True,
    require_rx=True,
    data_bits=8,
    parity='NONE',
    stop_bits=1,
)


async def to_code(config):
    hub = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(hub, config)
    await uart.register_uart_device(hub, config)
    cg.add(hub.set_value_interval(config[CONF_VALUE_INTERVAL]))
    cg.add(hub.set_bank_interval(config[CONF_BANK_INTERVAL]))

    revision = component_revision(Path(__file__).resolve().parent)
    if revision == UNKNOWN:
        _LOGGER.warning('Could not read the geopro_202s git revision; the firmware reports "%s"', UNKNOWN)
    cg.add(hub.set_component_revision(revision))
    if CONF_COMPONENT_REVISION in config:
        entity = await text_sensor.new_text_sensor(config[CONF_COMPONENT_REVISION])
        cg.add(hub.set_component_revision_text_sensor(entity))

    for value in VALUES:
        if value.key not in config:
            continue
        _, new_entity = _PLATFORMS[value.entity_kind]
        entity = await new_entity(config[value.key])
        group = getattr(PollGroup, value.group.value)
        address_kind = getattr(AddressKind, value.address_kind.value)
        cg.add(hub.register_value(
            group, address_kind, HexInt(value.address), value.offset, _decode_rule(value.decode), entity))
