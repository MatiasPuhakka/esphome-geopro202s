"""Watch one compressor run through Home Assistant and print its events.

Prints the Controller's call starting and ending (the compressor Status bit), compressor
current breaks during a call (drops of about 6 A on all three Shelly phases, which is
chatter), the heater bit, and a run summary. Every sample also goes to the samples file for
later analysis. Stops after one call of 5 minutes or more, or after 3 hours.

Usage: python3 tools/run_watch.py SAMPLES_FILE"""
import argparse
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

if not __package__:
    # Run as a script: make the tools package importable from any directory.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import contract  # noqa: E402
from tools.ha import LOCAL, HomeAssistant, local_time  # noqa: E402

# The Shelly 3EM on the heat pump's supply, one entity per phase. Not the Node's, so not in the contract.
PHASES = ["sensor.shellyem3_34945474817a_channel_%s_current" % phase for phase in "abc"]
# Config keys in tests/entity-contract.txt.
CALL = "compressor"
HEATER = "el_heater"
TEMPS = {"M7": "tank_top_in", "M9": "tank_top", "M10": "tank_bottom", "brine": "brine"}
COMP_LOCK = "comp_lock"

MAX_SECONDS = 3 * 3600
POLL_SECONDS = 2
# Home Assistant reads may fail this long before the watch says so.
FAILING_SECONDS = 30
# The compressor loads all three phases: above this on every phase it is drawing current...
DRAWING_AMPS = 4
# ...and below this on the lowest phase it has stopped (the history backfill).
STOPPED_AMPS = 3
# A drop on every phase within this range between two samples is the compressor stopping.
BREAK_DROP_AMPS = (-8.5, -4)
# The call bit comes from the Status word, which the Node reads every 10 s, so a normal stop
# shows the current drop a few seconds before the call ends. A drop only counts as a break if
# the Controller still calls this long after it.
BREAK_CONFIRM_SECONDS = 12
# The tank bottom is the condenser inlet; the alarm 11 trips came once it passed about 51 °C.
# Each whole degree from here up is reported.
TANK_BOTTOM_WATCH = 49
# The JV-at-0 runs chattered from minute 7-8, so say how many breaks there were at 10 min.
MILESTONE_SECONDS = 600
CHATTER_NOTE_SECONDS = 120
# A call this long is one full heating phase, and the watch stops after it.
FULL_RUN_MINUTES = 5


class Clock:
    def time(self):
        return time.time()

    def sleep(self, seconds):
        time.sleep(seconds)


def hms(timestamp):
    return datetime.fromtimestamp(timestamp, LOCAL).strftime("%H:%M:%S")


def temps_text(t):
    return ", ".join(f"{k} {v:.1f}" for k, v in t.items())


def new_run(start, since, t):
    """A call: when it started, breaks so far, the temperatures at its start and their extremes."""
    return {"start": start, "since": since, "breaks": 0, "first": dict(t),
            "max_m7": t["M7"], "min_brine": t["brine"], "milestone": False}


class Watch:
    def __init__(self, client, samples, out, clock, entity_contract):
        self.client = client
        self.samples = samples
        self.out = out
        self.clock = clock
        self.call_id = entity_contract.entity_id(CALL)
        self.heater_id = entity_contract.entity_id(HEATER)
        self.temp_ids = {name: entity_contract.entity_id(key) for name, key in TEMPS.items()}
        self.comp_lock_id = entity_contract.entity_id(COMP_LOCK)
        # Fail now on a renamed entity, which would otherwise read as "Home Assistant reads failing".
        entity_contract.require_ids({state["entity_id"] for state in client.states()},
                                    PHASES + [self.call_id, self.heater_id, self.comp_lock_id]
                                    + list(self.temp_ids.values()))

    def emit(self, text):
        self.out.write("%s %s\n" % (hms(self.clock.time()), text))
        self.out.flush()

    def backfill(self, start_iso):
        """Temperatures at the call start, and current breaks between the call start and now."""
        start = local_time(start_iso)
        later = start + timedelta(seconds=1)
        now = datetime.fromtimestamp(self.clock.time(), LOCAL)
        first = {k: float(self.client.history([e], start, later).series[e][0]["state"])
                 for k, e in self.temp_ids.items()}
        changes = sorted((datetime.fromisoformat(r["last_changed"]), entity, float(r["state"]))
                         for entity, rows in self.client.history(PHASES, start, now).series.items()
                         for r in rows if r["state"] not in ("unavailable", "unknown"))
        latest, drawing, breaks = {}, None, 0
        for _, entity, amps in changes:
            latest[entity] = amps
            if len(latest) < 3:
                continue
            low = min(latest.values())
            if drawing is None:
                drawing = low > DRAWING_AMPS
            elif drawing and low < STOPPED_AMPS:
                breaks, drawing = breaks + 1, False
            elif not drawing and low > DRAWING_AMPS:
                drawing = True
        return first, breaks

    def run(self):
        clock = self.clock
        started = clock.time()
        prev_cur = None
        call = heater = None
        run = None  # the current call: start time, breaks, temperature extremes
        failing_since = None
        last_chatter_note = 0

        while clock.time() - started < MAX_SECONDS:
            try:
                cur = [float(self.client.state(p)["state"]) for p in PHASES]
                call_state = self.client.state(self.call_id)
                heater_on = self.client.state(self.heater_id)["state"] == "on"
                t = {k: float(self.client.state(e)["state"]) for k, e in self.temp_ids.items()}
            except Exception as e:  # Home Assistant restart, network blip, an unavailable sensor
                if failing_since is None:
                    failing_since = clock.time()
                elif clock.time() - failing_since > FAILING_SECONDS and failing_since > 0:
                    self.emit(f"Home Assistant reads failing for {FAILING_SECONDS} s: {e}")
                    failing_since = -1  # reported; stay quiet until it recovers
                clock.sleep(POLL_SECONDS)
                continue
            if failing_since == -1:
                self.emit("Home Assistant reads working again")
            failing_since = None

            now = hms(clock.time())
            calling = call_state["state"] == "on"
            self.samples.write(f"{now} {cur[0]:5.2f} {cur[1]:5.2f} {cur[2]:5.2f} call={'on' if calling else 'off'} "
                               f"heater={'on' if heater_on else 'off'} {temps_text(t)}\n")

            if heater is not None and heater_on != heater:
                self.emit(f"heater {'ON' if heater_on else 'off'}, {temps_text(t)}")
            heater = heater_on

            if call is None:
                since = hms(datetime.fromisoformat(call_state["last_changed"]).timestamp())
                drawing = all(c > DRAWING_AMPS for c in cur)
                note = ""
                if calling:
                    start = datetime.fromisoformat(call_state["last_changed"]).timestamp()
                    run = new_run(start, since, t)
                    try:
                        run["first"], run["breaks"] = self.backfill(call_state["last_changed"])
                        note = f"; {run['breaks']} current breaks before this watch started (HA history)"
                    except Exception as e:
                        note = f"; HA history backfill failed ({e}), counting breaks from now"
                try:
                    note += f"; Kompr.esto in HA: {float(self.client.state(self.comp_lock_id)['state']):.0f}"
                except Exception:
                    pass
                self.emit(f"watching: Controller {'calling since ' + since if calling else 'idle since ' + since}, "
                          f"compressor {'drawing current' if drawing else 'not drawing'} "
                          f"({cur[0]:.1f}/{cur[1]:.1f}/{cur[2]:.1f} A), {temps_text(t)}{note}")
                if run:
                    run["m10_mark"] = int(t["M10"])
            elif calling and not call:
                self.emit(f"Controller call started, {temps_text(t)}")
                run = new_run(clock.time(), now, t)
                run["m10_mark"] = int(t["M10"])
            elif call and not calling and run:
                minutes, seconds = divmod(int(clock.time() - run["start"]), 60)
                f = run["first"]
                self.emit(f"run ended: call {run['since']}-{now} ({minutes} min {seconds} s), "
                          f"{run['breaks']} current breaks during the call; "
                          f"M9 {f['M9']:.1f}->{t['M9']:.1f}, M10 {f['M10']:.1f}->{t['M10']:.1f}, "
                          f"M7 max {run['max_m7']:.1f}, brine min {run['min_brine']:.1f}")
                if minutes >= FULL_RUN_MINUTES:
                    return  # one full heating phase seen; a short call keeps watching for the restart
                run = None
            call = calling

            if run:
                run["max_m7"] = max(run["max_m7"], t["M7"])
                run["min_brine"] = min(run["min_brine"], t["brine"])
                if int(t["M10"]) > run.get("m10_mark", int(t["M10"])) and t["M10"] >= TANK_BOTTOM_WATCH:
                    run["m10_mark"] = int(t["M10"])
                    self.emit(f"tank bottom passed {run['m10_mark']} °C, {run['breaks']} current breaks so far, "
                              f"{temps_text(t)}")
                if prev_cur:
                    d = [c - q for c, q in zip(cur, prev_cur)]
                    if calling and all(BREAK_DROP_AMPS[0] <= x <= BREAK_DROP_AMPS[1] for x in d):
                        run.setdefault("pending", []).append(clock.time())
                # A call that ends before a drop is confirmed drops `run`, and the drop with it.
                due = [p for p in run.get("pending", []) if clock.time() - p >= BREAK_CONFIRM_SECONDS]
                if due:
                    run["pending"] = [p for p in run["pending"] if clock.time() - p < BREAK_CONFIRM_SECONDS]
                    run["breaks"] += len(due)
                    if run["breaks"] == len(due) or clock.time() - last_chatter_note > CHATTER_NOTE_SECONDS:
                        self.emit(f"compressor current dropped while the Controller kept calling "
                                  f"(break {run['breaks']}), {temps_text(t)}")
                        last_chatter_note = clock.time()
                elapsed = clock.time() - run["start"]
                if not run["milestone"] and elapsed >= MILESTONE_SECONDS:
                    run["milestone"] = True
                    self.emit(f"10 min into the call, {run['breaks']} current breaks so far "
                              f"(the JV-at-0 runs chattered from minute 7-8), {temps_text(t)}")
            prev_cur = cur
            clock.sleep(POLL_SECONDS)
        self.emit("stopped after 3 h without a full run")


def watch(client, samples, out, clock=None, entity_contract=None):
    Watch(client, samples, out, clock or Clock(), entity_contract or contract.load()).run()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("samples", help="file to append every sample to")
    args = parser.parse_args(argv)
    with open(args.samples, "a", buffering=1, encoding="utf-8") as samples:
        watch(HomeAssistant(), samples, sys.stdout)


if __name__ == "__main__":
    main()
