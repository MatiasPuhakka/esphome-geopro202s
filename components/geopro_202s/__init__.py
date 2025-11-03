import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

DEPENDENCIES = ['uart']
AUTO_LOAD = ['sensor', 'binary_sensor']

# Component namespace
geopro_202s_ns = cg.esphome_ns.namespace('geopro_202s')
Geopro202sComponent = geopro_202s_ns.class_('Geopro202sComponent', cg.Component, uart.UARTDevice)

# Configuration schema
CONF_GEOPRO_202S_ID = 'geopro_202s_id'

GEOPRO_202S_COMPONENT_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(Geopro202sComponent),
}).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

# Import and merge schemas from sub-modules
from . import sensor
from . import binary_sensor
from . import bank_sensor

# Merge all schemas - each module extends GEOPRO_202S_COMPONENT_SCHEMA,
# so we need to start from base and extend with each module's additions
CONFIG_SCHEMA = GEOPRO_202S_COMPONENT_SCHEMA

# Each module's CONFIG_SCHEMA already includes the base, so we need to extract just the additions
# We'll merge by extending with each module's schema which will add their options
CONFIG_SCHEMA = sensor.CONFIG_SCHEMA
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(binary_sensor.CONFIG_SCHEMA)
CONFIG_SCHEMA = CONFIG_SCHEMA.extend(bank_sensor.CONFIG_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    # Call to_code functions from sub-modules to register sensors
    await sensor.to_code(config)
    await binary_sensor.to_code(config)
    await bank_sensor.to_code(config)