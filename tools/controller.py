"""A model of how the Controller decides to run the compressor, from docs/controller.md.

Pure: settings and temperatures in, the thresholds and whether the Controller should be calling
for the compressor out. Page numbers are the Käsikirja's (manuals/Geopro 202S Käsikirja.pdf)."""
from dataclasses import dataclass

# VaraajaYlä equals Var.ylä kesä at this outdoor temperature and above (p. 21).
SUMMER_OUTDOOR = 20.0
# VaraajaYlä equals Var.ylä talvi at this outdoor temperature and below (p. 21).
WINTER_OUTDOOR = -20.0
# The ML Ohjaustapa code for Sähkövastus, which turns compressor control into heater control
# (p. 23). The codes follow the menu order; the owner confirmed them on 2026-10-11 (docs/controller.md).
SAHKOVASTUS = 2


@dataclass(frozen=True)
class Settings:
    """The ML circuit's settings the compressor rules use, in °C, with their p. 21 labels."""
    var_yla_kesa: float  # Var.ylä kesä
    var_yla_talvi: float  # Var.ylä talvi
    varaaja_yla_ero: float  # VaraajaYläEro
    varaaja_ala_ero: float  # VaraajaAlaEro
    var_yla_ero_sv: float  # VarYläEroSv
    kompr_esto: float  # Kompr.esto
    ml_ohjaustapa: int  # ML Ohjaustapa code


@dataclass(frozen=True)
class Thresholds:
    """The temperatures at which the Controller switches, in °C."""
    varaaja_yla: float  # VaraajaYlä
    start: float  # M9 below this starts the compressor (p. 23)
    stop: float  # M9 above this stops it (p. 23)
    heater: float  # M9 below this switches S1 on (pp. 21, 23)
    restart: float  # after a Kompr.esto stop, M10 must fall to this before the compressor restarts (p. 23)


def varaaja_yla(settings, outdoor):
    """VaraajaYlä at an outdoor temperature: a straight line from Var.ylä kesä at +20 °C to
    Var.ylä talvi at −20 °C, flat beyond them (p. 21)."""
    outdoor = min(max(outdoor, WINTER_OUTDOOR), SUMMER_OUTDOOR)
    share = (SUMMER_OUTDOOR - outdoor) / (SUMMER_OUTDOOR - WINTER_OUTDOOR)
    return settings.var_yla_kesa + (settings.var_yla_talvi - settings.var_yla_kesa) * share


def thresholds(settings, outdoor):
    setpoint = varaaja_yla(settings, outdoor)
    start = setpoint - settings.varaaja_yla_ero
    return Thresholds(varaaja_yla=setpoint, start=start, stop=setpoint,
                      heater=start - settings.var_yla_ero_sv,
                      restart=settings.kompr_esto - settings.varaaja_ala_ero)


@dataclass(frozen=True)
class Temperatures:
    """One reading of the measurements the rules use, in °C."""
    outdoor: float  # M1
    tank_top: float  # M9
    tank_bottom: float  # M10


@dataclass(frozen=True)
class State:
    """What the Controller remembers from one reading to the next."""
    tank_top_call: bool = False  # M9 fell below the start threshold and hasn't risen above the stop one
    kompr_esto_stop: bool = False  # M10 reached Kompr.esto and hasn't fallen to the restart threshold
    calling: bool = False  # the Controller calls for the compressor


def step(settings, temperatures, state):
    """The State after one reading.

    Models the tank-top start and stop, the Kompr.esto stop and restart, and ML Ohjaustapa
    Sähkövastus (p. 23). Leaves out the tank-middle start and the tank-bottom stop, which need
    the L1 setpoint the Component doesn't read, and the running-feedback alarm (p. 20). How the
    tank-top and tank-bottom calls combine is an open question in docs/controller.md; here the
    Kompr.esto stop overrides the tank-top call, as p. 23 says."""
    t = thresholds(settings, temperatures.outdoor)
    if temperatures.tank_top < t.start:
        top_call = True
    elif temperatures.tank_top > t.stop:
        top_call = False
    else:
        top_call = state.tank_top_call
    if temperatures.tank_bottom >= settings.kompr_esto:
        esto = True
    elif temperatures.tank_bottom <= t.restart:
        esto = False
    else:
        esto = state.kompr_esto_stop
    calling = top_call and not esto and settings.ml_ohjaustapa != SAHKOVASTUS
    return State(tank_top_call=top_call, kompr_esto_stop=esto, calling=calling)
