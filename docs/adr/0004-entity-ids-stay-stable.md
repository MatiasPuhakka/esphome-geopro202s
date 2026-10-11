# Home Assistant entity IDs stay stable

Home Assistant builds an entity's unique ID from its platform and its name, and its history hangs on that ID. `geopro.yaml` therefore keeps the entity names of the YAML protocol copy it replaced (#11), and the Component keeps each Value's entity kind. Renaming a Value or moving it from `sensor` to `binary_sensor` orphans the old entity and its history, and changing a unit or state class raises a statistics repair. The IDs are also the interface to a separate repo whose automations and dashboards use them.

So a change to a name, kind, unit or state class is a Home Assistant migration, made on purpose and reviewed as one, never a side effect of a cleanup. Some migrations are still open (#26). The contract snapshot from #25 lists the entities and what each resolves to. Until it exists, the names are in `geopro.yaml` and each Value's kind, unit and state class in the Register map.
