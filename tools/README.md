# tools

Scripts for watching and analysing the heat pump through Home Assistant, and for reading the Node directly. They use plain Python 3.11 or newer and need nothing installed, except that the Node client needs `aioesphomeapi`, which comes with ESPHome.

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

## Entity IDs

`tools/contract.py` reads the Node's entities from `tests/entity-contract.txt` (see "Home Assistant entity contract" in the repo README): each config key's platform, name, Home Assistant entity ID, unit and classes. Tools ask for an entity by its config key, never by a hard-coded entity ID, and `test_contract.py` fails on a `geopro_` entity ID in tools code.

```python
from tools import contract

c = contract.load()
c.entity_id("brine")                          # the entity ID the contract records for brine
c.entity("brine").unit                        # "°C"; also platform, name, device_class, state_class
c.require(ha.states(), ["brine", "compressor"])   # fails, naming each missing entity
```

A key the contract doesn't have, an entity with no recorded ID, or an entity Home Assistant doesn't have stops the tool with a `ContractError` that names the key, the entity ID and how to record the IDs again.

## Node client

`tools/node.py` is the one client for the Node's native API. It reads device info and counts state messages, and sends no commands. Run it with the Python that has ESPHome installed, such as the venv in `.scratch/esphome-2026.9.1`.

- **API key:** `api_encryption_key` in the `secrets.yaml` next to `geopro.yaml`, the file ESPHome reads it from, wherever you run from. Set `GEOPRO_SECRETS_FILE` to the path of another one, for example from a worktree that has none. The client never prints the key.
- **Address:** `node_address` in the same `secrets.yaml`, or the LAN address `192.168.1.92` if unset. The port is 6053.

```python
from tools.node import Node

node = Node()
node.device_info()                            # aioesphomeapi DeviceInfo: esphome_version, compilation_time, name
node.count_states(75)                         # {entity name: state messages in 75 s}
```

The count includes the first message for each entity, which the Node sends on subscribing with the current state. Each of the two methods opens its own connection; to do both in one, use `read_device_info(client)` and `count_state_messages(client, seconds)` inside `async with node.connected() as client:`.

## Entry points

Each runs from any directory.

`flash_check.py` checks a flash of the Node in three phases, one command each; `docs/agents/verification.md` says when to run which. Each prints a report and exits with status 1 when a check fails.

```sh
python3 tools/flash_check.py before                                   # before flashing
.scratch/esphome-2026.9.1/bin/python tools/flash_check.py after       # after flashing; needs aioesphomeapi
python3 tools/flash_check.py overnight                                # the next morning
```

- `before` saves Home Assistant's states.
- `after` counts the Node's state messages for 75 s (`--seconds`), then saves Home Assistant's states and checks both against `tests/entity-contract.txt`. `verification.md` lists what fails it. The expected revision is what a local build of this checkout stamps; `--revision` names another commit or ref.
- `overnight` runs `day_run.py`'s summary for the contract's entities from the time the after phase ran (`--start`, `--end`), and fails on any unavailable or unknown state.

The phases keep `states-before.json`, `states-after.json` and `times.json` in `.scratch/flash-check/` (`--dir`). Running `before` again starts a new check.

`day_run.py` summarises a window of history for every `geopro_` entity: state changes, unavailable or unknown states, and the first and last value.

```sh
python3 tools/day_run.py "2026-10-10 00:00"            # until now
python3 tools/day_run.py 2026-10-09T19:21:30+03:00 --end 2026-10-10T19:21:30+03:00
```

`run_watch.py` watches one compressor run: the Controller's call starting and ending, compressor current breaks on the Shelly phases while the Controller keeps calling, the heater, and a run summary. It appends every 2 s sample to a file and stops after a call of 5 minutes or more, or after 3 hours.

```sh
python3 tools/run_watch.py .scratch/run.log
```

`fetch.py` writes Home Assistant history for some entities to a JSON file, for analysis. Name an entity by its config key, or by entity ID for another integration's entity such as a Shelly phase; with none it fetches every Node entity.

```sh
python3 tools/fetch.py 2026-10-09T00:00 2026-10-10T00:00 .scratch/geopro.json
python3 tools/fetch.py 2026-10-09T00:00 2026-10-10T00:00 .scratch/run.json compressor tank_top sensor.shellyem3_34945474817a_channel_a_current
```

`compare_entities.py` compares the Geopro entities in two `/api/states` snapshots, such as one from before a flash and one from after: entities that appeared or went missing, and for each of the rest its state, a changed unit, and whether it reported since.

```sh
python3 tools/compare_entities.py .scratch/flash-check/states-before.json .scratch/flash-check/states-after.json
```

`device_info.py` prints the Node's ESPHome version, compile time and name. `count_states.py` subscribes to the Node's states and counts the messages per entity, which shows that every entity still publishes when Home Assistant's history can't. Both need `aioesphomeapi`.

```sh
.scratch/esphome-2026.9.1/bin/python tools/device_info.py
.scratch/esphome-2026.9.1/bin/python tools/count_states.py 75
```

`cycles.py` lists the compressor runs in a window, each with its starts and breaks, M9, M4 and M10 at its ends, M1, and the Controller model's thresholds and call beside it. Then it lists the heater's runs.

```sh
python3 tools/cycles.py "2026-10-10 00:00" --end "2026-10-10 09:40"
```

`profile.py` prints M1, M9, M4 and M10, the compressor Status bit, the model's call, the highest current on the lowest phase and the compressor starts, one row per slot. Both scripts count starts the same way, with no start for a compressor already drawing when the window opens.

```sh
python3 tools/profile.py "2026-10-10 04:00" "2026-10-10 05:00" --step 5
```

Both replace the `.scratch/cycles/scripts/` versions, which read saved history files. They fetch through the client instead, and drop the columns the model doesn't use: M7, brine, L1 supply and the hour counters. `profile.py` no longer prints a row for the slot that starts at END.


`check_manual_links.py` checks that every link to a manual page anchor, such as the `#s21` of page 21 in `manuals/kasikirja.md`, points at a manual and anchor that exist (ADR 0006). It prints each broken link with its file and line and exits with status 1 if there is one. CI runs it as `make check-manual-links`.

```sh
python3 tools/check_manual_links.py
```

## Controller model and run detector

Both are pure: no Home Assistant, no clock. `plant.py` looks up the entities they read in the contract and turns history rows into their inputs.

- `controller.py` follows `docs/controller.md`. Settings and M1, M9 and M10 in; VaraajaYlä, the start, stop, heater and restart thresholds, and whether the Controller should be calling for the compressor out. It models the tank-top start and stop, the Kompr.esto stop and restart, and ML Ohjaustapa Sähkövastus. It leaves out the tank-middle start and the tank-bottom stop, because they need the L1 setpoint, which the Component doesn't read.
- `runs.py` takes the compressor Status bit and the three Shelly phase currents and finds runs, starts and breaks (see CONTEXT.md). The currents alone can't tell the compressor from the sauna or S1, which also draw 4 A or more on every phase, so it counts only the current inside a Status-bit run.

On the recorded day the model calls within a minute of every Status-bit edge, and the phase currents start and end every run within the 10 s value interval.

## Retired scripts

These log scrapers in `.scratch/` match log formats the Node no longer writes: ESPHome 2025.2.2's "Sending state" lines and the YAML protocol copy's lines. They have no port here, and deleting them is up to the owner.

- `.scratch/live/scripts/jv_watch.py`
- `.scratch/live/scripts/step_watch.py`
- `.scratch/live/scripts/summary.py`
- `.scratch/live/scripts/summary_quiet.py`
- `.scratch/alarm11/scripts/series.py`

`run_watch.py`, `fetch.py`, `compare_entities.py`, `count_states.py`, `device_info.py`, `cycles.py` and `profile.py` in `.scratch/` have their ports above, and `day_run.py` has had one since #42.

## Tests

```sh
make tools-test
```

The tests run offline against JSON recorded from Home Assistant and the Node and trimmed in `tests/fixtures/`:

- `states.json`, `history_day.json` and `history_nordpool.json`: Home Assistant on 2026-10-10.
- `states_before_flash.json` and `states_after_flash.json`: the Geopro entities in the states snapshots from before and after the first flash in #11, on 2026-10-09.
- `history_run_watch.json`: history for the entities `run_watch.py` reads, in two windows of 2026-10-09 (10:31 to 10:39 and 18:37 to 18:56 Finnish time). `ReplayHomeAssistant` in `fakes.py` answers from it as Home Assistant would have at a fake clock's time.
- `history_2026-10-09_day.json`: the recorded day for the model and the run detector, 2026-10-09 09:40 to 2026-10-10 09:40, with the compressor and heater Status bits, M1, M9, M4, M10, the ML settings and the phase currents. `tests/recorded.py` says how it was trimmed. `ReplayHomeAssistant` serves it to the `cycles.py` and `profile.py` tests.
- `node_session.json`: the Node's entities and 75 s of its state messages after the #11 flash, taken from its log. `RecordedNode` in `fakes.py` stands in for `aioesphomeapi` with it.

`tests/expected/` holds what the scripts in `.scratch/` printed for these fixtures before they moved here, and the ports must print the same. Fixtures must hold no token, key or password, no `context` (context and user IDs), and nothing beyond the entities a test needs; `test_fixtures.py` checks the first two.
