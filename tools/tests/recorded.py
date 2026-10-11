"""The recorded day in fixtures/history_2026-10-09_day.json: Home Assistant history from
2026-10-09 09:40 to 2026-10-10 09:40 Finnish time, for the compressor and heater Status bits,
M1, M9, M4, M10, the ML settings and the Shelly 3EM phase currents.

Trimmed from a fetch of the full history: rows that repeat the previous state are gone, times
are cut to whole seconds, temperatures are rounded to 0.01 °C, and currents to 0.1 A with a row
kept only when it moves 0.5 A or more. The run detector finds the same edges in the trimmed
currents as in the full ones, to within a second."""
import json
from datetime import datetime

from tools.ha import LOCAL
from tools.tests.fakes import FIXTURES, FakeClock, ReplayHomeAssistant, client_for

DAY = "history_2026-10-09_day.json"


def recorded_day():
    """The fixture's rows per entity ID, as History.series holds them."""
    return {rows[0]["entity_id"]: rows for rows in json.loads((FIXTURES / DAY).read_text())}


def local(text):
    """A Finnish time on the recorded day, from 'MM-DD HH:MM:SS'."""
    return datetime.strptime("2026-" + text, "%Y-%m-%d %H:%M:%S").replace(tzinfo=LOCAL)


def day_client(test):
    """A client on a temporary .env whose history requests the recorded day answers."""
    # The clock only dates /api/states answers, which the cycles.py and profile.py tests don't ask for.
    client, _ = client_for(test, ReplayHomeAssistant(FakeClock("2026-10-10T09:40:00+03:00"), DAY))
    return client
