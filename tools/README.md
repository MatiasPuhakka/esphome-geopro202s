# tools

Scripts for watching and analysing the heat pump through Home Assistant. They use plain Python 3.11 or newer and need nothing installed.

## Home Assistant client

`tools/ha.py` is the one client the tools share. It only sends GET requests.

- **Token:** read from `ACCESS_TOKEN` in the `.env` at the repo root, wherever you run from. Set `GEOPRO_ENV_FILE` to the path of another `.env`, for example from a worktree that has none. The token never comes from an argument and the client never prints it.
- **Address:** `HA_URL` in the same `.env`, or the LAN address `http://192.168.1.159:8123` if unset.
- **Time:** times without an offset are Finnish time (Europe/Helsinki), and every time the client returns is in Finnish time.

```python
from tools.ha import HomeAssistant

ha = HomeAssistant()
ha.states()                                   # every entity
ha.state("sensor.geopro_maaliuos")            # one entity
h = ha.history(["sensor.geopro_maaliuos"], "2026-10-10 00:00", "2026-10-11 00:00")
h.window()                                    # "2026-10-10 00:00:00+03:00 -> 2026-10-11 00:00:00+03:00 Europe/Helsinki"
h.series["sensor.geopro_maaliuos"]            # rows: state, last_changed
```

`history()` always sends an encoded `end_time` (now if you give none), because without one Home Assistant returns only the first day after the start. It asks for minimal rows without attributes unless you pass `attributes=True`. Even then Home Assistant leaves out the attributes an integration marks as unrecorded: the Nord Pool sensor's history keeps `current_price` for each quarter hour, but its `raw_today` and `raw_tomorrow` price lists are only in the current state (`ha.state(...)`).

## Entry points

`day_run.py` summarises a window of history for every `geopro_` entity: state changes, unavailable or unknown states, and the first and last value.

```sh
python3 tools/day_run.py "2026-10-10 00:00"            # until now
python3 tools/day_run.py 2026-10-09T19:21:30+03:00 --end 2026-10-10T19:21:30+03:00
```

## Tests

```sh
make tools-test
```

The tests run offline against JSON recorded from Home Assistant on 2026-10-10 and trimmed in `tests/fixtures/`. Fixtures must hold no token, no `context` (context and user IDs) and nothing beyond the entities a test needs; `test_fixtures.py` checks the first two.
