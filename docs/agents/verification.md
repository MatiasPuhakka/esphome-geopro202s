# Verifying a change on the Node

Host tests and CI cover building and decoding. The Node on the real bus covers the rest. Verify any change that alters what the Node runs: the Component, `geopro.yaml` or the ESPHome version. Ask the owner before flashing.

The steps below are manual. A tools module (#42), a revision stamp in the firmware (#45) and a flash check (#46) are planned to replace them.

## Setup

- **ESPHome version.** `geopro.yaml` needs ESPHome 2026.9.x ([ADR 0002](../adr/0002-supported-esphome-versions.md)). The `esphome` on PATH may be another version. The make targets that run ESPHome stop and say so; point them at a 2026.9.x install with `ESPHOME=/path/to/esphome`, for example `make check-node-config ESPHOME=/path/to/esphome`. When calling ESPHome directly, run `esphome version` first.
- **Secrets.** `secrets.yaml` sits next to `geopro.yaml`, is gitignored and holds `api_encryption_key` and `ota_password`. Never print it, paste it into a doc or commit it; `make check-secrets` fails on an inline key or password. The Home Assistant token is `ACCESS_TOKEN` in the gitignored `.env`; treat it the same way. Source it into the shell (`set -a; . ./.env; set +a`) so the value stays out of what you type and out of output.
- **Without a secrets.yaml.** Write a dummy one, as CI does, only when none exists:
  `printf 'api_encryption_key: "%s"\nota_password: ci\n' "$(head -c 32 /dev/urandom | base64)" > secrets.yaml`
  Then `make check-node-config check-trace-config` validates both configs and prints ESPHome's warnings, and `make compile-node` builds the Node's firmware. A dummy secrets.yaml can't flash anything.

## How a change reaches the Node

- **Home Assistant add-on.** It builds `/config/esphome/geopro-202s.yaml`, a copy of `geopro.yaml` whose Component source is `github://MatiasPuhakka/esphome-geopro202s@main`. A change reaches the Node only after it is merged to `main` and the add-on installs it, and the add-on may serve a cached copy of `main` for up to a day ([ADR 0005](../adr/0005-node-is-built-from-main.md)). A change to `geopro.yaml` is also made in the copy by hand.
- **Local build.** To test before merging, `make compile-node` (or `esphome compile geopro.yaml`), then `esphome upload geopro.yaml --device <Node address>`. The build lands in `.esphome/build/geopro-202s/`. This flashes the checkout's Component, so the Node then runs code that isn't on `main`; the next add-on install replaces it.

## Before flashing

Snapshot Home Assistant's states, so the after check has something to compare with:

```
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$HA_URL/api/states" > .scratch/states-before.json
```

`$HA_URL` is Home Assistant's address, for example `http://<host>:8123`. Keep the file in `.scratch/`. It lists every `sensor.geopro_*` and `binary_sensor.geopro_*` entity with its state; entity IDs are a contract ([ADR 0004](../adr/0004-entity-ids-stay-stable.md)).

## After flashing

1. **Running build.** Confirm the Node runs what you built. Home Assistant's device page for the Node shows the firmware's compile time; compare it with the time of your build.
2. **Entities still exist.** Fetch `/api/states` again. Every `sensor.geopro_*` and `binary_sensor.geopro_*` entity from the snapshot is present and none reads `unavailable` or `unknown`. A missing entity means a rename or a changed kind, which orphans its history.
3. **Every entity still publishes.** Check live, not in history: Home Assistant's ESPHome integration skips a state that didn't change, so a flat history proves nothing. Connect to the Node's API with `aioesphomeapi` (installed with ESPHome), using the key from `secrets.yaml`, and subscribe to states for about 75 s. The subscription starts with a dump of every current state, so count the updates after it. At the default intervals Values publish every 10 s and Banks every 60 s, and each sensor should publish again within its interval. A binary sensor may publish only when its bit changes; its entry in the dump is enough.

## The next morning

Review a day of Home Assistant history for each entity since the flash (`/api/history/period/<flash time>?filter_entity_id=<ids>&minimal_response`). Look for `unavailable` and `unknown`; there should be none. A Bank setting nobody touched can show a single state for the whole day, so a flat history is fine.

## Capturing a raw bus trace

`geopro-trace.yaml` includes `geopro.yaml` and adds ESPHome's UART `debug:` logging in both directions. It holds no credentials. The Node logs `>>>` lines for Read requests and `<<<` lines for Replies, in the format of `tests/traces/node-2026-10-09.log`. New traces are needed for the write-path work (#24).

1. `esphome compile geopro-trace.yaml`, then `esphome upload geopro-trace.yaml --device <Node address>` (owner's go-ahead first).
2. Record through at least one Bank cycle: `esphome logs geopro-trace.yaml --device <Node address> > .scratch/trace.log`. Run it for 2 minutes or longer.
3. Check that every Bank (0x0C, 0x2C, 0x0B) has both a `>>>` line and a `<<<` line each cycle. The API log stream drops lines without a notice when its send buffer is full. The full 2026-10-09 capture (#10, ESPHome 2025.2.2) lost two of its four Bank 0x0B Replies that way, so compare with the Component's "Received frame" lines, which log at DEBUG here.
4. Flash `geopro.yaml` back (local upload, or an add-on install after the merge). The overlay logs at DEBUG and is for the capture only.
5. To keep a trace, commit a short slice under `tests/traces/` with a header comment like the existing file's (date, issue, which cycles), and replay it from a host test. The lines are hex only; check the slice for anything else before committing.
