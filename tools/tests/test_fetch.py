import json
import tempfile
import unittest
import urllib.parse
from pathlib import Path

from tools import fetch
from tools.contract import ContractError
from tools.tests.fakes import FIXTURES, client_for

# The original printed one line per entity: its ID and how many rows it got. The port also
# prints the window first, as every history reader in tools does.
EXPECTED = """\
window 2026-10-09 19:21:30+03:00 -> 2026-10-10 19:21:30+03:00 Europe/Helsinki
binary_sensor.geopro_kompressori 7
sensor.geopro_maaliuos 4
sensor.geopro_ml_varyl_kes 5
"""


class FetchTest(unittest.TestCase):
    def setUp(self):
        self.client, self.transport = client_for(self)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.out = Path(directory.name) / "history.json"

    def fetch(self, entities):
        return fetch.fetch(self.client, entities, "2026-10-09T19:21:30+03:00", "2026-10-10T19:21:30+03:00", self.out)

    def requested_ids(self):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.transport.requests[-1][0]).query)
        return query["filter_entity_id"][0].split(",")

    def test_writes_the_history_and_prints_rows_per_entity(self):
        text = self.fetch(["compressor", "brine", "summer_temp"])

        self.assertEqual(text, EXPECTED)
        self.assertEqual(json.loads(self.out.read_text()),
                         json.loads((FIXTURES / "history_day.json").read_text()))

    def test_takes_contract_keys_and_other_entity_ids(self):
        shelly = "sensor.shellyem3_34945474817a_channel_a_current"
        with self.assertRaises(ContractError):
            # The fixture has no Shelly history.
            self.fetch(["compressor", shelly])

        self.assertEqual(self.requested_ids(), ["binary_sensor.geopro_kompressori", shelly])

    def test_fetches_every_node_entity_by_default(self):
        with self.assertRaises(ContractError):
            # The fixture has three of them, so the rest are missing.
            self.fetch([])

        ids = self.requested_ids()
        self.assertIn("sensor.geopro_komponentin_versio", ids)
        self.assertIn("binary_sensor.geopro_s_hk_vastus", ids)

    def test_an_entity_with_no_history_fails_with_its_id(self):
        with self.assertRaises(ContractError) as raised:
            self.fetch(["compressor", "brine", "summer_temp", "tank_top"])

        self.assertIn("sensor.geopro_varaaja_yl", str(raised.exception))
        self.assertIn("renamed", str(raised.exception))
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
