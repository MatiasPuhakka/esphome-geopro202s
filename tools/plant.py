"""The entities the Controller model and the run detector read, and how Home Assistant history
rows become their inputs. Geopro entities are looked up by config key in tests/entity-contract.txt
when this module loads, so a renamed entity stops it with a ContractError naming the key."""
from dataclasses import dataclass, replace
from datetime import datetime

from tools import contract
from tools.controller import Settings, State, Temperatures, Thresholds, step, thresholds
from tools.ha import local_time
from tools.runs import runs

# The config key behind each Settings field: the Bank Values.
SETTING_KEYS = {
    "var_yla_kesa": "summer_temp",
    "var_yla_talvi": "winter_temp",
    "varaaja_yla_ero": "top_diff",
    "varaaja_ala_ero": "bottom_diff",
    "var_yla_ero_sv": "top_eh_diff",
    "kompr_esto": "comp_lock",
    "ml_ohjaustapa": "hp_mode",
}

_CONTRACT = contract.load()
COMPRESSOR = _CONTRACT.entity_id("compressor")  # Status bit 0x10
HEATER = _CONTRACT.entity_id("el_heater")  # Status bit 0x08
OUTDOOR = _CONTRACT.entity_id("outside_temp")  # M1
TANK_TOP = _CONTRACT.entity_id("tank_top")  # M9
TANK_MIDDLE = _CONTRACT.entity_id("tank_middle")  # M4, for the tank-middle start the model leaves out
TANK_BOTTOM = _CONTRACT.entity_id("tank_bottom")  # M10
# The entity ID behind each Settings field.
SETTINGS = {field: _CONTRACT.entity_id(key) for field, key in SETTING_KEYS.items()}
# The Shelly 3EM's phase currents, in A, for the whole house.
PHASES = tuple("sensor.shellyem3_34945474817a_channel_%s_current" % p for p in "abc")
# What the model needs, apart from the Status bits.
MODEL_INPUTS = (OUTDOOR, TANK_TOP, TANK_BOTTOM) + tuple(SETTINGS.values())


def numbers(rows):
    """(Finnish time, float) per row; None where the entity was unavailable or unknown."""
    result = []
    for row in rows:
        try:
            value = float(row["state"])
        except ValueError:
            value = None
        result.append((local_time(row["last_changed"]), value))
    return result


def bits(rows):
    """(Finnish time, bool) per row of a binary sensor; None where it was unavailable or unknown."""
    states = {"on": True, "off": False}
    return [(local_time(row["last_changed"]), states.get(row["state"])) for row in rows]


def value_at(series, when):
    """The last known value at or before when in (time, value) rows, skipping None."""
    last = None
    for time, value in series:
        if time > when:
            break
        if value is not None:
            last = value
    return last


@dataclass(frozen=True)
class Step:
    """The Controller model after one reading."""
    time: datetime
    thresholds: Thresholds
    state: State


def replay(series):
    """Steps the Controller model through history, once per change in any of its inputs, from the
    first moment all of them are known. series maps entity IDs to Home Assistant rows. Returns a
    Step per reading. An unavailable input keeps its last known value.

    The model starts calling if the compressor Status bit's first known value is on: a window
    that starts in a run has M9 between the thresholds, where only the Status bit tells whether
    the Controller is calling. It always starts without a Kompr.esto stop, so in a window that
    opens after one, with M10 still above the restart threshold, it calls when the Controller
    doesn't."""
    known = [on for _, on in bits(series.get(COMPRESSOR, [])) if on is not None]
    on = bool(known and known[0])
    state = State(tank_top_call=on, calling=on)
    events = sorted((when, entity_id, value) for entity_id in MODEL_INPUTS
                    for when, value in numbers(series.get(entity_id, [])))
    latest = {}
    result = []
    for when, entity_id, value in events:
        if value is None:
            continue
        latest[entity_id] = value
        if len(latest) < len(MODEL_INPUTS):
            continue
        fields = {name: latest[entity_id] for name, entity_id in SETTINGS.items()}
        fields["ml_ohjaustapa"] = int(fields["ml_ohjaustapa"])
        settings = Settings(**fields)
        reading = Temperatures(outdoor=latest[OUTDOOR], tank_top=latest[TANK_TOP],
                               tank_bottom=latest[TANK_BOTTOM])
        state = step(settings, reading, state)
        result.append(Step(when, thresholds(settings, reading.outdoor), state))
    return result


def compressor_runs(history):
    """The compressor runs in a fetched History, with their starts and breaks. A compressor
    already drawing current when the window opens didn't start in it."""
    found = runs(bits(history.series.get(COMPRESSOR, [])),
                 [numbers(history.series.get(p, [])) for p in PHASES])
    return [replace(run, starts=tuple(s for s in run.starts if s > history.start)) for run in found]
