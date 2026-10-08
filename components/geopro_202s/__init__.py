import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, sensor, uart
from esphome.const import CONF_ID

from .value_table import VALUES

DEPENDENCIES = ['uart']
AUTO_LOAD = ['sensor', 'binary_sensor']

geopro_202s_ns = cg.esphome_ns.namespace('geopro_202s')
Geopro202sComponent = geopro_202s_ns.class_('Geopro202sComponent', cg.Component, uart.UARTDevice)

CONF_VALUE_INTERVAL = 'value_interval'
CONF_BANK_INTERVAL = 'bank_interval'

# A zero interval would poll without pause, so require more than zero.
_poll_interval = cv.All(cv.positive_not_null_time_period, cv.positive_time_period_milliseconds)


def _entity_schema(value):
    if value.kind.is_binary:
        return binary_sensor.binary_sensor_schema(**value.schema_options)
    return sensor.sensor_schema(**value.schema_options)


CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(Geopro202sComponent),
        cv.Optional(CONF_VALUE_INTERVAL, default='10s'): _poll_interval,
        cv.Optional(CONF_BANK_INTERVAL, default='60s'): _poll_interval,
        **{cv.Optional(value.key): _entity_schema(value) for value in VALUES},
    })
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    hub = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(hub, config)
    await uart.register_uart_device(hub, config)
    cg.add(hub.set_value_interval(config[CONF_VALUE_INTERVAL]))
    cg.add(hub.set_bank_interval(config[CONF_BANK_INTERVAL]))

    for value in VALUES:
        if value.key not in config:
            continue
        if value.kind.is_binary:
            entity = await binary_sensor.new_binary_sensor(config[value.key])
        else:
            entity = await sensor.new_sensor(config[value.key])
        register = getattr(hub, value.kind.register_method)
        cg.add(register(*value.register_args, entity))
