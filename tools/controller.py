"""A model of how the Controller decides to run the compressor, from docs/controller.md.

Pure: settings and temperatures in, the thresholds, the L1 setpoint and whether the Controller
should be calling for the compressor out. Each page cited is a link into the Käsikirja's
transcription, such as manuals/kasikirja.md#s21 for p. 21."""
from dataclasses import dataclass
from datetime import timedelta

# VaraajaYlä equals Var.ylä kesä at this outdoor temperature and above (manuals/kasikirja.md#s21).
SUMMER_OUTDOOR = 20.0
# VaraajaYlä equals Var.ylä talvi at this outdoor temperature and below (manuals/kasikirja.md#s21).
WINTER_OUTDOOR = -20.0
# The ML Ohjaustapa code for Sähkövastus, which turns compressor control into heater control
# (manuals/kasikirja.md#s23). The codes follow the menu order; the owner confirmed them on
# 2026-10-11 (docs/controller.md).
SAHKOVASTUS = 2


@dataclass(frozen=True)
class Settings:
    """The ML circuit's settings the compressor rules use, in °C, with their labels on
    manuals/kasikirja.md#s21."""
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
    start: float  # M9 below this starts the compressor (manuals/kasikirja.md#s23)
    stop: float  # M9 above this stops it (manuals/kasikirja.md#s23)
    heater: float  # M9 below this switches S1 on (manuals/kasikirja.md#s21, manuals/kasikirja.md#s23)
    # After a Kompr.esto stop, M10 must fall to this before the compressor restarts
    # (manuals/kasikirja.md#s23).
    restart: float


def varaaja_yla(settings, outdoor):
    """VaraajaYlä at an outdoor temperature: a straight line from Var.ylä kesä at +20 °C to
    Var.ylä talvi at −20 °C, flat beyond them (manuals/kasikirja.md#s21)."""
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
class L1Settings:
    """Circuit L1's settings the L1 setpoint uses, with their labels on manuals/kasikirja.md#s6,
    manuals/kasikirja.md#s8 and manuals/kasikirja.md#s26."""
    curve_minus20: float  # L1 Käyrä −20, the supply temperature at −20 °C outside
    curve_zero: float  # L1 Käyrä 0
    curve_plus20: float  # L1 Käyrä +20
    min_limit: float  # Minimiraja
    max_limit: float  # Maksimiraja
    night_effect: float  # Yöalennus v., in °C
    autumn_dry: float  # Syyskuivaus, in °C
    out_temp_delay: float  # Ulkol.hidas, in hours


def l1_curve(settings, outdoor):
    """The supply temperature on the L1 curve at an outdoor temperature: straight lines between
    the three points (manuals/kasikirja.md#s6). Flat beyond −20 °C and +20 °C, an assumption
    docs/controller.md lists as unverified."""
    outdoor = min(max(outdoor, WINTER_OUTDOOR), SUMMER_OUTDOOR)
    if outdoor < 0:
        return settings.curve_zero + (settings.curve_minus20 - settings.curve_zero) * outdoor / WINTER_OUTDOOR
    return settings.curve_zero + (settings.curve_plus20 - settings.curve_zero) * outdoor / SUMMER_OUTDOOR


def outdoor_average(readings, when, hours):
    """The time-weighted mean of M1 over the hours before when, as Ulkol.hidas sets it
    (manuals/kasikirja.md#s26). readings are (time, °C) in time order, each holding until the
    next. With hours 0 it is the last reading at or before when. None if there is no reading at
    or before when; a window that starts before the first reading averages from that reading."""
    known = [(time, value) for time, value in readings if time <= when]
    if not known:
        return None
    if hours <= 0:
        return known[-1][1]
    start = when - timedelta(hours=hours)
    before = [(start, value) for time, value in known if time <= start][-1:]
    points = before + [(time, value) for time, value in known if time > start]
    total = (when - points[0][0]).total_seconds()
    if total <= 0:
        return points[-1][1]
    ends = [time for time, _ in points[1:]] + [when]
    weighted = sum((end - time).total_seconds() * value for (time, value), end in zip(points, ends))
    return weighted / total


def l1_setpoint(settings, outdoor, night=False, autumn_dry=False):
    """The L1 setpoint: the supply temperature the Controller aims for on circuit L1, added up
    the way the Menovesi-info screen shows it (manuals/kasikirja.md#s12). outdoor is the averaged
    M1 (outdoor_average). night is whether the clock or a GSM command has the night setback on,
    autumn_dry whether Syyskuivaus is running (manuals/kasikirja.md#s9). The limits apply last.

    Leaves out room, wind and sun compensation, which need sensors this plant doesn't have;
    Esikorotus, which follows a night setback and whose amount the Component doesn't read; and
    Alasajo."""
    setpoint = l1_curve(settings, outdoor)
    if autumn_dry:
        setpoint += settings.autumn_dry
    if night:
        setpoint -= settings.night_effect
    return min(max(setpoint, settings.min_limit), settings.max_limit)


# The daily outdoor mean Syyskuivaus watches, in °C, and its count of days: the warm run before
# it and the cold days it lasts (manuals/kasikirja.md#s9).
AUTUMN_DRY_MEAN = 7.0
AUTUMN_DRY_DAYS = 20


def autumn_dry_active(daily_means):
    """Whether Syyskuivaus runs today by the rule on manuals/kasikirja.md#s9, from the outdoor
    daily means of the days before today, oldest first. It switches on when the mean falls below
    7 °C after at least 20 days in a row above it, and lasts for 20 days with a mean below 7 °C;
    warmer days in between don't count. docs/controller.md records the Controller not following
    this in October 2026."""
    warm_run = 0
    cold_days_left = 0
    for mean in daily_means:
        if mean > AUTUMN_DRY_MEAN:
            warm_run += 1
            continue
        if warm_run >= AUTUMN_DRY_DAYS:
            cold_days_left = AUTUMN_DRY_DAYS
        warm_run = 0
        if cold_days_left:
            cold_days_left -= 1
    return cold_days_left > 0


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
    Sähkövastus (manuals/kasikirja.md#s23). Leaves out the tank-middle start and the tank-bottom
    stop, which need the L1 setpoint the Component doesn't read, and the running-feedback
    alarm (manuals/kasikirja.md#s20). How the tank-top and tank-bottom calls combine is an open
    question in docs/controller.md; here the Kompr.esto stop overrides the tank-top call, as
    manuals/kasikirja.md#s23 says."""
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
