"""The Node's entities as tests/entity-contract.txt records them: each config key's platform,
name, Home Assistant entity ID, unit and classes. Tools look entity IDs up here by key, so a
renamed entity stops a tool with its key and ID named, instead of showing up as a failing read
or an empty column."""
import json
import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT = REPO_ROOT / "tests" / "entity-contract.txt"
# What tests/entity_contract.py writes for an entity with no ID in tests/ha-entity-ids.txt.
NO_ENTITY_ID = "(no entity ID recorded)"
# How to record the IDs again, from "Home Assistant entity contract" in the README.
RECORD_IDS = ("record them with `python3 tests/entity_contract.py record-ids build/node-config.out` "
              "and `make update-contract` (README, \"Home Assistant entity contract\")")

# A key's options: "KEY: PLATFORM unit=... device_class=... entity_category=...", "-" for unset.
_KEY_LINE = re.compile(r"^(\w+): (\w+) (unit=.*)$")
# One of the Node's entities: "KEY: PLATFORM "NAME" ENTITY_ID", the name JSON-quoted.
_NODE_LINE = re.compile(r'^(\w+): (\w+) ("(?:[^"\\]|\\.)*") (.+)$')


class ContractError(SystemExit):
    """The contract doesn't have an entity a tool needs, or Home Assistant doesn't."""


@dataclass(frozen=True)
class Entity:
    key: str
    platform: str
    name: str
    entity_id: str | None
    unit: str | None = None
    device_class: str | None = None
    state_class: str | None = None
    accuracy: str | None = None
    icon: str | None = None
    entity_category: str | None = None


class Contract:
    def __init__(self, entities, path):
        # The Node's entities by key, in geopro.yaml's order.
        self.entities = entities
        self.path = path

    def entity(self, key):
        try:
            return self.entities[key]
        except KeyError:
            raise ContractError("%s has no Node entity with the key %s." % (self.path, key)) from None

    def entity_id(self, key):
        entity = self.entity(key)
        if entity.entity_id is None:
            raise ContractError("%s has no Home Assistant entity ID for %s (\"%s\"); %s."
                                % (self.path, key, entity.name, RECORD_IDS))
        return entity.entity_id

    def entity_ids(self, keys):
        return [self.entity_id(key) for key in keys]

    def missing(self, states, keys=None):
        """The entities, of the given keys or all, whose ID isn't in a Home Assistant states list."""
        present = {state["entity_id"] for state in states}
        return [self.entity(key) for key in (self.entities if keys is None else keys)
                if self.entity_id(key) not in present]

    def require(self, states, keys=None):
        """Fails with every missing entity named, if Home Assistant lacks any of them."""
        keys = self.entities if keys is None else keys
        self.require_ids({state["entity_id"] for state in states}, self.entity_ids(keys))

    def require_ids(self, present, entity_ids, what="Home Assistant has no"):
        """Fails if any of the entity IDs, the contract's or another integration's, isn't in present."""
        missing = [entity_id for entity_id in entity_ids if entity_id not in present]
        if missing:
            raise self.missing_error(what, missing)

    def missing_error(self, what, entity_ids):
        """A ContractError naming each entity ID, and the key and name of those in the contract."""
        by_id = {e.entity_id: e for e in self.entities.values()}
        named = ["%s (%s, \"%s\" in %s)" % (i, by_id[i].key, by_id[i].name, self.path.name) if i in by_id else i
                 for i in entity_ids]
        return ContractError("%s %s. If an entity was renamed, %s." % (what, ", ".join(named), RECORD_IDS))


def load(path=None):
    """The Node's entities from the contract, with each key's options from its first part."""
    path = Path(path) if path else CONTRACT
    options, entities = {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        node = _NODE_LINE.match(line)
        if node:
            key, platform, name, entity_id = node.groups()
            entities[key] = (platform, json.loads(name), None if entity_id == NO_ENTITY_ID else entity_id)
            continue
        options_line = _KEY_LINE.match(line)
        if options_line:
            key, _, fields = options_line.groups()
            options[key] = {field: None if value == "-" else value
                            for field, value in (pair.split("=", 1) for pair in fields.split(" "))}
    return Contract({key: Entity(key, platform, name, entity_id, **options.get(key, {}))
                     for key, (platform, name, entity_id) in entities.items()}, path)
