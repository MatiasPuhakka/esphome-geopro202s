"""Fetch Home Assistant history for some entities into a JSON file, for the analysis scripts.

Prints the window, then each entity ID and how many rows it got. The file holds Home
Assistant's minimal history rows: a list per entity, whose first row carries the entity_id.

Usage: python3 tools/fetch.py START END OUT [ENTITY ...]
START and END are ISO 8601 times; one without an offset is Finnish time. Each ENTITY is a
config key from tests/entity-contract.txt (such as brine) or an entity ID of another
integration; with none, every Node entity in the contract."""
import argparse
import json
import sys
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import contract  # noqa: E402
from tools.ha import HomeAssistant  # noqa: E402


def entity_ids(entities, entity_contract):
    """Entity IDs for config keys and entity IDs; every Node entity's if none are given."""
    if not entities:
        return entity_contract.entity_ids(entity_contract.entities)
    return [e if "." in e else entity_contract.entity_id(e) for e in entities]


def fetch(client, entities, start, end, out, entity_contract=None):
    entity_contract = entity_contract or contract.load()
    ids = entity_ids(entities, entity_contract)
    history = client.history(ids, start, end)
    # Home Assistant returns a row at the start for every entity it has, so an empty one is gone.
    entity_contract.require_ids(history.series, ids, "Home Assistant has no history for")
    with open(out, "w", encoding="utf-8") as file:
        json.dump(list(history.series.values()), file)
    lines = ["window " + history.window()]
    lines += ["%s %d" % (entity_id, len(rows)) for entity_id, rows in history.series.items()]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("start", help="ISO 8601 time; without an offset it is Finnish time")
    parser.add_argument("end", help="ISO 8601 time")
    parser.add_argument("out", help="JSON file to write")
    parser.add_argument("entities", nargs="*", help="config keys or entity IDs (default: every Node entity)")
    args = parser.parse_args(argv)
    sys.stdout.write(fetch(HomeAssistant(), args.entities, args.start, args.end, args.out))


if __name__ == "__main__":
    main()
