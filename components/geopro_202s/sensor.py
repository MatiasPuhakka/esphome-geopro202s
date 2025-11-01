import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_DURATION,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_CELSIUS,
    UNIT_PERCENT,
    UNIT_HOUR,
)
from . import GEOPRO_202S_COMPONENT_SCHEMA, Geopro202sComponent

DEPENDENCIES = ['uart']

# Configuration entries for each sensor type
CONF_OUTSIDE_TEMP = "outside_temp"
CONF_L1_ROOM = "l1_room"
CONF_L1_SUPPLY = "l1_supply"
CONF_FREE_MEASUREMENT = "free_measurement"
CONF_TANK_TOP_IN = "tank_top_in"
CONF_TANK_TOP = "tank_top"
CONF_TANK_MID = "tank_middle"
CONF_TANK_BOTTOM = "tank_bottom"
CONF_BRINE = "brine"
CONF_VALVE_L1 = "valve_l1"
CONF_VALVE_DHW = "valve_dhw"
CONF_HOURS_EH = "hours_eh"
CONF_HOURS_COMP = "hours_comp"
CONF_STATUS_WORD = "status_word"

# TEMPERATURE_SENSORS = {
#     CONF_L1_SUPPLY: {
#         "id": 0x14,
#         "name": "L1 Menovesi",
#         "icon": "mdi:thermometer",
#         "entity_category": None,  # Shows in main UI
#         "enabled_default": True,
#         "device_class": DEVICE_CLASS_TEMPERATURE,
#         "description": {
#             "fi": "Menoveden lämpötila säätöpiirissä L1",
#             "range": "0-130°C"
#         }
#     },

# Map each temperature sensor to its hex ID and default name
TEMPERATURE_SENSORS = {
    CONF_OUTSIDE_TEMP: (0x12, "Ulkolämpötila"),
    CONF_L1_ROOM: (0x15, "L1 Huone"),
    CONF_L1_SUPPLY: (0x14, "L1 Menovesi"),
    CONF_FREE_MEASUREMENT: (0x1B, "Vapaa mittaus"),
    CONF_TANK_TOP_IN: (0x18, "Varaaja ylä tulo"),
    CONF_TANK_TOP: (0x21, "Varaaja ylä"),
    CONF_TANK_MID: (0x17, "Varaaja keski"),
    CONF_TANK_BOTTOM: (0x22, "Varaaja ala"),
    CONF_BRINE: (0x19, "Maaliuos"),
}

# Map valve sensors to their hex IDs and default names
VALVE_SENSORS = {
    CONF_VALVE_L1: (0x31, "L1 Venttiili"),
    CONF_VALVE_DHW: (0x33, "JV Venttiili"),
}

# Map hour counters to their hex IDs and default names
HOUR_SENSORS = {
    CONF_HOURS_EH: (0x3A, "Sähkövastus tunnit"),
    CONF_HOURS_COMP: (0x3B, "Kompressori tunnit"),
}

# Create the configuration schema
CONFIG_SCHEMA = GEOPRO_202S_COMPONENT_SCHEMA.extend({
    # Temperature sensors
    cv.Optional(key): sensor.sensor_schema(
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=UNIT_CELSIUS,
        accuracy_decimals=2,
    ) for key in TEMPERATURE_SENSORS.keys()
}).extend({
    # Valve position sensors
    cv.Optional(key): sensor.sensor_schema(
        state_class=STATE_CLASS_MEASUREMENT,
        unit_of_measurement=UNIT_PERCENT,
        accuracy_decimals=0,
    ) for key in VALVE_SENSORS.keys()
}).extend({
    # Hour counters
    cv.Optional(key): sensor.sensor_schema(
        device_class=DEVICE_CLASS_DURATION,
        state_class=STATE_CLASS_TOTAL_INCREASING,
        unit_of_measurement=UNIT_HOUR,
        accuracy_decimals=0,
    ) for key in HOUR_SENSORS.keys()
}).extend({
    # Status word
    cv.Optional(CONF_STATUS_WORD): sensor.sensor_schema(
        state_class=STATE_CLASS_MEASUREMENT,
        accuracy_decimals=0,
    ),
})

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ID])

    # Register temperature sensors
    for key, (sensor_id, default_name) in TEMPERATURE_SENSORS.items():
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(hub.register_temp_sensor(sensor_id, sens))

    # Register valve position sensors
    for key, (sensor_id, default_name) in VALVE_SENSORS.items():
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(hub.register_valve_sensor(sensor_id, sens))

    # Register hour counter sensors
    for key, (sensor_id, default_name) in HOUR_SENSORS.items():
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(hub.register_hour_sensor(sensor_id, sens))

    # Register status word sensor
    if CONF_STATUS_WORD in config:
        sens = await sensor.new_sensor(config[CONF_STATUS_WORD])
        cg.add(hub.register_status_sensor(sens))