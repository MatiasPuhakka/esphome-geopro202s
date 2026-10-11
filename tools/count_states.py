"""Subscribe to the Node's states for some seconds and count the messages per entity.

Shows that every entity still publishes, which Home Assistant's history can't show for an
unchanged value. The first message for each entity is its current state, sent on subscribing.

Usage: python3 tools/count_states.py SECONDS, with the Python that has ESPHome installed (for
aioesphomeapi). The Node's address and API key come from secrets.yaml; see tools/README.md."""
import argparse
import sys
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.node import Node  # noqa: E402


def summary(node, seconds):
    counts = node.count_states(seconds)
    lines = ["%-32s %3d" % (name, counts[name]) for name in sorted(counts)]
    silent = [name for name, count in counts.items() if count == 0]
    lines.append("entities: %d | with no state message: %s" % (len(counts), silent or "none"))
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("seconds", type=float, help="how long to listen, such as 75")
    args = parser.parse_args(argv)
    sys.stdout.write(summary(Node(), args.seconds))


if __name__ == "__main__":
    main()
