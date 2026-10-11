import unittest

from tools import cycles
from tools.tests.recorded import day_client

# Read off fixtures/history_2026-10-09_day.json: the Status-bit rows, M9, M4, M10 and M1 at each
# edge, and the model's thresholds at the start worked by hand from the settings and M1
# (at 4.5 °C VaraajaYlä is 50 + 5 × 15.5 / 40 = 51.94).
EXPECTED = """\
window 2026-10-10 02:00:00+03:00 -> 2026-10-10 05:00:00+03:00 Europe/Helsinki
== settings
summer_temp  50.0 from 10-10 02:00
winter_temp  55.0 from 10-10 02:00
top_diff     3.0 from 10-10 02:00
bottom_diff  5.0 from 10-10 02:00
top_eh_diff  5.0 from 10-10 02:00
comp_lock    51.0 from 10-10 02:00
hp_mode      0.0 from 10-10 02:00
== compressor runs: the Status bit, with starts and breaks from the phase currents
10-10 02:46:57 -> 03:12:48  25.9 min, off before     - | starts 1 breaks 0 | M9 48.6 -> 52.0  M4 47.5 -> 47.0  M10 32.1 -> 47.2  M1 4.5 | model: start below 48.94, stop above 51.94, calls 02:46:56 -> 03:12:47
10-10 04:16:41 -> 04:43:42  27.0 min, off before  63.9 | starts 1 breaks 0 | M9 49.0 -> 52.2  M4 47.5 -> 47.0  M10 30.8 -> 47.4  M1 3.7 | model: start below 49.04, stop above 52.04, calls 04:16:40 -> 04:43:41
== heater runs: the Status bit
"""


class CyclesTest(unittest.TestCase):
    def test_lists_each_run_with_the_model_beside_it(self):
        text = cycles.report(day_client(self), "2026-10-10 02:00", "2026-10-10 05:00")

        self.assertEqual(text, EXPECTED)

    def test_counts_the_breaks_in_a_chattering_run(self):
        text = cycles.report(day_client(self), "2026-10-09 11:40", "2026-10-09 13:20")

        self.assertIn("10-09 11:47:17 -> 13:09:00  81.7 min, off before     - | starts 3 breaks 2 |", text)

    def test_a_window_that_opens_in_a_run_counts_no_start_for_it(self):
        # profile.py counts the same way.
        text = cycles.report(day_client(self), "2026-10-10 04:30", "2026-10-10 05:00")

        self.assertIn("10-10 04:30:00 -> 04:43:42  13.7 min, off before     - | starts 0 breaks 0 |", text)


if __name__ == "__main__":
    unittest.main()
