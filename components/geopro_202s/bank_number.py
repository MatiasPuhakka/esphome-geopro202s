# ⚠️ WARNING: Write functionality is UNVERIFIED - use with extreme caution! ⚠️
# The write protocol (command 0x82) is assumed based on read command pattern (0x81)
# but has NOT been verified or tested. See SAFETY_WARNING.md for details.

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import (
    CONF_ID,
    CONF_MIN_VALUE,
    CONF_MAX_VALUE,
    CONF_STEP,
    CONF_MODE,
    CONF_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_DURATION,
    UNIT_CELSIUS,
    UNIT_MINUTE,
)
from . import GEOPRO_202S_COMPONENT_SCHEMA, Geopro202sComponent

DEPENDENCIES = ['uart']

# Import bank sensor configs to reuse the same keys
from .bank_sensor import BANK_SENSORS

# Create configuration schema for number controls
# These mirror the bank sensors but as writable number controls
CONFIG_SCHEMA = GEOPRO_202S_COMPONENT_SCHEMA.extend({
    cv.Optional(key): number.number_schema(
        number.NUMBER_SCHEMA.extend({
            cv.Optional(CONF_MIN_VALUE, default=-50): cv.float_,
            cv.Optional(CONF_MAX_VALUE, default=100): cv.float_,
            cv.Optional(CONF_STEP, default=1): cv.float_,
            cv.Optional(CONF_MODE, default="BOX"): cv.enum(number.NUMBER_MODES, upper=True),
            cv.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
        })
    ) for key in BANK_SENSORS.keys()
})

async def to_code(config):
    hub = await cg.get_variable(config[CONF_ID])

    for key, (bank_id, offset, default_name, unit, device_class) in BANK_SENSORS.items():
        if key in config:
            num_conf = config[key]
            num = await number.new_number(
                num_conf,
                min_value=num_conf.get(CONF_MIN_VALUE, -50),
                max_value=num_conf.get(CONF_MAX_VALUE, 100),
                step=num_conf.get(CONF_STEP, 1)
            )
            cg.add(hub.register_bank_number(bank_id, offset, num))

            # Set up callback to write value when changed
            # ESPHome number components pass 'value' as float in the lambda context
            hub_var = cg.Pvariable(hub)
            if key == "dhw_lock":
                # uint8_t value (0-255) - unsigned
                lambda_code = f"{hub_var}->write_bank_value(0x0B, 13, (uint8_t)value);"
            else:
                # int8_t values (-128 to 127) - signed
                lambda_code = f"{hub_var}->write_bank_value(0x{bank_id:02X}, {offset}, (int8_t)clamp(value, -128.0f, 127.0f));"

            lambda_ = cg.Lambda([cg.Pvariable("value", cg.float_)], cg.RawStatement(lambda_code))
            cg.add(num.set_control(lambda_))

