# Home Assistant entity IDs stay stable

Home Assistant builds an entity's unique ID from its platform and its name, and its history hangs on that ID. `node.yaml` therefore keeps the entity names of the YAML protocol copy it replaced (#11), and the Component keeps each Value's entity kind. Renaming a Value or moving it from `sensor` to `binary_sensor` orphans the old entity and its history, and changing a unit or state class raises a statistics repair. The IDs are also the interface to a separate repo whose automations and dashboards use them.

So a change to a name, kind, unit or state class is a Home Assistant migration, made on purpose and reviewed as one, never a side effect of a cleanup. The contract snapshot from #25 (`make check-contract`) lists the entities and what each resolves to.

Three migrations were considered in #26:

- **State class of settings.** The 24 Bank settings (`hp_mode` is one of them) and `status_word` lose `state_class: measurement` (#75). A setting changes only when someone edits it on the Controller, and an enum like `hp_mode` or a bitfield like the Status word has no meaningful mean or minimum, so their statistics say nothing. Cost: 25 statistics repairs; IDs and history stay.
- **hp_mode.** The numeric entity stays as it is. #64 decides how to show the mode's name.
- **L1 -20°C and L1 +20°C.** Both are renamed in firmware to `L1 20°C below zero` and `L1 20°C above zero` (#76). Cost: both entities are new, so both old ones and their history are orphaned, and the Home Assistant repo's references change with them. Renaming only the entity ID in Home Assistant's registry would have kept the statistics, but the registry isn't in this repo, so a fresh install would repeat the `_2` ambiguity.
