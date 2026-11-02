import unittest
from datetime import datetime

from tools import gaps
from tools.ha import LOCAL
from tools.tests.recorded import day_client

# Read off fixtures/history_2026-10-09_day.json: the Status-bit runs end at 03:12:48 and start
# again at 04:16:41. The fixture has no circulation pump, so its state is unknown.
EXPECTED = """\
window 2026-10-10 02:00:00+03:00 -> 2026-10-10 05:00:00+03:00 Europe/Helsinki
== gaps: start, hours, M1, fall in °C/h of M9, M4, M10, fastest M9 fall in 10 min, M9 and M4 at the next start
10-10 03:12 pump ?    1.06 h  M1   4.1  M9  2.82  M4  0.33  M10 18.48  draw 0.7  next M9 49.0 M4 47.5
== by outdoor band: gaps, median hours, median fall in °C/h of M9 and M4
 +4 to  +6 °C pump ?     1   1.06 h  M9 2.82  M4 0.33
"""


def at(text):
    return datetime.strptime("2026-11-01 " + text, "%Y-%m-%d %H:%M").replace(tzinfo=LOCAL)


class GapsTest(unittest.TestCase):
    def test_lists_the_gap_between_two_runs(self):
        text = gaps.report(day_client(self), "2026-10-10 02:00", "2026-10-10 05:00")

        self.assertEqual(text, EXPECTED)

    def test_the_pump_counts_as_off_for_a_gap_it_was_off_more_than_half_of(self):
        pump = [(at("07:00"), True), (at("22:00"), False)]

        self.assertTrue(gaps._pump_off(pump, at("21:00"), at("23:30")))  # off 1.5 h of 2.5
        self.assertFalse(gaps._pump_off(pump, at("21:00"), at("22:30")))  # off 0.5 h of 1.5
        self.assertIsNone(gaps._pump_off(pump, at("06:00"), at("08:00")))  # not known at 06:00

    def test_the_fastest_fall_is_over_10_minutes(self):
        top = [(at("18:00"), 52.0), (at("18:05"), 51.8), (at("18:08"), 49.0), (at("18:30"), 47.0)]

        self.assertAlmostEqual(gaps._fastest_fall(top, at("18:00"), at("18:30")), 3.0)


if __name__ == "__main__":
    unittest.main()
