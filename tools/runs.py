"""Finds compressor runs, starts and breaks in recorded history.

Pure: the compressor Status bit's history and the three phase currents in, runs out. Run, Start
and Break are defined in CONTEXT.md.

The phase currents alone can't tell the compressor from another load of 4 A or more on all
three phases: the sauna's ~10 A, or S1's. current_runs reports those as compressor current, so
runs() counts only the current within a Status-bit run, and no start from current that began
before it. A sauna during a run would still hide that run's breaks.

The thresholds come from the recorded day in tools/tests/fixtures/history_2026-10-09_day.json
(2026-10-09 09:40 to 2026-10-10 09:40, Shelly 3EM phase currents)."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

# The compressor draws 5 to 7 A on every phase in a steady run, so the lowest of the three
# phases rising above this means it started.
DRAWING_ABOVE_A = 4.0
# The lowest phase sits under 1.5 A with the compressor off, so falling below this means it
# stopped. A stop can pass through 3 to 4 A for one Shelly reading.
IDLE_BELOW_A = 3.0
# The Node reads the Status word once per value interval, the Component's default of 10 s that
# geopro.yaml keeps, so a Status-bit edge can lag the current by up to this.
VALUE_INTERVAL = timedelta(seconds=10)


@dataclass(frozen=True)
class Span:
    """A stretch of time."""
    start: datetime
    end: Optional[datetime]  # None if it lasts past the end of the history


@dataclass(frozen=True)
class Run:
    """One stretch of the Status bit being on, with what the phase currents show inside it."""
    start: datetime
    end: Optional[datetime]  # None if it lasts past the end of the history
    starts: tuple = ()  # datetimes the compressor began drawing current
    breaks: tuple = ()  # Spans with no current while the Status bit stayed on


def status_runs(status):
    """Spans of a Status bit being on, from (datetime, bool or None) rows in time order.
    None (the entity unavailable or unknown) keeps the state from before."""
    spans = []
    on_since = None
    for when, on in status:
        if on is None:
            continue
        if on and on_since is None:
            on_since = when
        elif not on and on_since is not None:
            spans.append(Span(on_since, when))
            on_since = None
    if on_since is not None:
        spans.append(Span(on_since, None))
    return spans


def lowest_phase(phases):
    """(datetime, amps) for the lowest of the phases after each reading, from lists of
    (datetime, amps or None) rows, one per phase. Starts once every phase has a reading and
    skips the readings made while any phase is unavailable."""
    events = sorted((when, index, amps) for index, rows in enumerate(phases) for when, amps in rows)
    latest = [None] * len(phases)
    result = []
    for when, index, amps in events:
        latest[index] = amps
        if None not in latest:
            result.append((when, min(latest)))
    return result


def current_runs(phases):
    """Spans of the compressor drawing current, from three lists of (datetime, amps or None) rows,
    one per phase. The compressor loads all three phases, so this follows the lowest one."""
    spans = []
    drawing_since = None
    for when, lowest in lowest_phase(phases):
        if drawing_since is None and lowest > DRAWING_ABOVE_A:
            drawing_since = when
        elif drawing_since is not None and lowest < IDLE_BELOW_A:
            spans.append(Span(drawing_since, when))
            drawing_since = None
    if drawing_since is not None:
        spans.append(Span(drawing_since, None))
    return spans


def overlaps(span, start, end):
    """Whether span overlaps start to end, where an end of None is open."""
    return (end is None or span.start <= end) and (span.end is None or span.end >= start)


def runs(status, phases):
    """Runs from the compressor Status bit's (datetime, bool or None) rows, each with the starts
    and breaks the phase currents show. Current within VALUE_INTERVAL of a run's ends belongs to
    the run; current that began earlier than that gives no start."""
    drawn = current_runs(phases)
    result = []
    for run in status_runs(status):
        inside = [s for s in drawn
                  if overlaps(s, run.start - VALUE_INTERVAL, run.end and run.end + VALUE_INTERVAL)]
        breaks = tuple(Span(a.end, b.start) for a, b in zip(inside, inside[1:]))
        starts = tuple(s.start for s in inside if s.start >= run.start - VALUE_INTERVAL)
        result.append(Run(run.start, run.end, starts, breaks))
    return result
