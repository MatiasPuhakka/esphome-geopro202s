"""Compare the Geopro entities in two Home Assistant /api/states snapshots (before, after).

Lists entities that appeared, entities that are gone, and for the rest the state before and
after, a changed unit, and whether last_reported moved since the before snapshot. Home
Assistant skips repeated ESPHome states, so an unchanged value keeps its old last_reported.

Usage: python3 tools/compare_entities.py BEFORE.json AFTER.json
Each snapshot is the JSON of GET /api/states, such as HomeAssistant().states() writes."""
import argparse
import json
import sys


def geopro(states):
    return {s["entity_id"]: s for s in states if "geopro" in s["entity_id"]}


def _reported(state):
    return state.get("last_reported", state["last_updated"])


def compare(before_states, after_states):
    before, after = geopro(before_states), geopro(after_states)
    lines = ["new entity ids: %s" % (sorted(set(after) - set(before)) or "none"),
             "missing from after: %s" % (sorted(set(before) - set(after)) or "none")]
    for entity_id in sorted(set(before) & set(after)):
        b, a = before[entity_id], after[entity_id]
        if a["state"] == "unavailable":
            flag = "   <-- UNAVAILABLE"
        elif _reported(a) > _reported(b):
            flag = ""
        else:
            flag = "   <-- not updated"
        unit_b = b["attributes"].get("unit_of_measurement", "")
        unit_a = a["attributes"].get("unit_of_measurement", "")
        unit = "" if unit_a == unit_b else "  unit %s -> %s" % (unit_b, unit_a)
        # The original padded the after state, so lines without a flag ended in spaces.
        lines.append(("%-48s %10s -> %-10s%s%s" % (entity_id, b["state"][:10], a["state"][:10], unit, flag)).rstrip())
    return "\n".join(lines) + "\n"


def _read(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("before", help="states snapshot from before")
    parser.add_argument("after", help="states snapshot from after")
    args = parser.parse_args(argv)
    sys.stdout.write(compare(_read(args.before), _read(args.after)))


if __name__ == "__main__":
    main()
