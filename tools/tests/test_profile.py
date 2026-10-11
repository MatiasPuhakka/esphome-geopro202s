import unittest

from tools import profile
from tools.tests.recorded import day_client

# Read off fixtures/history_2026-10-09_day.json around the 04:16:41 to 04:43:42 run, where the
# compressor started drawing at 04:16:36 and stopped at 04:43:38. M9 holds at 49.0 while the
# run lifts the tank bottom first (#24).
EXPECTED = """\
window 2026-10-10 04:10:00+03:00 -> 2026-10-10 04:50:00+03:00 Europe/Helsinki
time      M1    M9    M4   M10  status model  max A starts
04:10   4.0  49.4  47.5  33.4  off    off      6.1      1
04:20   3.7  49.0  45.0  40.4  on     on       5.5      0
04:30   3.7  49.0  44.9  44.8  on     on       5.5      0
04:40   3.7  50.9  46.6  46.6  on     on       5.5      0
"""


class ProfileTest(unittest.TestCase):
    def test_prints_the_tank_and_the_compressor_in_each_slot(self):
        text = profile.report(day_client(self), "2026-10-10 04:10", "2026-10-10 04:50", 10)

        self.assertEqual(text, EXPECTED)

    def test_a_window_that_starts_in_a_run_starts_the_model_calling(self):
        # M9 50.9 lies between the start and stop thresholds, so only the Status bit tells.
        text = profile.report(day_client(self), "2026-10-10 04:40", "2026-10-10 04:45", 5)

        self.assertEqual(text.splitlines()[-1], "04:40   3.7  50.9  46.6  46.6  on     on       5.5      0")

    def test_counts_no_start_for_another_load_with_the_status_bit_off(self):
        # About 10 A on all three phases from 10:41:52 to 11:10:16, likely the sauna.
        text = profile.report(day_client(self), "2026-10-09 10:40", "2026-10-09 11:20", 10)

        self.assertEqual([line.split()[-1] for line in text.splitlines()[2:]], ["0", "0", "0", "0"])
        self.assertEqual([line.split()[-2] for line in text.splitlines()[2:]], ["11.3", "10.9", "10.7", "11.1"])


if __name__ == "__main__":
    unittest.main()
