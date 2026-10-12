# Support the ESPHome 2026.9 series only

The Component supports ESPHome 2026.9.x, the series the Home Assistant add-on builds the Node with. CI builds against the add-on's exact version (2026.9.1) and nothing else. We dropped 2025.2.2, which CI had built as "the version the component was developed against" (#35). It lacks `invalidate_state()`, which the stale-entity fix needs, and it doesn't know the Ethernet `clk:` block that `node.yaml` and the example config use.

An older series is dropped when the add-on moves to a newer one. The change that bumps the CI version also updates `SUPPORTED_ESPHOME` in the Makefile and the README's minimum version. Newer ESPHome releases that the add-on doesn't ship yet aren't tested, so they aren't promised.

Revisit this if the Component gains users who run their own ESPHome and can't follow the add-on's version.
