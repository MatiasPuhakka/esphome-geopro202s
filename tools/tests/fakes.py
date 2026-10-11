"""A recorded Home Assistant for the offline tests: answers from the JSON in fixtures/."""
import json
import tempfile
import urllib.parse
from pathlib import Path

from tools.ha import HomeAssistant

FIXTURES = Path(__file__).resolve().parent / "fixtures"
# Not a real token. The tests check that it reaches the header and nothing else.
FAKE_TOKEN = "fake-token-for-tests-0123456789"


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


class TempEnv:
    """A temporary directory holding a .env, removed when the test ends."""

    def __init__(self, test, text="ACCESS_TOKEN=%s\n" % FAKE_TOKEN):
        directory = tempfile.TemporaryDirectory()
        test.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / ".env"
        self.path.write_text(text)


def client_for(test):
    """A client on a temporary .env that answers from the fixtures, and its transport."""
    transport = RecordedHomeAssistant()
    return HomeAssistant(env_path=TempEnv(test).path, transport=transport), transport
