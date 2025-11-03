import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_DURATION,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_MINUTE,
)
from . import GEOPRO_202S_COMPONENT_SCHEMA, Geopro202sComponent

DEPENDENCIES = ['uart']

# Bank 0x0C - Heating Circuit Settings
CONF_L1_MINUS20 = "l1_minus20"
CONF_L1_ZERO = "l1_zero"
CONF_L1_PLUS20 = "l1_plus20"
CONF_L1_NIGHT_EFFECT = "l1_night_effect"
CONF_L1_MIN_LIMIT = "l1_min_limit"
CONF_L1_MAX_LIMIT = "l1_max_limit"
CONF_L1_AUTUMN_DRY = "l1_autumn_dry"
CONF_L1_OUT_TEMP_DELAY = "l1_out_temp_delay"
CONF_L1_PRE_INCREASE = "l1_pre_increase"

# Bank 0x2C - L1 Settings
CONF_L1_SUMMER_CLOSE = "l1_summer_close"

# Bank 0x0B - Heat Pump Settings
CONF_HP_MODE = "hp_mode"
CONF_TANK_MIN = "tank_min"
CONF_DELAY_TIME = "delay_time"
CONF_SUMMER_TEMP = "summer_temp"
CONF_WINTER_TEMP = "winter_temp"
CONF_EXTRA_HEATING = "extra_heating"
CONF_EXTRA_TIME = "extra_time"
CONF_COMP_LOCK = "comp_lock"
CONF_TOP_EH_DIFF = "top_eh_diff"
CONF_BOTTOM_DIFF = "bottom_diff"
CONF_TOP_DIFF = "top_diff"
CONF_DHW_PRE = "dhw_pre"
CONF_DHW_LOCK = "dhw_lock"
CONF_BRINE_ALERT = "brine_alert"

# Bank sensor configuration: (bank_id, offset, default_name, unit, device_class, icon)
BANK_SENSORS = {
    # Bank 0x0C
    CONF_L1_MINUS20: (0x0C, 0, "L1 -20°C", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:chart-line"),
    CONF_L1_ZERO: (0x0C, 1, "L1 0°C", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:chart-line"),
    CONF_L1_PLUS20: (0x0C, 2, "L1 +20°C", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:chart-line"),
    CONF_L1_MIN_LIMIT: (0x0C, 3, "L1 Minimiraja", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_L1_MAX_LIMIT: (0x0C, 4, "L1 Maksimiraja", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_L1_NIGHT_EFFECT: (0x0C, 5, "L1 Yöalennus vaikutus", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_L1_AUTUMN_DRY: (0x0C, 14, "L1 Syyskuivaus", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_L1_OUT_TEMP_DELAY: (0x0C, 19, "L1 Ulkolämpötilan hidastus", UNIT_MINUTE, DEVICE_CLASS_DURATION, "mdi:clock"),
    CONF_L1_PRE_INCREASE: (0x0C, 23, "L1 Esikorotus", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),

    # Bank 0x2C
    CONF_L1_SUMMER_CLOSE: (0x2C, 8, "L1 venttiilin kesäsulku", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),

    # Bank 0x0B
    CONF_WINTER_TEMP: (0x0B, 1, "ML VarYlä Talvi", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_SUMMER_TEMP: (0x0B, 2, "ML VarYlä Kesä", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_BOTTOM_DIFF: (0x0B, 3, "ML VaraajaAlaEro", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_TOP_DIFF: (0x0B, 4, "ML VaraajaYläEro", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_TANK_MIN: (0x0B, 5, "ML VaraajaAlaMin", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_DELAY_TIME: (0x0B, 6, "ML SV_viiveaika", UNIT_MINUTE, DEVICE_CLASS_DURATION, "mdi:clock"),
    CONF_TOP_EH_DIFF: (0x0B, 7, "ML VarYlaEroSV", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_EXTRA_HEATING: (0x0B, 8, "ML Lisälämmitys", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_EXTRA_TIME: (0x0B, 9, "ML Lisälämmitys aika", UNIT_MINUTE, DEVICE_CLASS_DURATION, "mdi:clock"),
    CONF_HP_MODE: (0x0B, 10, "ML Ohjaustapa", None, None, "mdi:gauge"),
    CONF_BRINE_ALERT: (0x0B, 11, "ML Maaliuos hälytys", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_DHW_PRE: (0x0B, 12, "ML JV esiavaus", UNIT_CELSIUS, DEVICE_CLASS_TEMPERATURE, "mdi:temperature-celsius"),
    CONF_DHW_LOCK: (0x0B, 13, "ML JV Esto", UNIT_MINUTE, DEVICE_CLASS_DURATION, "mdi:clock"),
    CONF_COMP_LOCK: (0x0B, 14, "ML Kompuran esto", UNIT_MINUTE, DEVICE_CLASS_DURATION, "mdi:clock"),
}

# Build schema dict for bank sensors, handling None values for unit/device_class
bank_sensor_schemas = {}
for key, info in BANK_SENSORS.items():
    schema_kwargs = {
        "state_class": STATE_CLASS_MEASUREMENT,
        "accuracy_decimals": 0,
        "icon": info[5],
    }
    # Only add unit_of_measurement if it's not None
    if info[3] is not None:
        schema_kwargs["unit_of_measurement"] = info[3]
    # Only add device_class if it's not None
    if info[4] is not None:
        schema_kwargs["device_class"] = info[4]
    bank_sensor_schemas[cv.Optional(key)] = sensor.sensor_schema(**schema_kwargs)

CONFIG_SCHEMA = GEOPRO_202S_COMPONENT_SCHEMA.extend(bank_sensor_schemas)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ID])

    for key, (bank_id, offset, default_name, unit, device_class, icon) in BANK_SENSORS.items():
        if key in config:
            sens = await sensor.new_sensor(config[key])
            cg.add(hub.register_bank_sensor(bank_id, offset, sens))

