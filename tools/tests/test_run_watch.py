import io
import unittest

from tools import run_watch
from tools.contract import ContractError
from tools.tests.fakes import EXPECTED, FakeClock, ReplayHomeAssistant, client_for

# fixtures/history_run_watch.json holds two windows of 2026-10-09 history for the entities
# run_watch reads. The expected output is what .scratch/live/scripts/run_watch.py printed when
# the same history was replayed to it.
HISTORY = "history_run_watch.json"


class RunWatchTest(unittest.TestCase):
    def watch(self, start):
        clock = FakeClock(start)
        client, _ = client_for(self, ReplayHomeAssistant(clock, HISTORY))
        out, samples = io.StringIO(), io.StringIO()
        run_watch.watch(client, samples, out, clock)
        return out.getvalue(), samples.getvalue().splitlines()

    def test_reports_the_heater_and_a_short_run(self):
        out, samples = self.watch("2026-10-09T07:31:30+00:00")

        self.assertEqual(out, (EXPECTED / "run_watch_heater.txt").read_text())
        self.assertEqual(len(samples), 214)
        self.assertEqual(samples[0], "10:31:30  9.44  1.20  1.15 call=off heater=on M7 115.1, M9 45.7, M10 47.8, brine 7.2")
        self.assertEqual(samples[-1], "10:38:36  9.63  1.09  0.98 call=off heater=off M7 65.0, M9 51.3, M10 45.4, brine 6.1")

    def test_reports_a_current_break_and_the_tank_bottom_during_a_run(self):
        out, samples = self.watch("2026-10-09T15:38:00+00:00")

        self.assertEqual(out, (EXPECTED / "run_watch_call.txt").read_text())
        self.assertEqual(len(samples), 519)
        self.assertEqual(samples[-1], "18:55:16  0.64  1.22  1.44 call=off heater=off M7 60.4, M9 51.4, M10 49.2, brine 6.1")

    def test_backfills_from_history_when_it_starts_during_a_call(self):
        out, samples = self.watch("2026-10-09T15:50:00+00:00")

        self.assertEqual(out, (EXPECTED / "run_watch_backfill.txt").read_text())
        self.assertEqual(len(samples), 159)
        self.assertEqual(samples[0], "18:50:00  7.07  7.12  7.13 call=on heater=off M7 59.3, M9 48.5, M10 48.2, brine 6.1")

    def test_a_renamed_entity_fails_before_watching(self):
        clock = FakeClock("2026-10-09T15:38:00+00:00")
        transport = ReplayHomeAssistant(clock, HISTORY)
        transport.rows["sensor.geopro_maaliuos_2"] = transport.rows.pop("sensor.geopro_maaliuos")
        client, _ = client_for(self, transport)

        with self.assertRaises(ContractError) as raised:
            run_watch.watch(client, io.StringIO(), io.StringIO(), clock)

        self.assertIn("sensor.geopro_maaliuos (brine", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
