import unittest
from dataclasses import replace
from datetime import timedelta

from tools.controller import (SAHKOVASTUS, L1Settings, Settings, State, Temperatures,
                              autumn_dry_active, l1_curve, l1_setpoint, outdoor_average, step,
                              thresholds)
from tools.plant import COMPRESSOR, OUTDOOR, TANK_TOP, bits, numbers, replay, value_at
from tools.runs import status_runs
from tools.tests.recorded import local, recorded_day

# The settings on 2026-10-10 (#24 Notes, docs/controller.md).
OCTOBER = Settings(var_yla_kesa=50, var_yla_talvi=55, varaaja_yla_ero=3, varaaja_ala_ero=5,
                   var_yla_ero_sv=5, kompr_esto=51, ml_ohjaustapa=0)
# Circuit L1's settings from 2026-10-27 18:48 (docs/controller.md).
L1 = L1Settings(curve_minus20=36, curve_zero=31, curve_plus20=21, min_limit=20, max_limit=65,
                night_effect=0, autumn_dry=3, out_temp_delay=2)


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

        self.assertEqual(replace(at_stop, last_run_end=None),
                         State(tank_top_call=True, kompr_esto_stop=True, calling=False))
        self.assertEqual(at_stop.last_run_end.strftime("%H:%M"), "14:33")


# The ML settings from 2026-10-26 (docs/controller.md): VaraajaYlä 54.75 at 6 °C outside, so the
# tank top starts below 49.75 and stops above 54.75.
NOVEMBER = Settings(var_yla_kesa=53, var_yla_talvi=58, varaaja_yla_ero=5, varaaja_ala_ero=5,
                    var_yla_ero_sv=5, kompr_esto=51, ml_ohjaustapa=1, varaaja_ala_min=32)


def middle_calls(readings, l1=28.0, state=State(), start=local("11-01 03:00:00")):
    """Steps the model through (minutes, M9, M4, M10) readings at 6 °C outside and returns whether
    it called after each, and the last State."""
    calls = []
    for minutes, top, middle, bottom in readings:
        reading = Temperatures(outdoor=6, tank_top=top, tank_bottom=bottom, tank_middle=middle)
        state = step(NOVEMBER, reading, state, l1, start + timedelta(minutes=minutes))
        calls.append(state.calling)
    return calls, state


class TankMiddleTest(unittest.TestCase):
    def test_thresholds_take_the_highest_term(self):
        low = thresholds(NOVEMBER, 6, l1=28)  # L1 + 5 − 5 = 28 is under VaraajaAlaMin 32
        high = thresholds(NOVEMBER, 6, l1=35)

        self.assertEqual((low.middle_start, low.bottom_stop), (32, 37))  # VaraajaAlaMin, + VaraajaAlaEro
        self.assertEqual((high.middle_start, high.bottom_stop), (35, 40))  # L1 + 5 − 5, L1 + 5

    def test_no_middle_thresholds_without_an_l1_setpoint_or_varaaja_ala_min(self):
        self.assertIsNone(thresholds(NOVEMBER, 6).middle_start)
        self.assertIsNone(thresholds(OCTOBER, 6, l1=28).bottom_stop)

    def test_m4_below_varaaja_ala_min_starts_a_run_with_the_tank_top_full_enough(self):
        # The night runs of 2026-10-30 to 2026-11-02 started this way, at M4 31.7 to 31.8.
        calls, _ = middle_calls([(0, 52.3, 32.1, 31.0), (1, 52.3, 31.8, 31.0)])

        self.assertEqual(calls, [False, True])

    def test_the_run_goes_on_past_the_bottom_stop_until_the_tank_top_is_full(self):
        # On those nights M10 passed 37 °C some 20 min in, and the run ended at VaraajaYlä.
        calls, _ = middle_calls([(0, 52.3, 31.8, 31.0), (20, 52.8, 40.0, 37.5), (60, 54.6, 47.0, 47.8),
                                 (70, 54.8, 48.0, 48.2)])

        self.assertEqual(calls, [True, True, True, False])

    def test_a_tank_top_run_goes_on_until_the_bottom_is_past_its_stop(self):
        calls, _ = middle_calls([(0, 49.5, 45.0, 34.0), (30, 54.8, 46.0, 36.5), (31, 54.8, 46.0, 37.1)])

        self.assertEqual(calls, [True, True, False])

    def test_waits_5_minutes_after_a_run_before_a_tank_middle_start(self):
        _, after_run = middle_calls([(0, 49.5, 45.0, 40.0), (30, 54.8, 46.0, 48.0)])

        calls, _ = middle_calls([(34, 54.0, 31.5, 31.0), (35, 54.0, 31.5, 31.0)], state=after_run)

        self.assertEqual(calls, [False, True])

    def test_records_when_the_run_ended(self):
        _, state = middle_calls([(0, 49.5, 45.0, 40.0), (30, 54.8, 46.0, 48.0)])

        self.assertEqual(state.last_run_end, local("11-01 03:30:00"))


class L1CurveTest(unittest.TestCase):
    def test_runs_straight_between_the_three_points_and_flat_beyond(self):
        cases = {30: 21, 20: 21, 10: 26, 5.6: 28.2, 0: 31, -10: 33.5, -20: 36, -30: 36}
        for outdoor, expected in cases.items():
            with self.subTest(outdoor=outdoor):
                self.assertAlmostEqual(l1_curve(L1, outdoor), expected)


class L1SetpointTest(unittest.TestCase):
    def test_is_the_curve_when_nothing_else_applies(self):
        self.assertAlmostEqual(l1_setpoint(L1, 5.6), 28.2)

    def test_syyskuivaus_adds_its_setting(self):
        self.assertAlmostEqual(l1_setpoint(L1, 5.6, autumn_dry=True), 31.2)

    def test_the_night_setback_subtracts_its_setting(self):
        setback = replace(L1, night_effect=5)

        self.assertAlmostEqual(l1_setpoint(setback, 5.6, night=True), 23.2)
        self.assertAlmostEqual(l1_setpoint(setback, 5.6), 28.2)

    def test_the_limits_apply_after_everything_else(self):
        tight = replace(L1, min_limit=25, max_limit=30, night_effect=10)

        self.assertEqual(l1_setpoint(tight, 5.6, night=True), 25)  # 18.2 raised to Minimiraja
        self.assertEqual(l1_setpoint(tight, -20, autumn_dry=True), 30)  # 39 cut to Maksimiraja


def at(text):
    return local("11-01 " + text)


class OutdoorAverageTest(unittest.TestCase):
    readings = [(at("10:00:00"), 4.0), (at("11:00:00"), 6.0), (at("11:30:00"), 8.0)]

    def test_weights_each_reading_by_how_long_it_held_in_the_window(self):
        # 12:00 over 2 h: 4 °C for 1 h, 6 °C for 30 min, 8 °C for 30 min.
        self.assertAlmostEqual(outdoor_average(self.readings, at("12:00:00"), 2), 5.5)

    def test_counts_the_reading_from_before_the_window_from_the_window_start(self):
        # 12:30 over 2 h: 4 °C from 10:30 to 11:00, 6 °C to 11:30, 8 °C to 12:30.
        self.assertAlmostEqual(outdoor_average(self.readings, at("12:30:00"), 2), 6.5)

    def test_averages_from_the_first_reading_when_the_window_starts_before_it(self):
        # 11:00 over 2 h: only 4 °C, from 10:00.
        self.assertAlmostEqual(outdoor_average(self.readings, at("11:00:00"), 2), 4.0)

    def test_zero_hours_is_the_last_reading(self):
        self.assertEqual(outdoor_average(self.readings, at("11:45:00"), 0), 8.0)

    def test_ignores_readings_after_the_time(self):
        self.assertEqual(outdoor_average(self.readings, at("10:30:00"), 2), 4.0)

    def test_none_before_the_first_reading(self):
        self.assertIsNone(outdoor_average(self.readings, at("09:00:00"), 2))


class AutumnDryTest(unittest.TestCase):
    warm = [10.0] * 20

    def test_switches_on_when_the_mean_falls_below_7_after_20_warm_days(self):
        self.assertFalse(autumn_dry_active(self.warm))
        self.assertTrue(autumn_dry_active(self.warm + [6.0]))

    def test_needs_20_warm_days_in_a_row(self):
        self.assertFalse(autumn_dry_active([10.0] * 19 + [6.0]))
        self.assertFalse(autumn_dry_active([10.0] * 10 + [6.0] + [10.0] * 10 + [6.0]))

    def test_lasts_20_cold_days_and_skips_the_warm_ones_between(self):
        cold = [6.0] * 19

        self.assertTrue(autumn_dry_active(self.warm + cold))
        self.assertTrue(autumn_dry_active(self.warm + cold[:10] + [9.0] * 5 + cold[10:]))
        self.assertFalse(autumn_dry_active(self.warm + cold + [6.0]))


if __name__ == "__main__":
    unittest.main()
