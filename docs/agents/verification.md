# Verifying a change on the Node

Host tests and CI cover building and decoding. The Node on the real bus covers the rest. Verify any change that alters what the Node runs: the Component, `node.yaml` or the ESPHome version. Ask the owner before flashing.

The flash check in `tools/flash_check.py` runs the checks in three phases: `before`, `after` and `overnight`. Each phase prints a report and exits with status 1 when a check fails. See `tools/README.md`.

## Setup

- **ESPHome version.** `geopro.yaml` needs ESPHome 2026.9.x ([ADR 0002](../adr/0002-supported-esphome-versions.md)). The `esphome` on PATH may be another version. The make targets that run ESPHome stop and say so; point them at a 2026.9.x install with `ESPHOME=/path/to/esphome`, for example `make check-node-config ESPHOME=/path/to/esphome`. When calling ESPHome directly, run `esphome version` first.
- **Secrets.** `secrets.yaml` sits next to `geopro.yaml`, is gitignored and holds `api_encryption_key`, which the API and OTA uploads share. Never print it, paste it into a doc or commit it; `make check-secrets` fails on an inline key or password. The Home Assistant token is `ACCESS_TOKEN` in the gitignored `.env`; treat it the same way. Source it into the shell (`set -a; . ./.env; set +a`) so the value stays out of what you type and out of output.
- **Without a secrets.yaml.** `make dummy-secrets` writes one with a random API key, as CI does, and leaves an existing file alone. Then `make check-node-config check-trace-config` validates both configs and prints ESPHome's warnings, and `make compile-node` builds the Node's firmware. A dummy secrets.yaml can't flash anything.

## How a change reaches the Node

- **Home Assistant add-on.** It builds `/config/esphome/geopro-202s.yaml`, which holds `addon/geopro-202s.yaml`: `node.yaml` and the Component, both fetched from `main` on every build ([ADR 0005](../adr/0005-node-is-built-from-main.md)). A change reaches the Node when it is merged to `main` and the add-on installs it, with no edit in the add-on. Only a change to `addon/geopro-202s.yaml` itself is pasted into the add-on by hand, after it merges.
- **Local build.** To test before merging, `make compile-node` (or `esphome compile geopro.yaml`), then `esphome upload geopro.yaml --device <Node address>`. The build lands in `.esphome/build/geopro-202s/`. This flashes the checkout's Component, so the Node then runs code that isn't on `main`; the next add-on install replaces it.
- **Encrypted OTA.** `node.yaml` sets `ota: encryption: {}`, which encrypts uploads with the API key and needs no password ([ADR 0007](../adr/0007-ota-uses-the-api-key.md)). The Node refuses an upload that doesn't encrypt with that key, so upload with ESPHome 2026.9.x and the real `secrets.yaml` next to the config; the upload log says `Encrypted connection established`.

### Switching from the OTA password to encryption (#85)

Delete this section once the owner has removed `ota_password` from both `secrets.yaml` files (step 3).

The firmware that ran before #85 (ESPHome 2026.9.1) has the password but also offers encryption, since it has the API key, and skips the password check on an encrypted upload. So the install that ships #85 already uploads encrypted, and the old password is never sent. Firmware older than 2026.9.0 offers no encryption and the upload stops; `tools/device_info.py` shows the Node's version.

1. Run the before phase, merge, install from the add-on, then run the after phase with `--revision origin/main`.
2. Upload the same commit from a clean checkout: `make compile-node`, then `esphome upload geopro.yaml --device <Node address>`. Check the log for `Encrypted connection established`, then run the after phase again. This proves that a local upload works with encrypted OTA.
3. The owner removes `ota_password` from the add-on's `secrets.yaml` and from the one next to `geopro.yaml`. No config reads it after #85.

## Before flashing

```
python3 tools/flash_check.py before
```

This saves Home Assistant's states to `.scratch/flash-check/states-before.json` and starts a new check. Its notes list any Node entity Home Assistant doesn't have yet, such as one the flash adds. Entity IDs are a contract ([ADR 0004](../adr/0004-entity-ids-stay-stable.md)), recorded in `tests/entity-contract.txt`.

**A flash that adds or renames an entity.** Home Assistant 2026.10 builds a new entity's ID from the Node's area, the Node's friendly name and the entity's name, and turns ° into deg: `L1 20°C below zero` becomes `sensor.garage_geopro_l1_20degc_below_zero`. The Node's other entities are older and read `sensor.geopro_*`. So, as in #63 and #76:

1. In the change, add the entity's `sensor.geopro_*` ID by hand to `tests/ha-entity-ids.txt`, with a comment saying so, and run `make update-contract`.
2. After the flash, rename the new entity in Home Assistant to that ID (the entity's settings, Entity ID). A name change in `node.yaml` leaves the old entity behind as unavailable; delete it.
3. Then run the after phase. It fails until Home Assistant has the recorded ID.

## After flashing

```
.scratch/esphome-2026.9.1/bin/python tools/flash_check.py after
```

Run it with the Python that has ESPHome installed, since it talks to the Node's API; the path above is the venv in this checkout, relative to the repo root. It listens to the Node for 75 s, then saves Home Assistant's states to `.scratch/flash-check/states-after.json`, and fails on any of these:

1. **Running build.** The Node's Component revision (the `component_revision` sensor) isn't the one you flashed. By default it expects what a local build of this checkout stamps, `-dirty` included. After an add-on install, which builds `main`, run `git fetch` and pass `--revision origin/main`. The add-on may build from a cached copy of `main` up to a day old ([ADR 0005](../adr/0005-node-is-built-from-main.md)), so a failure right after a merge can mean the install built the commit before it; pass that commit to check. A `-dirty` revision matches any build of the same commit with uncommitted changes. The report starts with the Node's ESPHome version and compile time.
2. **Entities still exist.** An entity in the contract is missing from Home Assistant under its recorded ID, reads `unavailable` or `unknown`, or has another unit, device class or state class. A missing entity means a rename or a changed kind, which orphans its history. Home Assistant can show a duration or a temperature in another unit than the Node sends (after #11 it showed the Node's 2 h as 120.0 min); the report notes that and doesn't fail on it.
3. **Every entity still publishes.** A sensor sends no state message in the 75 s besides the one sent on subscribing, or the Node has an entity the contract lacks. This is checked live, not in history: Home Assistant's ESPHome integration skips a state that didn't change, so a flat history proves nothing. At the default intervals Values publish every 10 s and Banks every 60 s. A binary sensor may publish only when its bit changes, and the revision only at boot, so the state each sends on subscribing is enough.

Its notes list the Geopro entities gone since the before snapshot, and each unit or class that changed.

## The next morning

```
python3 tools/flash_check.py overnight
```

This summarises each entity's history from the after phase until now: state changes, unavailable or unknown states, and the first and last value. It fails on any unavailable or unknown state. A Bank setting nobody touched can show a single state for the whole night, so a flat history is fine. `--start` and `--end` set another window.

## Capturing a raw bus trace

`geopro-trace.yaml` includes `geopro.yaml` and adds ESPHome's UART `debug:` logging in both directions. It holds no credentials. The Node logs `>>>` lines for Read requests and `<<<` lines for Replies, in the format of `tests/traces/node-2026-10-09.log`. New traces are needed for the write-path work (#24).

1. `esphome compile geopro-trace.yaml`, then `esphome upload geopro-trace.yaml --device <Node address>` (owner's go-ahead first).
2. Record through at least one Bank cycle: `esphome logs geopro-trace.yaml --device <Node address> > .scratch/trace.log`. Run it for 2 minutes or longer.
3. Check that every Bank (0x0C, 0x2C, 0x0B) has both a `>>>` line and a `<<<` line each cycle. The API log stream drops lines without a notice when its send buffer is full. The full 2026-10-09 capture (#10, ESPHome 2025.2.2) lost two of its four Bank 0x0B Replies that way, so compare with the Component's "Received frame" lines, which log at DEBUG here.
4. Flash `geopro.yaml` back (local upload, or an add-on install after the merge). The overlay logs at DEBUG and is for the capture only.
5. To keep a trace, commit a short slice under `tests/traces/` with a header comment like the existing file's (date, issue, which cycles), and replay it from a host test. The lines are hex only; check the slice for anything else before committing.
