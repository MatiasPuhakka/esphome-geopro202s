import unittest
import urllib.parse

from tools import day_run
from tools.tests.fakes import client_for

# Counted by hand from fixtures/history_day.json.
EXPECTED = """\
window 2026-10-09 19:21:30+03:00 -> 2026-10-10 19:21:30+03:00 Europe/Helsinki
binary_sensor.geopro_kompressori             changes    6  unavailable 1  off -> off
sensor.geopro_maaliuos                       changes    3  unavailable 0  15.80000 -> 17.60000
sensor.geopro_ml_varyl_kes                   changes    4  unavailable 1  50.0 -> 53.0
entities: 3 | unavailable/unknown states: 2
"""


class DayRunTest(unittest.TestCase):
    def setUp(self):
        self.client, self.transport = client_for(self)

    def test_summarises_each_geopro_entity_over_the_window(self):
        text = day_run.summary(self.client, "2026-10-09T19:21:30+03:00", "2026-10-10T19:21:30+03:00")

        self.assertEqual(text, EXPECTED)

    def test_asks_only_for_the_geopro_entities(self):
        day_run.summary(self.client, "2026-10-09T19:21:30+03:00", "2026-10-10T19:21:30+03:00")

        history_url = self.transport.requests[-1][0]
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(history_url).query)
        self.assertEqual(query["filter_entity_id"],
                         ["binary_sensor.geopro_kompressori,sensor.geopro_maaliuos,sensor.geopro_ml_varyl_kes"])


if __name__ == "__main__":
    unittest.main()
