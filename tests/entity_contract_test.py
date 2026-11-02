"""Tests for entity_contract.py. Plain Python: run with `python3 -m unittest discover -s tests -p '*_test.py'`."""

import unittest

import entity_contract

KEYS_CONFIG = """\
esphome:
  name: geopro-all-keys
geopro_202s:
  id: geopro
  value_interval: 15s
  outside_temp:
    name: outside_temp
    disabled_by_default: false
    force_update: false
    unit_of_measurement: °C
    icon: mdi:thermometer
    accuracy_decimals: 2
    device_class: temperature
    state_class: measurement
  compressor:
    name: compressor
    disabled_by_default: false
    icon: mdi:engine
    device_class: running
  uart_id: uart_bus
logger:
  baud_rate: 0
"""

PLATFORMS = {"outside_temp": "sensor", "compressor": "binary_sensor"}


class KeyContractTest(unittest.TestCase):
    def test_lists_each_keys_platform_and_entity_options(self):
        self.assertEqual(
            entity_contract.key_lines(KEYS_CONFIG, PLATFORMS),
            [
                "outside_temp: sensor unit=°C device_class=temperature state_class=measurement"
                " accuracy=2 icon=mdi:thermometer entity_category=-",
                "compressor: binary_sensor unit=- device_class=running state_class=-"
                " accuracy=- icon=mdi:engine entity_category=-",
            ],
        )

    def test_fails_when_the_config_leaves_out_a_register_map_key(self):
        platforms = dict(PLATFORMS, hours_comp="sensor")
        with self.assertRaisesRegex(ValueError, "hours_comp"):
            entity_contract.key_lines(KEYS_CONFIG, platforms)

    def test_fails_on_an_entity_key_with_no_known_platform(self):
        with self.assertRaisesRegex(ValueError, "compressor"):
            entity_contract.key_lines(KEYS_CONFIG, {"outside_temp": "sensor"})


class ContractDiffTest(unittest.TestCase):
    def test_shows_a_changed_state_class_as_a_one_line_diff(self):
        committed = entity_contract.contract_text(KEYS_CONFIG, PLATFORMS)
        changed = KEYS_CONFIG.replace("state_class: measurement", "state_class: total")
        generated = entity_contract.contract_text(changed, PLATFORMS)
        diff = entity_contract.contract_diff(committed, generated).splitlines()
        self.assertEqual(
            [line for line in diff if line[:1] in "+-" and line[:3] not in ("+++", "---")],
            [
                "-outside_temp: sensor unit=°C device_class=temperature state_class=measurement"
                " accuracy=2 icon=mdi:thermometer entity_category=-",
                "+outside_temp: sensor unit=°C device_class=temperature state_class=total"
                " accuracy=2 icon=mdi:thermometer entity_category=-",
            ],
        )

    def test_lists_only_the_keys(self):
        text = entity_contract.contract_text(KEYS_CONFIG, PLATFORMS)
        self.assertEqual(
            [line for line in text.splitlines() if line and not line.startswith("#")],
            entity_contract.key_lines(KEYS_CONFIG, PLATFORMS),
        )

    def test_is_empty_when_nothing_changed(self):
        text = entity_contract.contract_text(KEYS_CONFIG, PLATFORMS)
        self.assertEqual(entity_contract.contract_diff(text, text), "")


if __name__ == "__main__":
    unittest.main()
