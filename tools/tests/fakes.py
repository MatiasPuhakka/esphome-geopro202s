"""A recorded Home Assistant and a recorded Node for the offline tests: they answer from the
JSON in fixtures/."""
import bisect
import json
import tempfile
import types
import urllib.error
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

from tools.ha import HomeAssistant
from tools.node import Node

FIXTURES = Path(__file__).resolve().parent / "fixtures"
# What the scripts in .scratch/ printed for the fixtures before they moved here.
EXPECTED = Path(__file__).resolve().parent / "expected"
# Not a real token. The tests check that it reaches the header and nothing else.
FAKE_TOKEN = "fake-token-for-tests-0123456789"
# Not a real API encryption key either: the base64 of "fake-key-for-tests-0123456789".
FAKE_KEY = "ZmFrZS1rZXktZm9yLXRlc3RzLTAxMjM0NTY3ODk="


class RecordedHomeAssistant:
    """A transport that serves fixture files and keeps every request it was given."""

    def __init__(self):
        self.requests = []

    def __call__(self, url, headers):
        self.requests.append((url, dict(headers)))
        parts = urllib.parse.urlsplit(url)
        if parts.path == "/api/states":
            return (FIXTURES / "states.json").read_bytes()
        if parts.path.startswith("/api/states/"):
            entity_id = urllib.parse.unquote(parts.path[len("/api/states/"):])
            states = json.loads((FIXTURES / "states.json").read_text())
            return json.dumps(next(s for s in states if s["entity_id"] == entity_id)).encode()
        if parts.path.startswith("/api/history/period/"):
            ids = urllib.parse.parse_qs(parts.query)["filter_entity_id"][0]
            name = "history_nordpool.json" if "nordpool" in ids else "history_day.json"
            return (FIXTURES / name).read_bytes()
        raise AssertionError("no fixture for " + url)


class FakeClock:
    """Seconds since the epoch that move only when someone sleeps."""

    def __init__(self, start):
        self.now = datetime.fromisoformat(start).timestamp()

    def time(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class ReplayHomeAssistant:
    """A transport that answers from a recorded history file as Home Assistant would have at
    the clock's time: each entity's state then, and history rows within a window. A test can
    give the history instead of a file name: a list of rows per entity, in Home Assistant's form."""

    def __init__(self, clock, name=None, history=None):
        self.clock = clock
        self.rows = {}
        for rows in history if history is not None else json.loads((FIXTURES / name).read_text()):
            self.rows[rows[0]["entity_id"]] = [(datetime.fromisoformat(r["last_changed"]).timestamp(), r)
                                               for r in rows]

    def _at(self, entity_id, when):
        rows = self.rows[entity_id]
        return rows[max(bisect.bisect_right([t for t, _ in rows], when) - 1, 0)][1]

    def _state(self, entity_id):
        row = self._at(entity_id, self.clock.time())
        return {"entity_id": entity_id, "state": row["state"], "last_changed": row["last_changed"]}

    def __call__(self, url, headers):
        parts = urllib.parse.urlsplit(url)
        path = urllib.parse.unquote(parts.path)
        if path == "/api/states":
            return json.dumps([self._state(entity_id) for entity_id in self.rows]).encode()
        if path.startswith("/api/states/"):
            entity_id = path[len("/api/states/"):]
            if entity_id not in self.rows:
                raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
            return json.dumps(self._state(entity_id)).encode()
        if path.startswith("/api/history/period/"):
            start = datetime.fromisoformat(path[len("/api/history/period/"):]).timestamp()
            query = urllib.parse.parse_qs(parts.query)
            end = datetime.fromisoformat(query["end_time"][0]).timestamp()
            series = []
            for entity_id in query["filter_entity_id"][0].split(","):
                # The first row is the state at the start, stamped with the start time.
                first = {"entity_id": entity_id, "state": self._at(entity_id, start)["state"],
                         "last_changed": datetime.fromtimestamp(start, timezone.utc).isoformat()}
                series.append([first] + [{"state": r["state"], "last_changed": r["last_changed"]}
                                         for t, r in self.rows[entity_id] if start < t <= end])
            return json.dumps(series).encode()
        raise AssertionError("no fixture for " + url)


class TempFile:
    """A file in a temporary directory, removed when the test ends."""

    NAME = "file"

    def __init__(self, test, text):
        directory = tempfile.TemporaryDirectory()
        test.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / self.NAME
        self.path.write_text(text)


class TempEnv(TempFile):
    NAME = ".env"

    def __init__(self, test, text="ACCESS_TOKEN=%s\n" % FAKE_TOKEN):
        super().__init__(test, text)


class TempSecrets(TempFile):
    NAME = "secrets.yaml"

    def __init__(self, test, text='api_encryption_key: "%s"\nota_password: fake\n' % FAKE_KEY):
        super().__init__(test, text)


def client_for(test, transport=None):
    """A client on a temporary .env that answers from the fixtures, and its transport."""
    transport = transport or RecordedHomeAssistant()
    return HomeAssistant(env_path=TempEnv(test).path, transport=transport), transport


class RecordedNode:
    """Stands in for aioesphomeapi's APIClient, replaying fixtures/node_session.json: the Node's
    entities and 75 s of its state messages after the #11 flash, taken from its log."""

    def __init__(self):
        self.session = json.loads((FIXTURES / "node_session.json").read_text())
        self.connections = []
        self.connected = False

    def __call__(self, address, port, key):
        self.connections.append((address, port, key))
        return self

    async def connect(self, login=False):
        self.connected = True

    async def disconnect(self):
        self.connected = False

    async def device_info(self):
        return types.SimpleNamespace(**self.session["device_info"])

    async def list_entities_services(self):
        return [types.SimpleNamespace(key=e["key"], name=e["name"]) for e in self.session["entities"]], []

    def subscribe_states(self, on_state):
        # The Node first sends every entity's current state, then each publish.
        for entity in self.session["entities"]:
            on_state(types.SimpleNamespace(key=entity["key"]))
        for state in self.session["states"]:
            on_state(types.SimpleNamespace(key=state["key"]))


def node_for(test):
    """A Node client on a temporary secrets.yaml that answers from the fixtures, and its API."""
    api = RecordedNode()
    return Node(secrets_path=TempSecrets(test).path, api=api), api
