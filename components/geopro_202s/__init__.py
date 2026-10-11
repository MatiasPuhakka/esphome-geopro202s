import logging
from pathlib import Path

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, sensor, text_sensor, uart
from esphome.const import CONF_ID, ENTITY_CATEGORY_DIAGNOSTIC
from esphome.core import HexInt

from .register_map import VALUES
from .revision import UNKNOWN, component_revision

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['uart']
AUTO_LOAD = ['sensor', 'binary_sensor', 'text_sensor']

geopro_202s_ns = cg.esphome_ns.namespace('geopro_202s')
Geopro202sComponent = geopro_202s_ns.class_('Geopro202sComponent', cg.Component, uart.UARTDevice)
DecodeRuleStruct = geopro_202s_ns.struct('DecodeRule')
PollGroup = geopro_202s_ns.enum('PollGroup', is_class=True)


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
    if value.is_binary:
        return binary_sensor.binary_sensor_schema(**value.schema_options)
    return sensor.sensor_schema(**value.schema_options)


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

    # This file's own checkout: the repository for a local build, ESPHome's clone
    # for a github:// source.
    revision = component_revision(Path(__file__).resolve().parent)
    if revision == UNKNOWN:
        _LOGGER.warning("Could not read the geopro_202s git revision; the firmware reports '%s'", UNKNOWN)
    cg.add(hub.set_component_revision(revision))
    if CONF_COMPONENT_REVISION in config:
        entity = await text_sensor.new_text_sensor(config[CONF_COMPONENT_REVISION])
        cg.add(hub.set_component_revision_text_sensor(entity))

    for value in VALUES:
        if value.key not in config:
            continue
        if value.is_binary:
            entity = await binary_sensor.new_binary_sensor(config[value.key])
        else:
            entity = await sensor.new_sensor(config[value.key])
        group = getattr(PollGroup, value.group.value)
        cg.add(hub.register_value(group, HexInt(value.address), value.offset, _decode_rule(value.decode), entity))
