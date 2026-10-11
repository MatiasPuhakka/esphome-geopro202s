import unittest
from datetime import datetime, timedelta

from tools.plant import COMPRESSOR, PHASES, bits, numbers
from tools.runs import VALUE_INTERVAL, Span, current_runs, runs, status_runs
from tools.tests.recorded import local, recorded_day

T0 = datetime.fromisoformat("2026-10-10T04:00:00+03:00")


def at(seconds):
    return T0 + timedelta(seconds=seconds)


def three(rows):
    """The same (seconds, amps) rows on all three phases, as the compressor loads them."""
    series = [(at(s), amps) for s, amps in rows]
    return [series, series, series]


class StatusRunsTest(unittest.TestCase):
    def test_a_run_lasts_from_the_bit_going_on_to_it_going_off(self):
        status = [(at(0), False), (at(60), True), (at(1600), False), (at(5000), True), (at(6000), False)]

        self.assertEqual(status_runs(status), [Span(at(60), at(1600)), Span(at(5000), at(6000))])

    def test_an_unavailable_bit_keeps_the_state_from_before(self):
        # The Node restarting in the middle of a run says nothing about the Controller.
        status = [(at(0), True), (at(900), None), (at(913), True), (at(975), False)]

        self.assertEqual(status_runs(status), [Span(at(0), at(975))])

    def test_a_run_still_on_when_the_history_ends_has_no_end(self):
        self.assertEqual(status_runs([(at(0), False), (at(60), True)]), [Span(at(60), None)])


class CurrentRunsTest(unittest.TestCase):
    def test_the_compressor_draws_from_above_4_a_until_below_3_a_on_every_phase(self):
        rows = [(0, 1.0), (16, 5.7), (20, 6.7), (100, 3.5), (110, 6.0), (1620, 4.0), (1621, 1.0)]

        self.assertEqual(current_runs(three(rows)), [Span(at(16), at(1621))])

    def test_a_load_on_one_phase_is_not_the_compressor(self):
        phases = three([(0, 1.0)])
        phases[0] = [(at(0), 1.0), (at(10), 9.4), (at(500), 1.0)]

        self.assertEqual(current_runs(phases), [])

    def test_waits_until_every_phase_has_a_reading(self):
        phases = three([(10, 6.0), (100, 1.0)])
        phases[2] = [(at(0), None), (at(20), 6.0), (at(100), 1.0)]

        self.assertEqual(current_runs(phases), [Span(at(20), at(100))])


class RunsTest(unittest.TestCase):
    def test_a_run_counts_each_start_and_each_break_in_the_current(self):
        status = [(at(0), False), (at(60), True), (at(1000), False)]
        current = three([(0, 1.0), (58, 6.0), (300, 1.0), (308, 6.0), (500, 1.0), (520, 6.0), (998, 1.0)])

        (run,) = runs(status, current)

        self.assertEqual((run.start, run.end), (at(60), at(1000)))
        self.assertEqual(run.starts, (at(58), at(308), at(520)))
        self.assertEqual(run.breaks, (Span(at(300), at(308)), Span(at(500), at(520))))

    def test_current_that_began_before_the_run_is_not_a_start(self):
        # Another load drawing from before the call, such as the sauna, runs into it.
        status = [(at(0), False), (at(600), True), (at(1000), False)]
        current = three([(0, 1.0), (100, 10.5), (998, 1.0)])

        (run,) = runs(status, current)

        self.assertEqual(run.starts, ())

    def test_a_run_without_current_has_no_starts(self):
        status = [(at(0), False), (at(60), True), (at(1000), False)]

        (run,) = runs(status, three([(0, 1.0)]))

        self.assertEqual((run.starts, run.breaks), ((), ()))


# The compressor Status bit's on and off rows in the recorded day.
STATUS_RUNS = [
    ("10-09 10:32:05", "10-09 10:38:35"),
    ("10-09 11:47:17", "10-09 13:09:00"),
    ("10-09 14:22:32", "10-09 14:33:02"),
    ("10-09 17:03:12", "10-09 17:21:22"),
    ("10-09 18:40:55", "10-09 18:55:15"),
    ("10-09 20:59:51", "10-09 21:17:42"),
    ("10-09 23:07:07", "10-09 23:27:58"),
    ("10-10 00:58:12", "10-10 01:19:33"),
    ("10-10 02:46:57", "10-10 03:12:48"),
    ("10-10 04:16:41", "10-10 04:43:42"),
    ("10-10 05:48:05", "10-10 06:14:56"),
    ("10-10 07:21:29", "10-10 07:47:40"),
    ("10-10 08:24:42", "10-10 08:45:53"),
]
# During the 11:47 run the compressor stopped twice for 6 to 7 minutes while the Controller
# kept calling, the day the JV was found closed (#16).
CHATTER_RUN = 1
CHATTER_BREAKS = [("10-09 12:27:52", "10-09 12:34:07"), ("10-09 12:44:10", "10-09 12:51:01")]
# A load of about 10 A on all three phases with both Status bits off: not the compressor,
# likely the sauna.
OTHER_LOAD = [("10-09 10:41:52", "10-09 11:10:16"), ("10-09 11:15:39", "10-09 11:27:40"),
              ("10-09 11:33:54", "10-09 11:44:39")]


def spans(pairs):
    return [Span(local(a), local(b)) for a, b in pairs]


class RecordedDayTest(unittest.TestCase):
    def setUp(self):
        day = recorded_day()
        self.bits = bits(day[COMPRESSOR])
        self.phases = [numbers(day[p]) for p in PHASES]

    def test_finds_the_runs_in_the_status_bit(self):
        self.assertEqual(status_runs(self.bits), spans(STATUS_RUNS))

    def test_the_phase_currents_start_and_end_each_run_within_the_value_interval(self):
        drawn = current_runs(self.phases)
        for run in spans(STATUS_RUNS):
            with self.subTest(run=run.start.isoformat()):
                started = [s for s in drawn if abs(s.start - run.start) <= VALUE_INTERVAL]
                ended = [s for s in drawn if s.end and abs(s.end - run.end) <= VALUE_INTERVAL]
                self.assertEqual(len(started), 1)
                self.assertEqual(len(ended), 1)

    def test_the_phase_currents_find_no_other_compressor_runs(self):
        status = spans(STATUS_RUNS)
        drawn = current_runs(self.phases)

        inside = [s for s in drawn if any(r.start - VALUE_INTERVAL <= s.start and s.end <= r.end + VALUE_INTERVAL
                                          for r in status)]
        outside = [s for s in drawn if s not in inside]
        self.assertEqual(len(inside), len(STATUS_RUNS) + len(CHATTER_BREAKS))
        self.assertEqual([(s.start.replace(microsecond=0), s.end.replace(microsecond=0)) for s in outside],
                         [(s.start, s.end) for s in spans(OTHER_LOAD)])

    def test_counts_the_starts_and_breaks_in_each_run(self):
        found = runs(self.bits, self.phases)

        self.assertEqual([len(r.starts) for r in found], [3 if i == CHATTER_RUN else 1 for i in range(len(found))])
        self.assertEqual(list(found[CHATTER_RUN].breaks), spans(CHATTER_BREAKS))
        self.assertEqual(sum(len(r.breaks) for r in found), len(CHATTER_BREAKS))


if __name__ == "__main__":
    unittest.main()
