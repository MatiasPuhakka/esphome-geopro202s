"""The one Home Assistant client for the tools. Read only: it sends GET requests and nothing else."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parent.parent
# Names another .env, for a worktree or checkout that has none of its own.
ENV_FILE_VAR = "GEOPRO_ENV_FILE"
# The LAN address. The public hostname sits behind Cloudflare Access, which a token can't pass.
DEFAULT_URL = "http://192.168.1.159:8123"
# Finnish time, so the offset follows daylight saving time (UTC+2 from 2026-10-25).
LOCAL = ZoneInfo("Europe/Helsinki")


def local_time(value):
    """A datetime or ISO 8601 text as Finnish time. A time without an offset is taken as Finnish."""
    when = value if isinstance(value, datetime) else datetime.fromisoformat(value)
    return when.replace(tzinfo=LOCAL) if when.tzinfo is None else when.astimezone(LOCAL)


class History:
    """History rows per entity ID, with the window they were asked for."""

    def __init__(self, start, end, series):
        self.start = start
        self.end = end
        self.series = series

    def window(self):
        return "%s -> %s %s" % (self.start.isoformat(" "), self.end.isoformat(" "), LOCAL.key)


def env_file():
    """The .env the client reads: $GEOPRO_ENV_FILE if set, else the one at the repo root."""
    return Path(os.environ.get(ENV_FILE_VAR) or REPO_ROOT / ".env")


def _read_env(path):
    try:
        text = path.read_text()
    except FileNotFoundError:
        raise SystemExit("No %s. Put ACCESS_TOKEN=<long-lived token> there, or point %s at a .env that has it."
                         % (path, ENV_FILE_VAR)) from None
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _urlopen(url, headers):
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as response:
        return response.read()


class HomeAssistant:
    """Reads the token, and HA_URL if set, from a .env file. The token never comes from an
    argument, so it stays out of `ps`, and the client never prints it."""

    def __init__(self, env_path=None, transport=_urlopen):
        path = Path(env_path) if env_path else env_file()
        env = _read_env(path)
        if not env.get("ACCESS_TOKEN"):
            raise SystemExit("%s has no ACCESS_TOKEN." % path)
        self._token = env["ACCESS_TOKEN"]
        self.url = env.get("HA_URL", DEFAULT_URL).rstrip("/")
        self._transport = transport

    def __repr__(self):
        return "HomeAssistant(%r)" % self.url

    def _get(self, path):
        headers = {"Authorization": "Bearer " + self._token}
        return json.loads(self._transport(self.url + path, headers))

    def states(self):
        return self._get("/api/states")

    def state(self, entity_id):
        return self._get("/api/states/" + urllib.parse.quote(entity_id, safe=""))

    def history(self, entity_ids, start, end=None, attributes=False):
        """Rows for each entity from start to end (now if not given).

        Always sends end_time: without it Home Assistant returns only the first day after start.
        Without attributes it asks for minimal rows, where only an entity's first row carries
        its entity_id and attributes. With attributes, Home Assistant still leaves out any the
        integration marks as unrecorded (the Nord Pool sensor's raw_today and raw_tomorrow lists)."""
        if not entity_ids:
            # An empty filter_entity_id reads as no filter at all.
            raise ValueError("history() needs at least one entity ID")
        start = local_time(start)
        end = local_time(end if end is not None else datetime.now(LOCAL).replace(microsecond=0))
        query = {"filter_entity_id": ",".join(entity_ids), "end_time": end.isoformat()}
        if not attributes:
            query.update(minimal_response="", no_attributes="")
        # quote_via=quote with safe="" encodes the "+" of an offset and the commas between IDs.
        path = "/api/history/period/%s?%s" % (
            urllib.parse.quote(start.isoformat(), safe=""),
            urllib.parse.urlencode(query, quote_via=urllib.parse.quote, safe=""))
        series = {rows[0]["entity_id"]: rows for rows in self._get(path) if rows}
        return History(start, end, series)
