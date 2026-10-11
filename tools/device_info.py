"""Print the Node's ESPHome version, compile time and name, to tell which build it runs.

Usage: python3 tools/device_info.py, with the Python that has ESPHome installed (for aioesphomeapi).
The Node's address and API key come from secrets.yaml; see tools/README.md."""
import argparse
import sys
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.node import Node  # noqa: E402


def describe(info):
    """A DeviceInfo's ESPHome version, compile time and name, on one line."""
    return "esphome %s | compiled %s | name %s" % (info.esphome_version, info.compilation_time, info.name)


def summary(node):
    return describe(node.device_info()) + "\n"


def main(argv=None):
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args(argv)
    sys.stdout.write(summary(Node()))


if __name__ == "__main__":
    main()
