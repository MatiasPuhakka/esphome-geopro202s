"""Print the tank and the compressor every few minutes over a window.

Each row is one slot: M1, M9, M4 and M10 at its start, the compressor Status bit and the Controller
model's call at its start, the highest current on the lowest phase within it (the compressor
draws about 6 A on every phase), and the compressor starts within it, counted as cycles.py counts
them: inside a Status-bit run.

Usage: python3 tools/profile.py START END [--step MINUTES]
START and END are ISO 8601 times; one without an offset is Finnish time."""
import argparse
import sys
from datetime import timedelta
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.ha import HomeAssistant  # noqa: E402
from tools.plant import (COMPRESSOR, MODEL_INPUTS, OUTDOOR, PHASES, TANK_BOTTOM,  # noqa: E402
                         TANK_MIDDLE, TANK_TOP, bits, compressor_runs, numbers, replay, value_at)
from tools.runs import lowest_phase  # noqa: E402

COLUMNS = (OUTDOOR, TANK_TOP, TANK_MIDDLE, TANK_BOTTOM)
ON_OFF = {True: "on", False: "off", None: "-"}


def report(client, start, end, step_minutes=5):
    history = client.history([COMPRESSOR, *MODEL_INPUTS, TANK_MIDDLE, *PHASES], start, end)
    series = history.series
    status = bits(series.get(COMPRESSOR, []))
    phases = [numbers(series.get(p, [])) for p in PHASES]
    model = [(s.time, s.state.calling) for s in replay(series)]
    lowest = lowest_phase(phases)
    starts = [s for run in compressor_runs(history) for s in run.starts]
    temperatures = {e: numbers(series.get(e, [])) for e in COLUMNS}

    step = timedelta(minutes=step_minutes)
    lines = ["window " + history.window(), "time      M1    M9    M4   M10  status model  max A starts"]
    slot = history.start
    while slot < history.end:
        temps = [value_at(temperatures[e], slot) for e in COLUMNS]
        amps = [a for when, a in lowest if slot <= when < slot + step]
        lines.append("%s %s  %-6s %-6s %5s %6d" % (
            slot.strftime("%H:%M"), " ".join("%5.1f" % t if t is not None else "    -" for t in temps),
            ON_OFF[value_at(status, slot)], ON_OFF[value_at(model, slot)],
            "%.1f" % max(amps) if amps else "-", sum(slot <= s < slot + step for s in starts)))
        slot += step
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("start", help="ISO 8601 time; without an offset it is Finnish time")
    parser.add_argument("end", help="ISO 8601 time")
    parser.add_argument("--step", type=float, default=5, help="slot length in minutes (default: 5)")
    args = parser.parse_args(argv)
    sys.stdout.write(report(HomeAssistant(), args.start, args.end, args.step))


if __name__ == "__main__":
    main()
