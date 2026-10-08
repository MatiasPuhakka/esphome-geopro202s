import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor, sensor, uart
from esphome.const import CONF_ID

from .value_table import VALUES, DecodeRule

DEPENDENCIES = ['uart']
AUTO_LOAD = ['sensor', 'binary_sensor']

geopro_202s_ns = cg.esphome_ns.namespace('geopro_202s')
Geopro202sComponent = geopro_202s_ns.class_('Geopro202sComponent', cg.Component, uart.UARTDevice)
DecodeRuleStruct = geopro_202s_ns.struct('DecodeRule')


def _register_arg(arg):
    if isinstance(arg, DecodeRule):
        return cg.StructInitializer(DecodeRuleStruct, ('width', arg.width), ('is_signed', arg.signed))
    return arg


def _entity_schema(value):
    if value.kind.is_binary:
        return binary_sensor.binary_sensor_schema(**value.schema_options)
    return sensor.sensor_schema(**value.schema_options)


CONFIG_SCHEMA = (
    cv.Schema({
        cv.GenerateID(): cv.declare_id(Geopro202sComponent),
        **{cv.Optional(value.key): _entity_schema(value) for value in VALUES},
    })
    .extend(cv.COMPONENT_SCHEMA)
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    hub = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(hub, config)
    await uart.register_uart_device(hub, config)

    for value in VALUES:
        if value.key not in config:
            continue
        if value.kind.is_binary:
            entity = await binary_sensor.new_binary_sensor(config[value.key])
        else:
            entity = await sensor.new_sensor(config[value.key])
        register = getattr(hub, value.kind.register_method)
        cg.add(register(*(_register_arg(arg) for arg in value.register_args), entity))
