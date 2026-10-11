import os
import unittest
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from tools.ha import LOCAL, HomeAssistant, env_file
from tools.tests.fakes import FAKE_TOKEN, RecordedHomeAssistant, TempEnv, client_for


class TokenTest(unittest.TestCase):
    def test_sends_the_token_from_the_env_file(self):
        client, transport = client_for(self)

        client.states()

        url, headers = transport.requests[0]
        self.assertEqual(url, "http://192.168.1.159:8123/api/states")
        self.assertEqual(headers["Authorization"], "Bearer " + FAKE_TOKEN)

    def test_finds_the_env_file_named_by_geopro_env_file(self):
        transport = RecordedHomeAssistant()
        with mock.patch.dict(os.environ, {"GEOPRO_ENV_FILE": str(TempEnv(self).path)}):
            client = HomeAssistant(transport=transport)

        client.states()

        self.assertEqual(transport.requests[0][1]["Authorization"], "Bearer " + FAKE_TOKEN)

    def test_defaults_to_the_env_file_at_the_repo_root(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(env_file(), Path(__file__).resolve().parents[2] / ".env")

    def test_takes_the_url_from_the_env_file(self):
        transport = RecordedHomeAssistant()
        env = TempEnv(self, "ACCESS_TOKEN=%s\nHA_URL=http://ha.test:8123/\n" % FAKE_TOKEN)
        HomeAssistant(env_path=env.path, transport=transport).states()

        self.assertEqual(transport.requests[0][0], "http://ha.test:8123/api/states")

    def test_a_missing_env_file_names_the_path_and_the_override(self):
        with self.assertRaises(SystemExit) as raised:
            HomeAssistant(env_path="/nonexistent/.env", transport=RecordedHomeAssistant())

        self.assertIn("/nonexistent/.env", str(raised.exception))
        self.assertIn("GEOPRO_ENV_FILE", str(raised.exception))

    def test_an_env_file_without_a_token_says_so(self):
        env = TempEnv(self, "HA_URL=http://ha.test:8123\n")
        with self.assertRaises(SystemExit) as raised:
            HomeAssistant(env_path=env.path, transport=RecordedHomeAssistant())

        self.assertIn("ACCESS_TOKEN", str(raised.exception))

    def test_never_shows_the_token(self):
        client, _ = client_for(self)

        self.assertNotIn(FAKE_TOKEN, repr(client))

    def test_an_http_error_leaves_the_token_out(self):
        def refuse(url, headers):
            raise urllib.error.HTTPError(url, 401, "Unauthorized", None, None)

        client = HomeAssistant(env_path=TempEnv(self).path, transport=refuse)
        with self.assertRaises(urllib.error.HTTPError) as raised:
            client.states()

        self.assertNotIn(FAKE_TOKEN, str(raised.exception))
        self.assertNotIn(FAKE_TOKEN, repr(raised.exception))


def path_and_query(url):
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.unquote(parts.path), urllib.parse.parse_qs(parts.query, keep_blank_values=True)


class StateTest(unittest.TestCase):
    def test_reads_one_entity(self):
        client, transport = client_for(self)

        state = client.state("sensor.geopro_maaliuos")

        self.assertEqual(state["state"], "17.2000007629395")
        self.assertEqual(transport.requests[0][0], "http://192.168.1.159:8123/api/states/sensor.geopro_maaliuos")

    def test_reads_the_nord_pool_quarter_hour_prices_from_the_current_state(self):
        client, _ = client_for(self)

        prices = client.state("sensor.nordpool_kwh_fi_eur_3_10_0255")["attributes"]["raw_today"]

        self.assertEqual(prices[1], {"start": "2026-10-10T00:15:00+03:00", "end": "2026-10-10T00:30:00+03:00",
                                     "value": 0.023})

    def test_reads_every_entity(self):
        client, _ = client_for(self)

        ids = [s["entity_id"] for s in client.states()]

        self.assertIn("sensor.nordpool_kwh_fi_eur_3_10_0255", ids)
        self.assertEqual(len(ids), 4)


class HistoryTest(unittest.TestCase):
    IDS = ["binary_sensor.geopro_kompressori", "sensor.geopro_maaliuos", "sensor.geopro_ml_varyl_kes"]

    def test_encodes_start_and_end_and_asks_for_minimal_rows(self):
        client, transport = client_for(self)

        client.history(self.IDS, "2026-10-09T19:21:30+03:00", "2026-10-10T19:21:30+03:00")

        url = transport.requests[0][0]
        # An unencoded "+03:00" in a query string arrives at Home Assistant as " 03:00".
        self.assertNotIn("+", url)
        path, query = path_and_query(url)
        self.assertEqual(path, "/api/history/period/2026-10-09T19:21:30+03:00")
        self.assertEqual(query["end_time"], ["2026-10-10T19:21:30+03:00"])
        self.assertEqual(query["filter_entity_id"], [",".join(self.IDS)])
        self.assertIn("minimal_response", query)
        self.assertIn("no_attributes", query)

    def test_groups_rows_by_entity(self):
        client, _ = client_for(self)

        history = client.history(self.IDS, "2026-10-09T19:21:30+03:00", "2026-10-10T19:21:30+03:00")

        self.assertEqual(sorted(history.series), self.IDS)
        self.assertEqual([r["state"] for r in history.series["sensor.geopro_ml_varyl_kes"]],
                         ["50.0", "unavailable", "50.0", "55.0", "53.0"])

    def test_records_its_window_in_finnish_time(self):
        client, _ = client_for(self)

        history = client.history(self.IDS, "2026-10-09T16:21:30+00:00", "2026-10-10T19:21:30")

        self.assertEqual(history.start.isoformat(), "2026-10-09T19:21:30+03:00")
        self.assertEqual(history.end.isoformat(), "2026-10-10T19:21:30+03:00")
        self.assertEqual(history.window(), "2026-10-09 19:21:30+03:00 -> 2026-10-10 19:21:30+03:00 Europe/Helsinki")

    def test_reads_a_time_without_an_offset_as_finnish_time(self):
        client, transport = client_for(self)

        # Daylight saving time ends on 2026-10-25, so the two ends have different offsets.
        client.history(self.IDS, "2026-10-24 12:00", "2026-10-26 12:00")

        path, query = path_and_query(transport.requests[0][0])
        self.assertEqual(path, "/api/history/period/2026-10-24T12:00:00+03:00")
        self.assertEqual(query["end_time"], ["2026-10-26T12:00:00+02:00"])

    def test_ends_now_when_no_end_is_given(self):
        client, transport = client_for(self)
        before = datetime.now(timezone.utc)

        history = client.history(self.IDS, "2026-10-09T19:21:30+03:00")

        self.assertGreaterEqual(history.end, before.replace(microsecond=0))
        self.assertLessEqual(history.end, datetime.now(timezone.utc))
        self.assertEqual(history.end.utcoffset(), history.end.astimezone(LOCAL).utcoffset())
        _, query = path_and_query(transport.requests[0][0])
        self.assertEqual(query["end_time"], [history.end.isoformat()])

    def test_refuses_a_request_with_no_entities(self):
        client, transport = client_for(self)

        # Home Assistant would read an empty filter as no filter at all.
        with self.assertRaises(ValueError):
            client.history([], "2026-10-09T19:21:30+03:00")
        self.assertEqual(transport.requests, [])

    def test_includes_attributes_on_request(self):
        client, transport = client_for(self)
        nordpool = "sensor.nordpool_kwh_fi_eur_3_10_0255"

        history = client.history([nordpool], "2026-10-10T12:00:00+03:00", "2026-10-10T12:20:00+03:00",
                                 attributes=True)

        _, query = path_and_query(transport.requests[0][0])
        self.assertNotIn("no_attributes", query)
        self.assertNotIn("minimal_response", query)
        self.assertEqual([r["attributes"]["current_price"] for r in history.series[nordpool]],
                         [0.022, 0.027, 0.028])


if __name__ == "__main__":
    unittest.main()
