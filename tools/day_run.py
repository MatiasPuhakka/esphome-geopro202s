"""Summarise Home Assistant history for the Geopro entities over a window.

Prints the window, then per entity: state changes, unavailable/unknown count, first and last value.

Usage: python3 tools/day_run.py START [--end END]
START and END are ISO 8601 times; one without an offset is Finnish time. END defaults to now."""
import argparse
import sys
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.ha import HomeAssistant  # noqa: E402

MISSING_STATES = ("unavailable", "unknown")


def geopro_ids(states):
    return sorted(s["entity_id"] for s in states if s["entity_id"].split(".", 1)[1].startswith("geopro_"))


def summary(client, start, end=None):
    ids = geopro_ids(client.states())
    if not ids:
        raise SystemExit("Home Assistant has no geopro_ entities.")
    history = client.history(ids, start, end)
    lines = ["window " + history.window()]
    missing_total = 0
    for entity_id in sorted(history.series):
        values = [row["state"] for row in history.series[entity_id]]
        missing = sum(v in MISSING_STATES for v in values)
        missing_total += missing
        lines.append("%-44s changes %4d  unavailable %d  %s -> %s"
                     % (entity_id, len(values) - 1, missing, values[0][:8], values[-1][:8]))
    lines.append("entities: %d | unavailable/unknown states: %d" % (len(history.series), missing_total))
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("start", help="ISO 8601 time; without an offset it is Finnish time")
    parser.add_argument("--end", help="ISO 8601 time (default: now)")
    args = parser.parse_args(argv)
    sys.stdout.write(summary(HomeAssistant(), args.start, args.end))


if __name__ == "__main__":
    main()
