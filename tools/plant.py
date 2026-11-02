"""The entities the Controller model and the run detector read, and how Home Assistant history
rows become their inputs. Geopro entities are looked up by config key in tests/entity-contract.txt
when this module loads, so a renamed entity stops it with a ContractError naming the key."""
from dataclasses import dataclass, replace
from datetime import datetime, timedelta

from tools import contract
from tools.controller import (L1Settings, Settings, State, Temperatures, Thresholds, l1_setpoint,
                              outdoor_average, step, thresholds)
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
TANK_MIDDLE = _CONTRACT.entity_id("tank_middle")  # M4
TANK_BOTTOM = _CONTRACT.entity_id("tank_bottom")  # M10
# The entity ID behind each Settings field.
SETTINGS = {field: _CONTRACT.entity_id(key) for field, key in SETTING_KEYS.items()}
# The Shelly 3EM's phase currents, in A, for the whole house.
PHASES = tuple("sensor.shellyem3_34945474817a_channel_%s_current" % p for p in "abc")
# What the model needs, apart from the Status bits.
MODEL_INPUTS = (OUTDOOR, TANK_TOP, TANK_BOTTOM) + tuple(SETTINGS.values())

# The config key behind each L1Settings field: the Bank Values.
L1_SETTING_KEYS = {
    "curve_minus20": "l1_minus20",
    "curve_zero": "l1_zero",
    "curve_plus20": "l1_plus20",
    "min_limit": "l1_min_limit",
    "max_limit": "l1_max_limit",
    "night_effect": "l1_night_effect",
    "autumn_dry": "l1_autumn_dry",
    "out_temp_delay": "l1_out_temp_delay",
}
L1_SETTINGS = {field: _CONTRACT.entity_id(key) for field, key in L1_SETTING_KEYS.items()}
VARAAJA_ALA_MIN = _CONTRACT.entity_id("tank_min")
# What the tank-middle start and the tank-bottom stop need as well. Without all of them, the
# model leaves those two rules out.
MIDDLE_INPUTS = (TANK_MIDDLE, VARAAJA_ALA_MIN) + tuple(L1_SETTINGS.values())
# Home Assistant may show a duration in another unit than the Component publishes; the
# entity's attributes say which. Ulkol.hidas is in hours in the contract.
TO_HOURS = {"h": 1.0, "min": 1 / 60, "s": 1 / 3600, "d": 24.0}


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


def _hours_factor(rows):
    """What turns an Ulkol.hidas row into hours, from the unit in its first row's attributes,
    which only a history fetched with attributes carries. Hours if it doesn't say."""
    unit = rows[0].get("attributes", {}).get("unit_of_measurement", "h") if rows else "h"
    return TO_HOURS[unit]


def replay(series):
    """Steps the Controller model through history, once per change in any of its inputs, from the
    first moment all of them are known. series maps entity IDs to Home Assistant rows. Returns a
    Step per reading. An unavailable input keeps its last known value.

    Once M4, VaraajaAlaMin and every L1 setting are known as well, the model also runs the
    tank-middle start and the tank-bottom stop, with the L1 setpoint from M1 averaged over
    Ulkol.hidas. Without them, those two rules stay out. Syyskuivaus stays off: the Controller
    didn't run it in October 2026 (docs/controller.md).

    The model starts calling if the compressor Status bit's first known value is on: a window
    that starts in a run has M9 between the thresholds, where only the Status bit tells whether
    the Controller is calling. It always starts without a Kompr.esto stop, so in a window that
    opens after one, with M10 still above the restart threshold, it calls when the Controller
    doesn't."""
    known = [on for _, on in bits(series.get(COMPRESSOR, [])) if on is not None]
    on = bool(known and known[0])
    state = State(tank_top_call=on, calling=on)
    middle = all(series.get(entity_id) for entity_id in MIDDLE_INPUTS)
    inputs = MODEL_INPUTS + (MIDDLE_INPUTS if middle else ())
    delay_factor = _hours_factor(series.get(L1_SETTINGS["out_temp_delay"], []))
    events = sorted((when, entity_id, value) for entity_id in inputs
                    for when, value in numbers(series.get(entity_id, [])))
    latest = {}
    outdoor = []  # M1 readings, trimmed to the averaging window
    result = []
    for when, entity_id, value in events:
        if value is None:
            continue
        latest[entity_id] = value
        if entity_id == OUTDOOR:
            outdoor.append((when, value))
        if any(entity_id not in latest for entity_id in MODEL_INPUTS):
            continue
        middle_now = middle and all(entity_id in latest for entity_id in MIDDLE_INPUTS)
        fields = {name: latest[entity_id] for name, entity_id in SETTINGS.items()}
        fields["ml_ohjaustapa"] = int(fields["ml_ohjaustapa"])
        l1 = None
        if middle_now:
            fields["varaaja_ala_min"] = latest[VARAAJA_ALA_MIN]
            l1_fields = {name: latest[entity_id] for name, entity_id in L1_SETTINGS.items()}
            l1_fields["out_temp_delay"] *= delay_factor
            l1_settings = L1Settings(**l1_fields)
            window_start = when - timedelta(hours=l1_settings.out_temp_delay)
            while len(outdoor) > 1 and outdoor[1][0] <= window_start:
                outdoor.pop(0)
            l1 = l1_setpoint(l1_settings, outdoor_average(outdoor, when, l1_settings.out_temp_delay))
        settings = Settings(**fields)
        reading = Temperatures(outdoor=latest[OUTDOOR], tank_top=latest[TANK_TOP],
                               tank_bottom=latest[TANK_BOTTOM],
                               tank_middle=latest[TANK_MIDDLE] if middle_now else None)
        state = step(settings, reading, state, l1, when)
        result.append(Step(when, thresholds(settings, reading.outdoor, l1), state))
    return result


def model_history(client, entity_ids, start, end=None):
    """History for entity_ids and every input replay() reads, from a HomeAssistant client.
    Ulkol.hidas comes in a second request with attributes, so replay() can read the unit Home
    Assistant shows it in."""
    history = client.history([*entity_ids, *MODEL_INPUTS, *MIDDLE_INPUTS], start, end)
    delay = L1_SETTINGS["out_temp_delay"]
    if delay in history.series:
        history.series[delay] = client.history([delay], start, end, attributes=True).series[delay]
    return history


def compressor_runs(history):
    """The compressor runs in a fetched History, with their starts and breaks. A compressor
    already drawing current when the window opens didn't start in it."""
    found = runs(bits(history.series.get(COMPRESSOR, [])),
                 [numbers(history.series.get(p, [])) for p in PHASES])
    return [replace(run, starts=tuple(s for s in run.starts if s > history.start)) for run in found]
