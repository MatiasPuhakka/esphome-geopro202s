"""List the gaps between compressor runs over a window: how long a full tank carried the house.

Prints one row per gap between two Status-bit runs: when it began, its length, M1 averaged over
it, how fast M9, M4 and M10 fell, the fastest M9 fall in 10 minutes (a hot water draw shows as
a fast one), and M9 and M4 when the next run started. M4 and M10 are read from 10 minutes after
the run ends, once the water in the tank has settled. Then a summary per outdoor band, with the
gaps where the DHW circulation pump was off for most of the gap apart from the rest: the pump
cools the tank top, and since 2026-10-27 it is off from 22:00 to 07:00 (dhw/kiertotesti.py in
the home-assistant repo).

Usage: python3 tools/gaps.py START [--end END]
START and END are ISO 8601 times; one without an offset is Finnish time. END defaults to now."""
import argparse
import statistics
import sys
from datetime import timedelta
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.controller import outdoor_average  # noqa: E402
from tools.ha import HomeAssistant  # noqa: E402
from tools.plant import COMPRESSOR, OUTDOOR, TANK_BOTTOM, TANK_MIDDLE, TANK_TOP, bits, numbers, value_at  # noqa: E402
from tools.runs import status_runs  # noqa: E402

SETTLE = timedelta(minutes=10)  # after a run, before M4 and M10 are read
DRAW_WINDOW = timedelta(minutes=10)  # the span the fastest M9 fall is measured over
# The DHW circulation pump's switch, from the home-assistant repo.
CIRCULATION = "switch.kv_kierto_switch"
BAND = 2  # °C, the width of an outdoor band in the summary


def _known(rows):
    return [(when, value) for when, value in numbers(rows) if value is not None]


def _fall_per_hour(series, start, end):
    first, last = value_at(series, start), value_at(series, end)
    hours = (end - start).total_seconds() / 3600
    if first is None or last is None or hours <= 0:
        return None
    return (first - last) / hours


def _fastest_fall(series, start, end):
    inside = [(when, value) for when, value in series if start <= when <= end]
    fastest = 0.0
    for i, (when, value) in enumerate(inside):
        later = [v for w, v in inside[i:] if w - when <= DRAW_WINDOW]
        fastest = max(fastest, value - min(later))
    return fastest


def _pump_off(pump, start, end):
    """Whether the pump was off for more than half of start to end; None if unknown."""
    share = _off_share(pump, start, end)
    return None if share is None else share > 0.5


PUMP = {True: "pump off", False: "pump on ", None: "pump ?  "}


def _off_share(pump, start, end):
    """The share of start to end that the pump was off; None if its state isn't known."""
    if value_at(pump, start) is None:
        return None
    changes = [(start, value_at(pump, start))] + [(w, on) for w, on in pump if start < w < end] + [(end, None)]
    off = sum((b[0] - a[0]).total_seconds() for a, b in zip(changes, changes[1:]) if a[1] is False)
    return off / (end - start).total_seconds()


def gaps(series):
    """One dict per gap between two finished Status-bit runs in history series."""
    top, middle, bottom = (_known(series.get(e, [])) for e in (TANK_TOP, TANK_MIDDLE, TANK_BOTTOM))
    outdoor = _known(series.get(OUTDOOR, []))
    pump = [(when, on) for when, on in bits(series.get(CIRCULATION, [])) if on is not None]
    finished = [run for run in status_runs(bits(series.get(COMPRESSOR, []))) if run.end]
    result = []
    for before, after in zip(finished, finished[1:]):
        hours = (after.start - before.end).total_seconds() / 3600
        settled = min(before.end + SETTLE, after.start)
        result.append({
            "start": before.end,
            "hours": hours,
            "pump_off": _pump_off(pump, before.end, after.start),
            "outdoor": outdoor_average(outdoor, after.start, hours),
            "m9": _fall_per_hour(top, before.end, after.start),
            "m4": _fall_per_hour(middle, settled, after.start),
            "m10": _fall_per_hour(bottom, settled, after.start),
            "draw": _fastest_fall(top, before.end, after.start),
            "m9_next": value_at(top, after.start),
            "m4_next": value_at(middle, after.start),
        })
    return result


def _number(value, form):
    return "-" if value is None else form % value


def _median(values):
    known = [v for v in values if v is not None]
    return statistics.median(known) if known else None


def report(client, start, end=None):
    history = client.history([COMPRESSOR, OUTDOOR, TANK_TOP, TANK_MIDDLE, TANK_BOTTOM, CIRCULATION], start, end)
    found = gaps(history.series)
    lines = ["window " + history.window(),
             "== gaps: start, hours, M1, fall in °C/h of M9, M4, M10, fastest M9 fall in 10 min, "
             "M9 and M4 at the next start"]
    for g in found:
        lines.append("%s %s %5.2f h  M1 %s  M9 %s  M4 %s  M10 %s  draw %s  next M9 %s M4 %s" % (
            g["start"].strftime("%m-%d %H:%M"), PUMP[g["pump_off"]], g["hours"],
            _number(g["outdoor"], "%5.1f"), _number(g["m9"], "%5.2f"), _number(g["m4"], "%5.2f"),
            _number(g["m10"], "%5.2f"), _number(g["draw"], "%.1f"), _number(g["m9_next"], "%.1f"),
            _number(g["m4_next"], "%.1f")))
    lines.append("== by outdoor band: gaps, median hours, median fall in °C/h of M9 and M4")
    bands = {}
    for g in found:
        if g["outdoor"] is not None:
            low = int(g["outdoor"] // BAND * BAND)
            bands.setdefault((low, g["pump_off"]), []).append(g)
    for (low, pump_off), members in sorted(bands.items(), key=lambda item: (item[0][0], str(item[0][1]))):
        lines.append("%+3d to %+3d °C %s %3d  %5.2f h  M9 %s  M4 %s" % (
            low, low + BAND, PUMP[pump_off], len(members),
            _median(g["hours"] for g in members), _number(_median(g["m9"] for g in members), "%.2f"),
            _number(_median(g["m4"] for g in members), "%.2f")))
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("start", help="ISO 8601 time; without an offset it is Finnish time")
    parser.add_argument("--end", help="ISO 8601 time (default: now)")
    args = parser.parse_args(argv)
    sys.stdout.write(report(HomeAssistant(), args.start, args.end))


if __name__ == "__main__":
    main()
