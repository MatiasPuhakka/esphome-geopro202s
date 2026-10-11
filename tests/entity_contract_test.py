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


NODE_CONFIG = """\
esphome:
  name: geopro-202s
  friendly_name: Geopro
geopro_202s:
  id: geopro
  l1_minus20:
    name: L1 -20°C
    state_class: measurement
  l1_plus20:
    name: L1 +20°C
    state_class: measurement
  compressor:
    name: Kompressori
    device_class: running
  value_interval: 10s
"""

NODE_PLATFORMS = {"l1_minus20": "sensor", "l1_plus20": "sensor", "compressor": "binary_sensor"}


class NodeContractTest(unittest.TestCase):
    def test_gives_each_entity_the_id_home_assistant_has_for_its_friendly_name(self):
        # Both names slugify to l1_20_c, so Home Assistant added _2 to the second one.
        entity_ids = [
            ("sensor.geopro_l1_20_c_2", "Geopro L1 +20°C"),
            ("sensor.geopro_l1_20_c", "Geopro L1 -20°C"),
            ("binary_sensor.geopro_kompressori", "Geopro Kompressori"),
        ]
        self.assertEqual(
            entity_contract.node_lines(NODE_CONFIG, NODE_PLATFORMS, entity_ids),
            [
                'l1_minus20: sensor "L1 -20°C" sensor.geopro_l1_20_c',
                'l1_plus20: sensor "L1 +20°C" sensor.geopro_l1_20_c_2',
                'compressor: binary_sensor "Kompressori" binary_sensor.geopro_kompressori',
            ],
        )

    def test_reads_names_esphome_quotes_or_wraps(self):
        # How ESPHome 2026.9.1 prints these names in `esphome config`.
        config = (
            "esphome:\n"
            "  name: geopro-202s\n"
            "geopro_202s:\n"
            "  l1_minus20:\n"
            "    name: 'it''s: 20'\n"
            "    force_update: false\n"
            "  l1_plus20:\n"
            "    name: Lisälämmitys aika ja paljon muuta tekstiä joka ei mahdu yhdelle riville\n"
            "      vaan jatkuu\n"
            "    filters:\n"
            "      - multiply: 2.0\n"
            "  compressor:\n"
            "    name: \"tab\\there\"\n"
        )
        self.assertEqual(
            entity_contract.node_lines(config, NODE_PLATFORMS, []),
            [
                'l1_minus20: sensor "it\'s: 20" (no entity ID recorded)',
                'l1_plus20: sensor "Lisälämmitys aika ja paljon muuta tekstiä joka ei mahdu'
                ' yhdelle riville vaan jatkuu" (no entity ID recorded)',
                'compressor: binary_sensor "tab\\there" (no entity ID recorded)',
            ],
        )

    def test_flags_an_entity_with_no_recorded_id_on_its_platform(self):
        # A sensor called Kompressori is a different entity from the binary sensor.
        entity_ids = [("sensor.geopro_kompressori", "Geopro Kompressori")]
        self.assertEqual(
            entity_contract.node_lines(NODE_CONFIG, NODE_PLATFORMS, entity_ids)[2],
            'compressor: binary_sensor "Kompressori" (no entity ID recorded)',
        )


class ContractDiffTest(unittest.TestCase):
    def test_shows_a_changed_state_class_as_a_one_line_diff(self):
        committed = entity_contract.contract_text(KEYS_CONFIG, KEYS_CONFIG, PLATFORMS, [])
        changed = KEYS_CONFIG.replace("state_class: measurement", "state_class: total")
        generated = entity_contract.contract_text(changed, KEYS_CONFIG, PLATFORMS, [])
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

    def test_is_empty_when_nothing_changed(self):
        text = entity_contract.contract_text(KEYS_CONFIG, KEYS_CONFIG, PLATFORMS, [])
        self.assertEqual(entity_contract.contract_diff(text, text), "")


class EntityIdsTest(unittest.TestCase):
    def test_records_the_nodes_sensors_from_a_states_snapshot(self):
        states = [
            {"entity_id": "sensor.geopro_ulkol_mp_tila", "state": "-3.2",
             "attributes": {"friendly_name": "Geopro Ulkolämpötila", "unit_of_measurement": "°C"}},
            {"entity_id": "binary_sensor.geopro_kompressori", "state": "on",
             "attributes": {"friendly_name": "Geopro Kompressori"}},
            {"entity_id": "sensor.sun_next_dawn", "state": "2026-10-12T04:00:00+00:00",
             "attributes": {"friendly_name": "Sun Next dawn"}},
            {"entity_id": "button.geopro_restart", "state": "unknown",
             "attributes": {"friendly_name": "Geopro Restart"}},
        ]
        text = entity_contract.entity_ids_text(states, "Geopro", "2026-10-11")
        self.assertEqual(
            entity_contract.parse_entity_ids(text),
            [
                ("binary_sensor.geopro_kompressori", "Geopro Kompressori"),
                ("sensor.geopro_ulkol_mp_tila", "Geopro Ulkolämpötila"),
            ],
        )
        self.assertNotIn("-3.2", text)


if __name__ == "__main__":
    unittest.main()
