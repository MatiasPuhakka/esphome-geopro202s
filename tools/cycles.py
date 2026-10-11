"""List compressor and heater runs over a window, with the Controller model beside each one.

Prints the window, the ML settings and their changes, then per compressor run: its Status-bit
start and end, the starts and breaks the phase currents show, M9, M4, M10 and M1, and the model's
thresholds and call. Then the heater's Status-bit runs.

Usage: python3 tools/cycles.py START [--end END]
START and END are ISO 8601 times; one without an offset is Finnish time. END defaults to now."""
import argparse
import sys
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.ha import HomeAssistant  # noqa: E402
from tools.plant import (COMPRESSOR, HEATER, MODEL_INPUTS, OUTDOOR, PHASES, SETTING_KEYS, SETTINGS,  # noqa: E402
                         TANK_BOTTOM, TANK_MIDDLE, TANK_TOP, bits, compressor_runs, numbers, replay,
                         value_at)
from tools.runs import overlaps, status_runs  # noqa: E402


def _settings_lines(series):
    lines = ["== settings"]
    for field, key in SETTING_KEYS.items():
        rows = series.get(SETTINGS[field], [])
        changes = [r for i, r in enumerate(rows) if i == 0 or r["state"] != rows[i - 1]["state"]]
        times = [when for when, _ in numbers(changes)]
        lines.append("%-12s %s" % (key, ", ".join(
            "%s from %s" % (r["state"], when.strftime("%m-%d %H:%M")) for r, when in zip(changes, times))))
    return lines


def _span_text(span, window_end):
    """Start, end and minutes of a run; one still on runs to the window's end."""
    end = span.end or window_end
    return "%s -> %s %5.1f min" % (span.start.strftime("%m-%d %H:%M:%S"),
                                   span.end.strftime("%H:%M:%S") if span.end else "(still on)",
                                   (end - span.start).total_seconds() / 60)


def _model_text(steps, model_calls, run):
    before = [s.thresholds for s in steps if s.time <= run.start]
    if not before:
        return "model: no reading"
    t = before[-1]
    overlapping = [c for c in model_calls if overlaps(c, run.start, run.end)]
    called = ("calls %s -> %s" % (overlapping[0].start.strftime("%H:%M:%S"),
                                  overlapping[0].end.strftime("%H:%M:%S") if overlapping[0].end else "")
              if overlapping else "no call")
    return "model: start below %.2f, stop above %.2f, %s" % (t.start, t.stop, called)


def _temperature(series, entity_id, when):
    value = value_at(numbers(series.get(entity_id, [])), when)
    return "-" if value is None else "%.1f" % value


def report(client, start, end=None):
    history = client.history([COMPRESSOR, HEATER, *MODEL_INPUTS, TANK_MIDDLE, *PHASES], start, end)
    series = history.series
    steps = replay(series)
    model_calls = status_runs([(s.time, s.state.calling) for s in steps])
    found = compressor_runs(history)

    lines = ["window " + history.window()] + _settings_lines(series)
    lines.append("== compressor runs: the Status bit, with starts and breaks from the phase currents")
    previous_end = None
    for run in found:
        end_time = run.end or history.end
        off_before = "%5.1f" % ((run.start - previous_end).total_seconds() / 60) if previous_end else "    -"
        previous_end = run.end
        temperatures = "  ".join(
            "%s %s -> %s" % (name, _temperature(series, e, run.start), _temperature(series, e, end_time))
            for name, e in (("M9", TANK_TOP), ("M4", TANK_MIDDLE), ("M10", TANK_BOTTOM)))
        lines.append("%s, off before %s | starts %d breaks %d | %s  M1 %s | %s" % (
            _span_text(run, history.end), off_before, len(run.starts), len(run.breaks), temperatures,
            _temperature(series, OUTDOOR, run.start), _model_text(steps, model_calls, run)))
    lines.append("== heater runs: the Status bit")
    for run in status_runs(bits(series.get(HEATER, []))):
        lines.append(_span_text(run, history.end))
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("start", help="ISO 8601 time; without an offset it is Finnish time")
    parser.add_argument("--end", help="ISO 8601 time (default: now)")
    args = parser.parse_args(argv)
    sys.stdout.write(report(HomeAssistant(), args.start, args.end))


if __name__ == "__main__":
    main()
