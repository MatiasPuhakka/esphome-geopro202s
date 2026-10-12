import re
import tempfile
import unittest
from pathlib import Path

from tools import contract
from tools.contract import ContractError

TOOLS = Path(__file__).resolve().parents[1]

# A contract in the format of tests/entity-contract.txt, with one entity that has no ID yet.
SMALL = """\
# Every key in tests/all-keys.yaml: platform and entity options (- for unset).
brine: sensor unit=°C device_class=temperature state_class=measurement accuracy=2 icon=mdi:thermometer entity_category=-
compressor: binary_sensor unit=- device_class=running state_class=- accuracy=- icon=mdi:engine entity_category=-
hp_mode: sensor unit=- device_class=- state_class=measurement accuracy=0 icon=mdi:gauge entity_category=-

# Every entity in node.yaml: platform, name and the entity ID Home Assistant has
brine: sensor "Maaliuos" sensor.geopro_maaliuos
compressor: binary_sensor "Kompressori" binary_sensor.geopro_kompressori
hp_mode: sensor "ML Ohjaustapa" (no entity ID recorded)
"""


def small_contract(test):
    directory = tempfile.TemporaryDirectory()
    test.addCleanup(directory.cleanup)
    path = Path(directory.name) / "entity-contract.txt"
    path.write_text(SMALL, encoding="utf-8")
    return contract.load(path)


class CommittedContractTest(unittest.TestCase):
    def test_reads_an_entity_from_the_committed_contract(self):
        brine = contract.load().entity("brine")

        self.assertEqual(brine.entity_id, "sensor.geopro_maaliuos")
        self.assertEqual(brine.name, "Maaliuos")
        self.assertEqual(brine.platform, "sensor")
        self.assertEqual(brine.unit, "°C")
        self.assertEqual(brine.device_class, "temperature")
        self.assertEqual(brine.state_class, "measurement")

    def test_lists_the_nodes_entities_in_config_order(self):
        keys = list(contract.load().entities)

        self.assertEqual(keys[:3], ["component_revision", "outside_temp", "l1_supply"])
        # tests/all-keys.yaml sets l1_room; node.yaml doesn't, so the Node has no such entity.
        self.assertNotIn("l1_room", keys)


class LookupTest(unittest.TestCase):
    def test_gives_entity_ids_for_keys(self):
        c = small_contract(self)

        self.assertEqual(c.entity_ids(["compressor", "brine"]),
                         ["binary_sensor.geopro_kompressori", "sensor.geopro_maaliuos"])

    def test_reads_unset_options_as_none(self):
        compressor = small_contract(self).entity("compressor")

        self.assertIsNone(compressor.unit)
        self.assertIsNone(compressor.state_class)
        self.assertEqual(compressor.device_class, "running")

    def test_an_unknown_key_names_the_key_and_the_contract(self):
        with self.assertRaises(ContractError) as raised:
            small_contract(self).entity_id("tank_top")

        self.assertIn("tank_top", str(raised.exception))
        self.assertIn("entity-contract.txt", str(raised.exception))

    def test_a_key_with_no_entity_id_says_how_to_record_one(self):
        with self.assertRaises(ContractError) as raised:
            small_contract(self).entity_id("hp_mode")

        self.assertIn("hp_mode", str(raised.exception))
        self.assertIn("record-ids", str(raised.exception))


class RequireTest(unittest.TestCase):
    STATES = [{"entity_id": "sensor.geopro_maaliuos"}, {"entity_id": "binary_sensor.geopro_kompressori"}]

    def test_passes_when_home_assistant_has_every_entity(self):
        small_contract(self).require(self.STATES, ["brine", "compressor"])

    def test_a_renamed_entity_fails_with_its_key_and_old_id(self):
        renamed = [{"entity_id": "sensor.geopro_maaliuos_2"}, {"entity_id": "binary_sensor.geopro_kompressori"}]

        with self.assertRaises(ContractError) as raised:
            small_contract(self).require(renamed, ["brine", "compressor"])

        message = str(raised.exception)
        self.assertIn("sensor.geopro_maaliuos (brine", message)
        self.assertIn("renamed", message)
        self.assertNotIn("kompressori", message)

    def test_lists_every_missing_entity(self):
        missing = small_contract(self).missing([], ["brine", "compressor"])

        self.assertEqual([e.key for e in missing], ["brine", "compressor"])


class NoHardCodedEntityIdsTest(unittest.TestCase):
    def test_tools_code_takes_geopro_entity_ids_from_the_contract(self):
        entity_id = re.compile(r"\b(?:binary_sensor|sensor|text_sensor)\.geopro_\w+")
        for path in sorted(TOOLS.glob("*.py")):
            with self.subTest(path.name):
                self.assertIsNone(entity_id.search(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
