"""Check a flash of the Node in three phases: before, after and overnight.

before:    save Home Assistant's states, before flashing.
after:     check the running Component revision; that every entity in tests/entity-contract.txt
           exists in Home Assistant with its recorded entity ID, unit and classes and doesn't read
           unavailable or unknown; and that each sensor publishes again within its value or bank
           interval. Needs aioesphomeapi, so run it with the Python that has ESPHome installed.
overnight: summarise each entity's history since the after phase, the next morning.

Each prints its report and exits with status 1 if a check failed. The phases keep their files
in .scratch/flash-check/ at the repo root.

Usage: python3 tools/flash_check.py before
       .scratch/esphome-2026.9.1/bin/python tools/flash_check.py after [--revision REV] [--seconds 75]
       python3 tools/flash_check.py overnight [--start START] [--end END]"""
import argparse
import asyncio
import importlib.util
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import compare_entities, contract, day_run, device_info  # noqa: E402
from tools.contract import RECORD_IDS  # noqa: E402
from tools.day_run import MISSING_STATES  # noqa: E402
from tools.ha import LOCAL, HomeAssistant  # noqa: E402
from tools.node import Node, count_state_messages, read_device_info  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPONENT_DIR = REPO_ROOT / "components" / "geopro_202s"
# Where the phases keep their snapshots: gitignored, at the repo root wherever you run from.
PHASE_DIR = REPO_ROOT / ".scratch" / "flash-check"
# How long the after phase listens to the Node: longer than the 60 s bank interval, the longer
# of the two, so every sensor publishes again after the state sent on subscribing.
DEFAULT_SECONDS = 75

# The config key of the text sensor that publishes the Component revision (#45).
REVISION_KEY = "component_revision"
# What the firmware reports when its build couldn't read git (components/geopro_202s/revision.py).
# Home Assistant's state for an entity with no value reads the same.
UNKNOWN_REVISION = "unknown"
# Units Home Assistant converts between for display, so it can show a Value in another unit
# of the same kind than the Node sends: after #11 it showed the Node's 2 h as 120.0 min.
CONVERTIBLE_UNITS = ({"μs", "ms", "s", "min", "h", "d", "w"}, {"°C", "°F", "K"})


class Result:
    """A phase's report: lines to print, and the problems that fail it."""

    def __init__(self, checked):
        # What a pass covers, such as "37 entities".
        self.checked = checked
        self.lines = []
        self.notes = []
        self.problems = []

    def text(self):
        lines = self.lines + ["note: " + note for note in self.notes]
        lines += ["FAIL " + problem for problem in self.problems]
        if self.problems:
            lines.append("failed: " + _plural(len(self.problems), "problem"))
        else:
            lines.append("passed: " + self.checked)
        return "\n".join(lines) + "\n"


class PhaseFiles:
    """The files the phases leave for each other: the states snapshots, and when each phase ran."""

    def __init__(self, directory):
        self.directory = Path(directory)
        self.before = self.directory / "states-before.json"
        self.after = self.directory / "states-after.json"
        self._times = self.directory / "times.json"

    def write(self, path, states):
        self.directory.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(states, ensure_ascii=False), encoding="utf-8")

    def read(self, path):
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None

    def times(self):
        return self.read(self._times) or {}

    def write_times(self, times):
        self.write(self._times, times)


def _now():
    return datetime.now(LOCAL).replace(microsecond=0)


def before(client, directory=PHASE_DIR, now=None, entity_contract=None):
    """Saves Home Assistant's states for the after phase, and starts a new check."""
    entity_contract = entity_contract or contract.load()
    now = now or _now()
    files = PhaseFiles(directory)
    states = client.states()
    files.write(files.before, states)
    files.write_times({"before": now.isoformat()})
    present = {state["entity_id"] for state in states}
    entities = entity_contract.entities.values()
    result = Result("%d of %d Node entities in Home Assistant"
                    % (sum(e.entity_id in present for e in entities), len(entities)))
    result.lines.append("saved %d states to %s at %s" % (len(states), files.before, now.isoformat(" ")))
    for e in entities:
        if e.entity_id is None:
            result.notes.append('%s ("%s") has no entity ID recorded yet' % (e.key, e.name))
        elif e.entity_id not in present:
            result.notes.append("Home Assistant has no %s (%s) yet" % (e.entity_id, e.key))
    return result


async def _read_node(node, seconds):
    async with node.connected() as client:
        return await read_device_info(client), await count_state_messages(client, seconds)


def after(node, client, expected_revision, seconds=DEFAULT_SECONDS, directory=PHASE_DIR, now=None,
          entity_contract=None):
    """Listens to the Node for `seconds`, then snapshots Home Assistant and checks both."""
    entity_contract = entity_contract or contract.load()
    now = now or _now()
    files = PhaseFiles(directory)
    before_states = files.read(files.before)
    info, counts = asyncio.run(_read_node(node, seconds))
    # After listening, so Home Assistant has also had a bank interval to receive every state.
    states = client.states()
    files.write(files.after, states)
    files.write_times({**files.times(), "after": now.isoformat()})
    result = check_after(entity_contract, states, counts, expected_revision, before_states)
    result.lines.insert(0, device_info.describe(info))
    if before_states is None:
        result.notes.append("no before snapshot in %s, so nothing to compare with" % files.directory)
    return result


def overnight(client, directory=PHASE_DIR, start=None, end=None, entity_contract=None):
    """Summarises each Node entity's history from the after phase (or start) to end (or now), and
    fails on any unavailable or unknown state."""
    entity_contract = entity_contract or contract.load()
    files = PhaseFiles(directory)
    start = start or files.times().get("after")
    if start is None:
        raise SystemExit("No after phase time in %s. Run the after phase first, or give --start." % files.directory)
    ids = entity_contract.entity_ids(entity_contract.entities)
    history = client.history(ids, start, end)
    # Home Assistant returns a row at the start for every entity it has, so an empty one is gone.
    entity_contract.require_ids(history.series, ids, "Home Assistant has no history for")
    text, missing = day_run.report(history)
    result = Result("%d entities, no unavailable or unknown state" % len(ids))
    result.lines = text.splitlines()
    for entity in entity_contract.entities.values():
        if missing[entity.entity_id]:
            result.problems.append("%s: %s" % (_about(entity),
                                               _plural(missing[entity.entity_id], "unavailable or unknown state")))
    return result


def _convertible(unit, other):
    return any(unit in kind and other in kind for kind in CONVERTIBLE_UNITS)


ROW = "%-44s %-12s %-5s %8s"


def check_after(entity_contract, after_states, counts, expected_revision, before_states=None):
    """Checks the after snapshot and the Node's state message counts against the contract: the
    revision, and each entity's ID, state, unit, classes and messages. Notes what changed since
    the before snapshot, if there is one."""
    entities = list(entity_contract.entities.values())
    result = Result("%d entities" % len(entities))
    states = {state["entity_id"]: state for state in after_states}
    revision_entity = entity_contract.entities.get(REVISION_KEY)
    revision = states.get(revision_entity.entity_id) if revision_entity else None
    if revision_entity is None:
        result.problems.append("geopro.yaml sets no %s, so the flash check can't tell which build the Node runs"
                               % REVISION_KEY)
    # An unavailable revision fails as an unavailable entity, below.
    elif revision is not None and revision["state"] != "unavailable":
        running = revision["state"]
        result.lines.append("Component revision %s (expected %s)" % (running, expected_revision))
        result.problems += _revision_problems(running, expected_revision)
        if expected_revision.endswith("-dirty") and not result.problems:
            result.notes.append("a -dirty revision can't tell which uncommitted changes a build had, so any build"
                                " of %s with changes matches" % expected_revision[:-len("-dirty")])
    result.lines.append(ROW % ("entity", "state", "unit", "messages"))
    for entity in entities:
        if entity.entity_id is None:
            result.problems.append('%s ("%s"): the contract records no entity ID; %s.'
                                   % (entity.key, entity.name, RECORD_IDS))
            continue
        state = states.get(entity.entity_id)
        if state is not None:
            result.lines.append((ROW % (entity.entity_id, state["state"][:12],
                                        state["attributes"].get("unit_of_measurement", ""),
                                        counts.get(entity.name, "-"))))
        problems, notes = _home_assistant_problems(entity, state)
        result.notes += notes
        if entity.name not in counts:
            problems.append('the Node has no entity named "%s"' % entity.name)
        elif counts[entity.name] == 0:
            problems.append("no state message")
        elif counts[entity.name] == 1 and entity.platform == "sensor":
            problems.append("only the state sent on subscribing; a sensor publishes again every value or bank"
                            " interval")
        result.problems += ["%s: %s" % (_about(entity), problem) for problem in problems]
    names = {entity.name for entity in entities}
    extra = [name for name in counts if name not in names]
    if extra:
        result.problems.append("the Node has entities %s lacks: %s. Was one renamed, or does the Node run a build"
                               " of another geopro.yaml?"
                               % (entity_contract.path.name, ", ".join('"%s"' % name for name in extra)))
    if before_states is not None:
        result.notes += _changes_since(before_states, states, entity_contract)
    return result


def _changes_since(before_states, after, entity_contract):
    """Notes on the Geopro entities that went away, and the contract's whose unit or classes changed."""
    before = {state["entity_id"]: state for state in before_states}
    notes = []
    gone = sorted(entity_id for entity_id in compare_entities.geopro(before_states) if entity_id not in after)
    if gone:
        notes.append("gone since the before snapshot: " + ", ".join(gone))
    for entity in entity_contract.entities.values():
        if entity.entity_id not in before or entity.entity_id not in after:
            continue
        old, new = before[entity.entity_id]["attributes"], after[entity.entity_id]["attributes"]
        changes = ["%s %s -> %s" % (label, old.get(name) or "none", new.get(name) or "none")
                   for name, label in (("unit_of_measurement", "unit"), ("device_class", "device_class"),
                                       ("state_class", "state_class"))
                   if old.get(name) != new.get(name)]
        if changes:
            notes.append("%s (%s) changed since the before snapshot: %s"
                         % (entity.entity_id, entity.key, ", ".join(changes)))
    return notes


def _revision_problems(running, expected):
    if running == UNKNOWN_REVISION:
        return ["Home Assistant reads the Component revision as unknown: the build couldn't read git, or the"
                " Node hasn't published it. Either way the Node may not run %s" % expected]
    commit, _, dirty = running.partition("-")
    expected_commit, _, expected_dirty = expected.partition("-")
    # git abbreviates a commit to 7 or more characters, so one may be longer than the other.
    same = len(commit) >= 7 and len(expected_commit) >= 7 and (
        commit.startswith(expected_commit) or expected_commit.startswith(commit))
    if not same or dirty != expected_dirty:
        return ["the Node runs Component revision %s, not %s" % (running, expected)]
    return []


def _about(entity):
    return '%s (%s, "%s")' % (entity.entity_id, entity.key, entity.name)


def _plural(count, noun):
    return "%d %s%s" % (count, noun, "" if count == 1 else "s")


def _home_assistant_problems(entity, state):
    """The problems with an entity's state in Home Assistant, and notes on a converted unit."""
    if state is None:
        return ["Home Assistant has no such entity. If it was renamed, %s." % RECORD_IDS], []
    problems, notes = [], []
    # The revision check reports an unknown revision.
    if state["state"] in MISSING_STATES and (entity.key, state["state"]) != (REVISION_KEY, UNKNOWN_REVISION):
        problems.append("reads " + state["state"])
    attributes = state["attributes"]
    unit = attributes.get("unit_of_measurement")
    if unit != entity.unit:
        if _convertible(entity.unit, unit):
            notes.append("%s (%s) shows %s; the contract has %s, which Home Assistant converts"
                         % (entity.entity_id, entity.key, unit, entity.unit))
        else:
            problems.append("unit %s, the contract has %s" % (unit or "none", entity.unit or "none"))
    for name in ("device_class", "state_class"):
        if attributes.get(name) != getattr(entity, name):
            problems.append("%s %s, the contract has %s"
                            % (name, attributes.get(name) or "none", getattr(entity, name) or "none"))
    return problems, notes


def _component_revision(directory):
    """components/geopro_202s/revision.py's component_revision(), which codegen stamps into a build."""
    spec = importlib.util.spec_from_file_location("geopro_revision", COMPONENT_DIR / "revision.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.component_revision(directory)


def expected_revision(ref=None):
    """The Component revision the Node should run: the commit `ref` names, or with no ref, what a
    local build of this checkout stamps, "-dirty" included."""
    if ref is None:
        revision = _component_revision(COMPONENT_DIR)
        if revision == UNKNOWN_REVISION:
            raise SystemExit("git can't tell the revision of %s. Give the one the Node should run with --revision."
                             % COMPONENT_DIR)
        return revision
    try:
        run = subprocess.run(["git", "rev-parse", "--verify", "--quiet", "--short=12", ref + "^{commit}"],
                             cwd=REPO_ROOT, check=True, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        raise SystemExit("git has no commit %s in %s. For origin/main, run git fetch first."
                         % (ref, REPO_ROOT)) from None
    return run.stdout.strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dir", type=Path, default=PHASE_DIR,
                        help="where the phases keep their files (default: .scratch/flash-check)")
    phases = parser.add_subparsers(dest="phase", required=True)
    phases.add_parser("before", parents=[common], help="save Home Assistant's states, before flashing")
    after_phase = phases.add_parser("after", parents=[common], help="check the Node and Home Assistant, after flashing")
    after_phase.add_argument("--revision", help="the commit or ref the Node should run, such as origin/main for an"
                                                " add-on build (default: this checkout's, as a local build stamps it)")
    after_phase.add_argument("--seconds", type=float, default=DEFAULT_SECONDS,
                             help="how long to count the Node's state messages (default: %(default)s)")
    overnight_phase = phases.add_parser("overnight", parents=[common],
                                        help="summarise each entity's history since the after phase")
    overnight_phase.add_argument("--start", help="ISO 8601 time (default: when the after phase ran)")
    overnight_phase.add_argument("--end", help="ISO 8601 time (default: now)")
    args = parser.parse_args(argv)
    if args.phase == "before":
        result = before(HomeAssistant(), args.dir)
    elif args.phase == "after":
        # Everything that can fail on setup fails before the wait.
        result = after(Node(), HomeAssistant(), expected_revision(args.revision), args.seconds, args.dir)
    else:
        result = overnight(HomeAssistant(), args.dir, args.start, args.end)
    sys.stdout.write(result.text())
    if result.problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
