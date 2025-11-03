import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

DEPENDENCIES = ['uart']
AUTO_LOAD = ['sensor', 'binary_sensor', 'bank_sensor']

# Component namespace
geopro_202s_ns = cg.esphome_ns.namespace('geopro_202s')
Geopro202sComponent = geopro_202s_ns.class_('Geopro202sComponent', cg.Component, uart.UARTDevice)

# Configuration schema
CONF_GEOPRO_202S_ID = 'geopro_202s_id'

GEOPRO_202S_COMPONENT_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Geopro202sComponent),
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

CONFIG_SCHEMA = GEOPRO_202S_COMPONENT_SCHEMA

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)