import json
import unittest

from tools import compare_entities
from tools.tests.fakes import EXPECTED, FIXTURES


def snapshots():
    return (json.loads((FIXTURES / "states_before_flash.json").read_text()),
            json.loads((FIXTURES / "states_after_flash.json").read_text()))


class CompareEntitiesTest(unittest.TestCase):
    def test_compares_the_snapshots_from_before_and_after_a_flash(self):
        # The #11 flash dropped four entities and changed three units.
        before, after = snapshots()

        self.assertEqual(compare_entities.compare(before, after),
                         (EXPECTED / "compare_entities.txt").read_text())

    def test_flags_an_entity_that_did_not_update_and_one_that_is_unavailable(self):
        before, after = snapshots()
        by_id = {state["entity_id"]: state for state in after}
        by_id["sensor.geopro_maaliuos"]["last_reported"] = next(
            s["last_reported"] for s in before if s["entity_id"] == "sensor.geopro_maaliuos")
        by_id["sensor.geopro_varaaja_ala"]["state"] = "unavailable"

        self.assertEqual(compare_entities.compare(before, after),
                         (EXPECTED / "compare_entities_flagged.txt").read_text())


if __name__ == "__main__":
    unittest.main()
