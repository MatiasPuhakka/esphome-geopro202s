import unittest
from dataclasses import replace
from datetime import timedelta

from tools.controller import SAHKOVASTUS, Settings, State, Temperatures, step, thresholds
from tools.plant import COMPRESSOR, OUTDOOR, TANK_TOP, bits, numbers, replay, value_at
from tools.runs import status_runs
from tools.tests.recorded import local, recorded_day

# The settings on 2026-10-10 (#24 Notes, docs/controller.md).
OCTOBER = Settings(var_yla_kesa=50, var_yla_talvi=55, varaaja_yla_ero=3, varaaja_ala_ero=5,
                   var_yla_ero_sv=5, kompr_esto=51, ml_ohjaustapa=0)


class ThresholdTest(unittest.TestCase):
    def test_the_tank_top_cycles_between_about_49_and_52_at_3_to_5_degrees_outside(self):
        for outdoor in (3, 4, 5):
            with self.subTest(outdoor=outdoor):
                t = thresholds(OCTOBER, outdoor)

                self.assertAlmostEqual(t.start, 49, delta=0.2)
                self.assertAlmostEqual(t.stop, 52, delta=0.2)

    def test_varaaja_yla_runs_from_var_yla_kesa_at_plus_20_to_var_yla_talvi_at_minus_20(self):
        # Worked from the graph on manuals/kasikirja.md#s21: a straight line between the two,
        # flat beyond.
        cases = {30: 50, 20: 50, 3: 52.125, 0: 52.5, -20: 55, -30: 55}
        for outdoor, expected in cases.items():
            with self.subTest(outdoor=outdoor):
                self.assertAlmostEqual(thresholds(OCTOBER, outdoor).varaaja_yla, expected)

    def test_names_every_threshold(self):
        t = thresholds(OCTOBER, 3)

        self.assertAlmostEqual(t.varaaja_yla, 52.125)
        self.assertAlmostEqual(t.start, 49.125)  # VaraajaYlä − VaraajaYläEro
        self.assertAlmostEqual(t.stop, 52.125)  # VaraajaYlä
        self.assertAlmostEqual(t.heater, 44.125)  # VaraajaYlä − VaraajaYläEro − VarYläEroSv
        self.assertAlmostEqual(t.restart, 46)  # Kompr.esto − VaraajaAlaEro


def calls_after(settings, readings, state=State()):
    """Steps the model through (outdoor, M9, M10) readings and returns whether it called after each."""
    calls = []
    for outdoor, top, bottom in readings:
        state = step(settings, Temperatures(outdoor=outdoor, tank_top=top, tank_bottom=bottom), state)
        calls.append(state.calling)
    return calls


class CallTest(unittest.TestCase):
    # At +3 °C outside: start below 49.125, stop above 52.125.

    def test_calls_from_below_the_start_threshold_until_above_varaaja_yla(self):
        tops = [50.0, 49.2, 49.1, 49.5, 51.0, 52.1, 52.2, 51.5, 49.2]

        calls = calls_after(OCTOBER, [(3, top, 40) for top in tops])

        self.assertEqual(calls, [False, False, True, True, True, True, False, False, False])

    def test_kompr_esto_stops_a_tank_top_call_until_the_bottom_falls_varaaja_ala_ero_below_it(self):
        # Kompr.esto 51, VaraajaAlaEro 5: stop at M10 51, restart at 46.
        bottoms = [45.0, 50.9, 51.0, 49.0, 46.1, 46.0, 47.0]

        calls = calls_after(OCTOBER, [(3, 48.0, bottom) for bottom in bottoms])

        self.assertEqual(calls, [True, True, False, False, False, True, True])

    def test_never_calls_when_ml_ohjaustapa_is_sahkovastus(self):
        heater_only = replace(OCTOBER, ml_ohjaustapa=SAHKOVASTUS)

        self.assertEqual(calls_after(heater_only, [(3, 45.0, 40.0)]), [False])

    def test_resumes_the_call_once_ml_ohjaustapa_allows_the_compressor_again(self):
        state = step(replace(OCTOBER, ml_ohjaustapa=SAHKOVASTUS), Temperatures(3, 45.0, 40.0), State())

        self.assertEqual(calls_after(OCTOBER, [(3, 45.0, 40.0)], state), [True])


# How far apart the model and the Status bit may switch. The Bank Values reach Home Assistant
# later than the Controller acts on them (10:32, 17:03), and while M1 fell on the evening of
# 2026-10-09 the Controller switched up to 0.2 °C from the model (20:59 to 01:20, see
# docs/controller.md). Every other edge is within 2 s.
MODEL_TOLERANCE = timedelta(seconds=60)


def edges(steps):
    """(time, calling) at each step where the model's call changes, from a model that starts idle."""
    result = []
    calling = False
    for s in steps:
        if s.state.calling != calling:
            calling = s.state.calling
            result.append((s.time, calling))
    return result


class RecordedDayTest(unittest.TestCase):
    """Replays the recorded day (tools/tests/recorded.py) through the model. The day opens with
    the Status bit off, so the model starts neither calling nor stopped by Kompr.esto."""

    def setUp(self):
        self.day = recorded_day()
        self.steps = replay(self.day)
        self.status = status_runs(bits(self.day[COMPRESSOR]))

    def test_calls_when_the_status_bit_says_the_controller_called(self):
        model = edges(self.steps)
        status = [edge for run in self.status for edge in ((run.start, True), (run.end, False))]

        self.assertEqual([on for _, on in model], [on for _, on in status])
        for (model_time, _), (status_time, on) in zip(model, status):
            with self.subTest(status_time.isoformat(), on=on):
                self.assertLessEqual(abs(model_time - status_time), MODEL_TOLERANCE)

    def test_the_tank_top_cycles_between_about_49_and_52_at_3_to_5_degrees_outside(self):
        tops = numbers(self.day[TANK_TOP])
        outdoor = numbers(self.day[OUTDOOR])
        night = [(when, on) for when, on in edges(self.steps) if 3 <= value_at(outdoor, when) <= 5]

        # The runs from 02:46 to 08:45 on 2026-10-10.
        self.assertEqual(len(night), 10)
        for when, on in night:
            with self.subTest(when.isoformat(), on=on):
                self.assertAlmostEqual(value_at(tops, when), 49 if on else 52, delta=0.5)

    def test_the_kompr_esto_stop_ends_the_1422_run_with_the_tank_top_still_calling(self):
        at_stop = [s.state for s in self.steps if s.time <= local("10-09 14:33:02")][-1]

        self.assertEqual(at_stop, State(tank_top_call=True, kompr_esto_stop=True, calling=False))


if __name__ == "__main__":
    unittest.main()
