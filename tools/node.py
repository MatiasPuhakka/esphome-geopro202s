"""The one client for the Node's native API. Read only: it reads device info and subscribes
to states, and sends no commands.

Needs aioesphomeapi, which comes with ESPHome, so run it with the Python that has ESPHome
installed. The rest of the tools module needs nothing installed, so it imports
aioesphomeapi only when it connects."""
import asyncio
import collections
import contextlib
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# Names another secrets.yaml, for a worktree or checkout that has none of its own.
SECRETS_FILE_VAR = "GEOPRO_SECRETS_FILE"
# The Node's LAN address, unless secrets.yaml sets node_address.
DEFAULT_ADDRESS = "192.168.1.92"
API_PORT = 6053
CLIENT_INFO = "geopro-tools"


def secrets_file():
    """The secrets.yaml the client reads: $GEOPRO_SECRETS_FILE if set, else the one next to geopro.yaml."""
    return Path(os.environ.get(SECRETS_FILE_VAR) or REPO_ROOT / "secrets.yaml")


def _read_secrets(path):
    """The top-level `name: value` lines of a secrets.yaml, unquoted."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit("No %s. It is the secrets.yaml next to geopro.yaml; point %s at one from another checkout."
                         % (path, SECRETS_FILE_VAR)) from None
    values = {}
    for line in text.splitlines():
        if line[:1].isspace() or line.lstrip().startswith("#") or ":" not in line:
            continue
        name, value = line.split(":", 1)
        values[name.strip()] = value.strip().strip('"').strip("'")
    return values


def _api_client(address, port, key):
    import aioesphomeapi

    return aioesphomeapi.APIClient(address, port, None, noise_psk=key, client_info=CLIENT_INFO)


class Node:
    """Reads api_encryption_key, and node_address if set, from secrets.yaml, the file ESPHome
    reads the key from. The client never prints the key."""

    def __init__(self, secrets_path=None, api=_api_client):
        path = Path(secrets_path) if secrets_path else secrets_file()
        secrets = _read_secrets(path)
        if not secrets.get("api_encryption_key"):
            raise SystemExit("%s has no api_encryption_key." % path)
        self._key = secrets["api_encryption_key"]
        self.address = secrets.get("node_address") or DEFAULT_ADDRESS
        self.port = API_PORT
        self._api = api

    def __repr__(self):
        return "Node('%s:%d')" % (self.address, self.port)

    @contextlib.asynccontextmanager
    async def connected(self):
        """An aioesphomeapi APIClient, logged in, disconnected on leaving."""
        client = self._api(self.address, self.port, self._key)
        await client.connect(login=True)
        try:
            yield client
        finally:
            await client.disconnect()

    async def _with_client(self, read, *args):
        async with self.connected() as client:
            return await read(client, *args)

    def device_info(self):
        """The Node's DeviceInfo: name, esphome_version, compilation_time and the rest."""
        return asyncio.run(self._with_client(read_device_info))

    def count_states(self, seconds):
        """State messages per entity name over `seconds` after subscribing, in the Node's entity
        order. The count includes the Node's first message for each entity, its current state."""
        return asyncio.run(self._with_client(count_state_messages, seconds))


# The reads on a client from Node.connected(), for a caller that does several in one connection.
async def read_device_info(client):
    return await client.device_info()


async def count_state_messages(client, seconds):
    entities, _ = await client.list_entities_services()
    counts = collections.Counter()
    client.subscribe_states(lambda state: counts.update([state.key]))
    await asyncio.sleep(seconds)
    return {e.name: counts[e.key] for e in entities}
