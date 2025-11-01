import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_RUNNING,
)
from . import GEOPRO_202S_COMPONENT_SCHEMA, Geopro202sComponent

DEPENDENCIES = ['uart']

# Status word bit masks
BITMASK_DIGI1 = 0x01
BITMASK_DIGI2 = 0x02
BITMASK_DIGI3 = 0x04
BITMASK_EL_HEATER = 0x08
BITMASK_COMPRESSOR = 0x10

# Configuration entries for status bits
CONF_DIGI1 = "digi1"
CONF_DIGI2 = "digi2"
CONF_DIGI3 = "digi3"
CONF_EL_HEATER = "el_heater"
CONF_COMPRESSOR = "compressor"

# Status bits mapping with their default names and device classes
STATUS_BITS = {
    CONF_COMPRESSOR: {
        "name": "Kompressori",
        "mask": BITMASK_COMPRESSOR,
        "device_class": DEVICE_CLASS_RUNNING,
        "icon": "mdi:engine",
    },
    CONF_EL_HEATER: {
        "name": "Sähkövastus",
        "mask": BITMASK_EL_HEATER,
        "device_class": DEVICE_CLASS_RUNNING,
        "icon": "mdi:radiator",
    },
    # What are these?
    CONF_DIGI1: {
        "name": "Digi1",
        "mask": BITMASK_DIGI1,
        "device_class": DEVICE_CLASS_RUNNING,
        "icon": "mdi:numeric-1-box",
    },
    CONF_DIGI2: {
        "name": "Digi2",
        "mask": BITMASK_DIGI2,
        "device_class": DEVICE_CLASS_RUNNING,
        "icon": "mdi:numeric-2-box",
    },
    CONF_DIGI3: {
        "name": "Digi3",
        "mask": BITMASK_DIGI3,
        "device_class": DEVICE_CLASS_RUNNING,
        "icon": "mdi:numeric-3-box",
    },
}

# Create configuration schema
CONFIG_SCHEMA = GEOPRO_202S_COMPONENT_SCHEMA.extend({
    cv.Optional(key): binary_sensor.binary_sensor_schema(
        device_class=info["device_class"],
        icon=info["icon"],
    ) for key, info in STATUS_BITS.items()
})

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ID])

    for key, info in STATUS_BITS.items():
        if key in config:
            sens = await binary_sensor.new_binary_sensor(config[key])
            cg.add(hub.register_status_bit(info["mask"], sens))