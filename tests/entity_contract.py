"""The Home Assistant entity contract: what each key publishes, and the Node's entity IDs.

Writes tests/entity-contract.txt from `esphome config` output; see "Home Assistant
entity contract" in the README for why.

    check KEYS_OUT NODE_OUT    fail with a diff if the contract changed (make check-contract)
    update KEYS_OUT NODE_OUT   rewrite the contract (make update-contract)
    record-ids NODE_OUT        record the Node's entity IDs from Home Assistant

KEYS_OUT and NODE_OUT are `esphome config` output for tests/all-keys.yaml and
geopro.yaml. check and update read the Register map, so they need the Python that has
ESPHome installed. record-ids reads HA_URL (such as http://homeassistant.local:8123) and
a long-lived ACCESS_TOKEN from the environment and writes tests/ha-entity-ids.txt.
"""

import datetime
import difflib
import importlib.util
import json
import os
import re
import sys
import unicodedata
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT = os.path.join(HERE, "entity-contract.txt")
ENTITY_IDS = os.path.join(HERE, "ha-entity-ids.txt")
REGISTER_MAP = os.path.join(HERE, "..", "components", "geopro_202s", "register_map.py")

# Contract field name -> the option `esphome config` prints for it.
_OPTIONS = (
    ("unit", "unit_of_measurement"),
    ("device_class", "device_class"),
    ("state_class", "state_class"),
    ("accuracy", "accuracy_decimals"),
    ("icon", "icon"),
    ("entity_category", "entity_category"),
)


def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _block(config_text, name):
    """The lines of one top-level block, without its header."""
    lines = config_text.splitlines()
    try:
        start = lines.index(name + ":") + 1
    except ValueError:
        raise ValueError(f"no top-level {name}: block in the config output") from None
    block = []
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        if line.strip():
            block.append(line)
    return block


def _scalar(text):
    """A scalar as ESPHome's YAML dumper prints it: plain, 'single' or "double" quoted."""
    if text.startswith("'"):
        if not text.endswith("'") or len(text) < 2:
            raise ValueError(f"unterminated quoted scalar: {text}")
        return text[1:-1].replace("''", "'")
    if text.startswith('"'):
        # YAML's double-quoted escapes are a superset of JSON's; the dumper only uses
        # them for control characters, which JSON reads the same way.
        return json.loads(text)
    return text


def _options(lines, indent):
    """Each `option: value` line at this indent as (option, value, deeper lines).

    The dumper wraps a long scalar onto deeper-indented lines, so for an option with
    a value the deeper lines are folded into it; for one without, they are its children.
    """
    options = []
    for line in lines:
        if _indent(line) > indent and options:
            options[-1][2].append(line)
            continue
        option, sep, value = line.strip().partition(":")
        if _indent(line) != indent or not sep:
            raise ValueError(f"can't read config output line: {line!r}")
        options.append((option, value.strip(), []))
    result = []
    for option, value, deeper in options:
        if value:
            value = _scalar(" ".join([value] + [line.strip() for line in deeper]))
            deeper = []
        result.append((option, value, deeper))
    return result


def _entities(config_text):
    """Each entity under geopro_202s: as (key, {option: value}), in config order."""
    return [
        (key, {option: value for option, value, _ in _options(children, 4) if value})
        # A key with no value opens an entity; the others are hub options like id.
        for key, value, children in _options(_block(config_text, "geopro_202s"), 2)
        if not value
    ]


def _platform(platforms, key):
    try:
        return platforms[key]
    except KeyError:
        raise ValueError(
            f"geopro_202s: {key} has no known platform. "
            "Add it to _platforms() in tests/entity_contract.py."
        ) from None


def key_lines(config_text, platforms):
    """One line per key: its platform and entity options. The config must set every key."""
    entities = _entities(config_text)
    missing = set(platforms) - {key for key, _ in entities}
    if missing:
        raise ValueError(f"the config doesn't set these Register map keys: {', '.join(sorted(missing))}")
    lines = []
    for key, options in entities:
        fields = " ".join(f"{field}={options.get(option, '-')}" for field, option in _OPTIONS)
        lines.append(f"{key}: {_platform(platforms, key)} {fields}")
    return lines


def _friendly_name(config_text):
    for option, value, _ in _options(_block(config_text, "esphome"), 2):
        if option == "friendly_name":
            return value
    return None


def entity_ids_text(states, node_name, recorded):
    """The entity IDs file: each of the Node's sensors and binary sensors in a states
    snapshot from Home Assistant, by friendly name. Keeps no state or other attribute."""
    entities = sorted(
        (state["entity_id"], state["attributes"]["friendly_name"])
        for state in states
        if state["entity_id"].split(".")[0] in ("sensor", "binary_sensor")
        and state["attributes"].get("friendly_name", "").startswith(node_name + " ")
    )
    header = (
        f"# The entity IDs Home Assistant has for the Node's entities, recorded {recorded}\n"
        "# from GET /api/states by `python3 tests/entity_contract.py record-ids NODE_OUT`.\n"
        "# entity ID<TAB>friendly name\n"
    )
    return header + "".join(f"{entity_id}\t{name}\n" for entity_id, name in entities)


def parse_entity_ids(text):
    """(entity ID, friendly name) pairs from the entity IDs file."""
    return [
        tuple(line.split("\t", 1))
        for line in text.splitlines()
        if line and not line.startswith("#")
    ]


# ESPHome's text sensors are sensors in Home Assistant.
_HA_DOMAIN = {"text_sensor": "sensor"}


def _slug(name):
    """Close to the slug Home Assistant 2026.10 builds a new entity's ID from: ä to a, ° to deg,
    every other run of characters outside a-z and 0-9 to one _."""
    text = unicodedata.normalize("NFKD", name.replace("°", "deg")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def node_lines(config_text, platforms, entity_ids):
    # Home Assistant names a Node's entity "<friendly_name> <name>" and picks its entity ID
    # once, so look the ID up by that name and the entity's platform.
    node_name = _friendly_name(config_text)
    by_name = {(entity_id.split(".")[0], name): entity_id for entity_id, name in entity_ids}
    by_slug = {}
    lines = []
    for key, options in _entities(config_text):
        platform = _platform(platforms, key)
        name = options["name"]
        full_name = f"{node_name} {name}" if node_name else name
        domain = _HA_DOMAIN.get(platform, platform)
        # Two names with one slug get one entity ID, and Home Assistant adds _2 to the second (#76).
        slug = _slug(name)
        other_key, other_name = by_slug.setdefault((domain, slug), (key, name))
        if other_key != key:
            raise ValueError(
                f'{other_key} ("{other_name}") and {key} ("{name}") would get the same Home Assistant '
                f"entity ID, ending in {slug}, and the second one a _2. Rename one (ADR 0004)."
            )
        entity_id = by_name.get((domain, full_name), "(no entity ID recorded)")
        lines.append(f"{key}: {platform} {json.dumps(name, ensure_ascii=False)} {entity_id}")
    return lines


_HEADER = """\
# The Home Assistant entity contract. Generated by `make update-contract` from
# `esphome config`; `make check-contract` fails when the generated one differs.
# Home Assistant keys each entity on its platform and name and keeps statistics in its
# unit and state class, so a change here is a Home Assistant migration.
"""


def contract_text(keys_config, node_config, platforms, entity_ids):
    return "\n".join([
        _HEADER,
        "# Every key in tests/all-keys.yaml: platform and entity options (- for unset).",
        *key_lines(keys_config, platforms),
        "",
        "# Every entity in node.yaml: platform, name and the entity ID Home Assistant has",
        "# for it, from tests/ha-entity-ids.txt.",
        *node_lines(node_config, platforms, entity_ids),
        "",
    ])


def contract_diff(committed, generated):
    """A unified diff from the committed contract to the generated one; empty if equal."""
    return "".join(difflib.unified_diff(
        committed.splitlines(keepends=True), generated.splitlines(keepends=True),
        "tests/entity-contract.txt (committed)", "generated from esphome config",
    ))


def _platforms():
    """Each entity key's platform: its entity kind in the Register map, plus the hub's
    own text sensor."""
    spec = importlib.util.spec_from_file_location("register_map", REGISTER_MAP)
    register_map = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(register_map)
    except ModuleNotFoundError as error:
        sys.exit(f"{error}. Run this with the Python that has ESPHome installed (make PYTHON=...).")
    platforms = {value.key: value.entity_kind.value for value in register_map.VALUES}
    platforms["component_revision"] = "text_sensor"
    return platforms


def _read(path):
    with open(path, encoding="utf-8") as file:
        return file.read()


def _write(path, text):
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def _generated(keys_out, node_out):
    return contract_text(_read(keys_out), _read(node_out), _platforms(), parse_entity_ids(_read(ENTITY_IDS)))


def _fetch_states():
    request = urllib.request.Request(
        os.environ["HA_URL"].rstrip("/") + "/api/states",
        headers={"Authorization": "Bearer " + os.environ["ACCESS_TOKEN"]},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def main(argv):
    command, *paths = argv or [""]
    if command == "check" and len(paths) == 2:
        diff = contract_diff(_read(CONTRACT), _generated(*paths))
        if diff:
            sys.stdout.write(diff)
            print("The Home Assistant entity contract changed. If that's intended, run "
                  "`make update-contract` and commit tests/entity-contract.txt.")
            return 1
        return 0
    if command == "update" and len(paths) == 2:
        _write(CONTRACT, _generated(*paths))
        return 0
    if command == "record-ids" and len(paths) == 1:
        node_name = _friendly_name(_read(paths[0]))
        _write(ENTITY_IDS, entity_ids_text(_fetch_states(), node_name, datetime.date.today().isoformat()))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except ValueError as error:
        sys.exit(f"entity_contract.py: {error}")
