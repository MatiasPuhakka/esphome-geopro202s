import io
import json
import subprocess
import sys
import tempfile
import unittest
import urllib.parse
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest import mock

from tools import contract, flash_check
from tools.tests.fakes import FIXTURES, FakeClock, ReplayHomeAssistant, TempFile, client_for, node_for

# The commit the tests pretend the Node was built from. The #11 snapshots predate the
# revision sensor (#45), so the tests add its state and its one message.
REVISION = "02b5199"
# The contract the #11 snapshots match. The live one has migrated since (#75).
FLASH_CONTRACT = FIXTURES / "entity_contract_flash.txt"


def snapshot(name):
    return json.loads((FIXTURES / name).read_text())


def after_states(revision=REVISION):
    """The #11 after snapshot, with the revision sensor the Node has had since #45."""
    return snapshot("states_after_flash.json") + [{
        "entity_id": "sensor.geopro_komponentin_versio", "state": revision,
        "attributes": {"icon": "mdi:source-commit", "friendly_name": "Geopro Komponentin versio"},
        "last_changed": "2026-10-09T16:17:20+00:00", "last_reported": "2026-10-09T16:17:20+00:00",
        "last_updated": "2026-10-09T16:17:20+00:00"}]


def counts(test):
    """State messages per entity name in the recorded Node session, and the revision's one."""
    node, _ = node_for(test)
    return {**node.count_states(0), "Komponentin versio": 1}


def flash_contract():
    return contract.load(FLASH_CONTRACT)


def by_id(states, entity_id):
    return next(s for s in states if s["entity_id"] == entity_id)


class CheckAfterTest(unittest.TestCase):
    def check(self, after=None, node_counts=None, expected=REVISION, before=None):
        return flash_check.check_after(flash_contract(), after_states() if after is None else after,
                                       counts(self) if node_counts is None else node_counts, expected,
                                       before)

    def test_passes_on_the_snapshot_and_node_session_from_after_the_11_flash(self):
        result = self.check(before=snapshot("states_before_flash.json"))

        self.assertEqual(result.problems, [])

    def test_lists_each_entity_with_its_state_unit_and_messages(self):
        text = self.check().text()

        self.assertIn("entity                                       state        unit  messages\n"
                      "sensor.geopro_komponentin_versio             02b5199                   1\n"
                      "sensor.geopro_ulkol_mp_tila                  9.3999996185 °C           9\n", text)
        self.assertIn("binary_sensor.geopro_kompressori             off                       1\n", text)
        self.assertTrue(text.endswith("\npassed: 37 entities\n"), text)

    def test_notes_what_changed_since_the_before_snapshot(self):
        # The #11 flash left out four entities and changed three units, as compare_entities shows.
        text = self.check(before=snapshot("states_before_flash.json")).text()

        self.assertIn("note: gone since the before snapshot: sensor.garage_geopro_l1_huone,"
                      " sensor.garage_geopro_vapaa_mittaus, sensor.geopro_jv_venttiili, sensor.geopro_l1_venttiili\n",
                      text)
        self.assertIn("note: sensor.geopro_l1_esikorotus (l1_pre_increase) changed since the before snapshot:"
                      " unit °C -> h, device_class temperature -> duration\n", text)
        self.assertIn("note: sensor.geopro_ml_jv_esto (dhw_lock) changed since the before snapshot: unit s -> min\n",
                      text)

    def test_counts_the_problems_at_the_end(self):
        text = self.check(after_states("7f261e5"), {**counts(self), "Maaliuos": 1}).text()

        self.assertTrue(text.endswith("\nfailed: 2 problems\n"), text)

    def test_accepts_a_duration_that_home_assistant_shows_in_another_unit(self):
        # After #11, Home Assistant showed the Node's 2 h as 120.0 min.
        result = self.check()

        self.assertEqual(result.problems, [])
        self.assertIn("sensor.geopro_l1_ulkol_mp_tilan_hidastus (l1_out_temp_delay) shows min; the contract has h,"
                      " which Home Assistant converts", result.text())

    def test_a_missing_entity_fails(self):
        after = [s for s in after_states() if s["entity_id"] != "sensor.geopro_maaliuos"]

        result = self.check(after)

        self.assertEqual(result.problems, [
            'sensor.geopro_maaliuos (brine, "Maaliuos"): Home Assistant has no such entity.'
            ' If it was renamed, ' + contract.RECORD_IDS + '.'])

    def test_a_renamed_entity_fails(self):
        # Home Assistant keeps the old entity as unavailable and adds one under the new name.
        after = after_states()
        old = by_id(after, "sensor.geopro_maaliuos")
        old["state"] = "unavailable"
        old["attributes"]["restored"] = True
        after.append({**old, "entity_id": "sensor.geopro_maaliuos_lampotila", "state": "14.7"})
        node_counts = counts(self)
        node_counts["Maaliuos lämpötila"] = node_counts.pop("Maaliuos")

        result = self.check(after, node_counts)

        self.assertEqual(result.problems, [
            'sensor.geopro_maaliuos (brine, "Maaliuos"): reads unavailable',
            'sensor.geopro_maaliuos (brine, "Maaliuos"): the Node has no entity named "Maaliuos"',
            'the Node has entities entity_contract_flash.txt lacks: "Maaliuos lämpötila".'
            ' Was one renamed, or does the Node run a build of another node.yaml?'])

    def test_an_entity_with_no_recorded_id_fails(self):
        # Such as a new entity, before its ID is recorded.
        text = FLASH_CONTRACT.read_text(encoding="utf-8").replace(
            '"Maaliuos" sensor.geopro_maaliuos', '"Maaliuos" ' + contract.NO_ENTITY_ID)
        path = TempFile(self, text).path

        result = flash_check.check_after(contract.load(path), after_states(), counts(self), REVISION)

        self.assertEqual(result.problems, [
            'brine ("Maaliuos"): the contract records no entity ID; ' + contract.RECORD_IDS + '.'])

    def test_a_changed_unit_or_class_fails(self):
        # Before #23, L1 Esikorotus was a temperature in °C. The contract has it in hours.
        after = after_states()
        after.remove(by_id(after, "sensor.geopro_l1_esikorotus"))
        after.append(by_id(snapshot("states_before_flash.json"), "sensor.geopro_l1_esikorotus"))
        by_id(after, "sensor.geopro_kompressori_tunnit")["attributes"]["state_class"] = "measurement"
        del by_id(after, "sensor.geopro_maaliuos")["attributes"]["unit_of_measurement"]

        result = self.check(after)

        self.assertEqual(result.problems, [
            'sensor.geopro_maaliuos (brine, "Maaliuos"): unit none, the contract has °C',
            'sensor.geopro_kompressori_tunnit (hours_comp, "Kompressori tunnit"):'
            ' state_class measurement, the contract has total_increasing',
            'sensor.geopro_l1_esikorotus (l1_pre_increase, "L1 Esikorotus"): unit °C, the contract has h',
            'sensor.geopro_l1_esikorotus (l1_pre_increase, "L1 Esikorotus"):'
            ' device_class temperature, the contract has duration'])

    def test_a_sensor_that_does_not_publish_again_within_its_interval_fails(self):
        # A sensor publishes every value or bank interval. A binary sensor publishes when its bit
        # changes, and the revision once at boot, so the state sent on subscribing is enough for them.
        node_counts = {**counts(self), "Maaliuos": 1, "ML VarYlä Kesä": 1, "Sähkövastus": 0}

        result = self.check(node_counts=node_counts)

        self.assertEqual(result.problems, [
            'sensor.geopro_maaliuos (brine, "Maaliuos"): only the state sent on subscribing;'
            ' a sensor publishes again every value or bank interval',
            'binary_sensor.geopro_s_hk_vastus (el_heater, "Sähkövastus"): no state message',
            'sensor.geopro_ml_varyl_kes (summer_temp, "ML VarYlä Kesä"): only the state sent on subscribing;'
            ' a sensor publishes again every value or bank interval'])

    def test_the_wrong_revision_fails(self):
        result = self.check(after_states("7f261e5"))

        self.assertEqual(result.problems, ["the Node runs Component revision 7f261e5, not 02b5199"])

    def test_a_build_with_uncommitted_changes_is_not_the_commit(self):
        result = self.check(after_states(REVISION + "-dirty"))

        self.assertEqual(result.problems, ["the Node runs Component revision 02b5199-dirty, not 02b5199"])

    def test_an_unknown_revision_fails(self):
        # The firmware's "unknown" and Home Assistant's own unknown state read the same.
        result = self.check(after_states("unknown"))

        self.assertEqual(result.problems, [
            "Home Assistant reads the Component revision as unknown: the build couldn't read git, or the Node"
            " hasn't published it. Either way the Node may not run 02b5199"])

    def test_an_unavailable_revision_fails_once(self):
        after = after_states()
        by_id(after, "sensor.geopro_komponentin_versio")["state"] = "unavailable"

        result = self.check(after)

        self.assertEqual(result.problems, [
            'sensor.geopro_komponentin_versio (component_revision, "Komponentin versio"): reads unavailable'])

    def test_notes_that_a_dirty_revision_matches_any_uncommitted_changes(self):
        result = self.check(after_states(REVISION + "-dirty"), expected=REVISION + "-dirty")

        self.assertEqual(result.problems, [])
        self.assertIn("note: a -dirty revision can't tell which uncommitted changes a build had, so any build"
                      " of 02b5199 with changes matches\n", result.text())

    def test_a_node_without_the_revision_sensor_fails(self):
        text = FLASH_CONTRACT.read_text(encoding="utf-8").replace(
            'component_revision: text_sensor "Komponentin versio" sensor.geopro_komponentin_versio\n', "")
        node_counts = counts(self)
        del node_counts["Komponentin versio"]

        result = flash_check.check_after(contract.load(TempFile(self, text).path), snapshot("states_after_flash.json"),
                                         node_counts, REVISION)

        self.assertEqual(result.problems, [
            "node.yaml sets no component_revision, so the flash check can't tell which build the Node runs"])

    def test_matches_a_revision_abbreviated_to_another_length(self):
        result = self.check(expected="02b51993cfa8")

        self.assertEqual(result.problems, [])
        self.assertIn("Component revision 02b5199 (expected 02b51993cfa8)", result.text())


class States:
    """A Home Assistant transport that answers /api/states with a snapshot."""

    def __init__(self, states):
        self.states = states

    def __call__(self, url, headers):
        assert urllib.parse.urlsplit(url).path == "/api/states", url
        return json.dumps(self.states).encode()


def phase_dir(test):
    directory = tempfile.TemporaryDirectory()
    test.addCleanup(directory.cleanup)
    return Path(directory.name) / "flash-check"


BEFORE_TIME = datetime.fromisoformat("2026-10-09T19:13:00+03:00")
AFTER_TIME = datetime.fromisoformat("2026-10-09T19:21:30+03:00")


class BeforeTest(unittest.TestCase):
    def test_saves_home_assistants_states_and_the_time(self):
        directory = phase_dir(self)
        client, _ = client_for(self, States(snapshot("states_before_flash.json")))

        result = flash_check.before(client, directory, now=BEFORE_TIME, entity_contract=flash_contract())

        self.assertEqual(json.loads((directory / "states-before.json").read_text()),
                         snapshot("states_before_flash.json"))
        self.assertEqual(json.loads((directory / "times.json").read_text()), {"before": "2026-10-09T19:13:00+03:00"})
        self.assertEqual(result.problems, [])
        self.assertIn("saved 41 states to %s" % (directory / "states-before.json"), result.text())

    def test_notes_the_node_entities_home_assistant_does_not_have_yet(self):
        # The #11 before snapshot is from the YAML protocol copy, which had no revision sensor.
        client, _ = client_for(self, States(snapshot("states_before_flash.json")))

        text = flash_check.before(client, phase_dir(self), now=BEFORE_TIME, entity_contract=flash_contract()).text()

        self.assertIn("note: Home Assistant has no sensor.geopro_komponentin_versio (component_revision) yet\n", text)
        self.assertTrue(text.endswith("passed: 36 of 37 Node entities in Home Assistant\n"), text)

    def test_notes_a_new_entity_whose_id_is_not_recorded_yet(self):
        # A flash that adds an entity: its ID can only be recorded once Home Assistant has it.
        text = FLASH_CONTRACT.read_text(encoding="utf-8").replace(
            '"Komponentin versio" sensor.geopro_komponentin_versio', '"Komponentin versio" ' + contract.NO_ENTITY_ID)
        client, _ = client_for(self, States(snapshot("states_before_flash.json")))

        result = flash_check.before(client, phase_dir(self), now=BEFORE_TIME,
                                    entity_contract=contract.load(TempFile(self, text).path))

        self.assertIn('note: component_revision ("Komponentin versio") has no entity ID recorded yet\n', result.text())


class AfterTest(unittest.TestCase):
    def setUp(self):
        self.directory = phase_dir(self)
        client, _ = client_for(self, States(snapshot("states_before_flash.json")))
        flash_check.before(client, self.directory, now=BEFORE_TIME, entity_contract=flash_contract())
        self.node, self.api = node_for(self)
        # The recorded session predates the revision sensor, which the Node sends once, on subscribing.
        self.api.session["entities"].append({"key": 99, "platform": "text_sensor", "name": "Komponentin versio"})
        self.client, _ = client_for(self, States(after_states()))

    def after(self, expected=REVISION):
        return flash_check.after(self.node, self.client, expected, seconds=0, directory=self.directory,
                                 now=AFTER_TIME, entity_contract=flash_contract())

    def test_checks_the_node_and_home_assistant_in_one_go(self):
        result = self.after()

        self.assertEqual(result.problems, [])
        text = result.text()
        self.assertTrue(text.startswith("esphome 2026.9.1 | compiled 2026-10-09 19:10:50 +0300 | name geopro-202s\n"
                                        "Component revision 02b5199 (expected 02b5199)\n"), text)
        self.assertIn("note: gone since the before snapshot: sensor.garage_geopro_l1_huone,", text)
        self.assertEqual(len(self.api.connections), 1)
        self.assertFalse(self.api.connected)

    def test_saves_the_after_snapshot_and_its_time(self):
        self.after()

        self.assertEqual(json.loads((self.directory / "states-after.json").read_text()), after_states())
        self.assertEqual(json.loads((self.directory / "times.json").read_text()),
                         {"before": "2026-10-09T19:13:00+03:00", "after": "2026-10-09T19:21:30+03:00"})

    def test_fails_on_the_wrong_revision(self):
        result = self.after("7f261e5")

        self.assertEqual(result.problems, ["the Node runs Component revision 02b5199, not 7f261e5"])

    def test_runs_without_a_before_snapshot_and_says_so(self):
        (self.directory / "states-before.json").unlink()

        result = self.after()

        self.assertEqual(result.problems, [])
        self.assertIn("note: no before snapshot in %s, so nothing to compare with\n" % self.directory, result.text())


# The entities in fixtures/history_day.json, in the format of tests/entity-contract.txt.
HISTORY_DAY_CONTRACT = """\
brine: sensor unit=°C device_class=temperature state_class=measurement accuracy=2 icon=mdi:thermometer entity_category=-
compressor: binary_sensor unit=- device_class=running state_class=- accuracy=- icon=mdi:engine entity_category=-
summer_temp: sensor unit=°C device_class=temperature state_class=measurement accuracy=0 icon=mdi:temperature-celsius entity_category=-

brine: sensor "Maaliuos" sensor.geopro_maaliuos
compressor: binary_sensor "Kompressori" binary_sensor.geopro_kompressori
summer_temp: sensor "ML VarYlä Kesä" sensor.geopro_ml_varyl_kes
"""


class OvernightTest(unittest.TestCase):
    def setUp(self):
        self.directory = phase_dir(self)
        self.directory.mkdir()
        (self.directory / "times.json").write_text(json.dumps({"after": "2026-10-09T19:21:30+03:00"}))
        self.client, self.transport = client_for(self)

    def overnight(self, text=HISTORY_DAY_CONTRACT, **kwargs):
        return flash_check.overnight(self.client, self.directory, end="2026-10-10T19:21:30+03:00",
                                     entity_contract=contract.load(TempFile(self, text).path), **kwargs)

    def test_summarises_the_history_since_the_after_phase_and_fails_on_unavailable_states(self):
        # Counted by hand from fixtures/history_day.json, as in test_day_run. The fixture is
        # trimmed, so what it says about frozen temperatures isn't checked here (OvernightFreezeTest).
        text = self.overnight().text()

        self.assertTrue(text.startswith("""\
window 2026-10-09 19:21:30+03:00 -> 2026-10-10 19:21:30+03:00 Europe/Helsinki
binary_sensor.geopro_kompressori             changes    6  unavailable 1  off -> off
sensor.geopro_maaliuos                       changes    3  unavailable 0  15.80000 -> 17.60000
sensor.geopro_ml_varyl_kes                   changes    4  unavailable 1  50.0 -> 53.0
entities: 3 | unavailable/unknown states: 2
FAIL binary_sensor.geopro_kompressori (compressor, "Kompressori"): 1 unavailable or unknown state
FAIL sensor.geopro_ml_varyl_kes (summer_temp, "ML VarYlä Kesä"): 1 unavailable or unknown state
"""), text)

    def test_asks_for_the_contracts_entities_from_the_after_time(self):
        self.overnight()

        url = urllib.parse.urlsplit(self.transport.requests[-1][0])
        self.assertEqual(urllib.parse.unquote(url.path), "/api/history/period/2026-10-09T19:21:30+03:00")
        self.assertEqual(urllib.parse.parse_qs(url.query)["filter_entity_id"],
                         ["sensor.geopro_maaliuos,binary_sensor.geopro_kompressori,sensor.geopro_ml_varyl_kes"])

    def test_takes_another_start(self):
        self.overnight(start="2026-10-10T00:00:00+03:00")

        url = urllib.parse.urlsplit(self.transport.requests[-1][0])
        self.assertEqual(urllib.parse.unquote(url.path), "/api/history/period/2026-10-10T00:00:00+03:00")

    def test_without_an_after_time_asks_for_a_start(self):
        (self.directory / "times.json").unlink()

        with self.assertRaises(SystemExit) as raised:
            self.overnight()

        self.assertIn("No after phase time in %s" % self.directory, str(raised.exception))
        self.assertIn("--start", str(raised.exception))

    def test_an_entity_without_history_fails(self):
        text = HISTORY_DAY_CONTRACT + 'tank_top: sensor "Varaaja ylä" sensor.geopro_varaaja_yl\n'

        with self.assertRaises(contract.ContractError) as raised:
            self.overnight(text)

        self.assertIn("Home Assistant has no history for sensor.geopro_varaaja_yl (tank_top", str(raised.exception))


# Two temperature Values and a Status bit, in the format of tests/entity-contract.txt.
FREEZE_CONTRACT = """\
tank_top: sensor unit=°C device_class=temperature state_class=measurement accuracy=2 icon=mdi:thermometer entity_category=-
brine: sensor unit=°C device_class=temperature state_class=measurement accuracy=2 icon=mdi:thermometer entity_category=-
compressor: binary_sensor unit=- device_class=running state_class=- accuracy=- icon=mdi:engine entity_category=-

tank_top: sensor "Varaaja ylä" sensor.geopro_varaaja_yl
brine: sensor "Maaliuos" sensor.geopro_maaliuos
compressor: binary_sensor "Kompressori" binary_sensor.geopro_kompressori
"""


class OvernightFreezeTest(unittest.TestCase):
    """The 2026-10-12 freeze, cut down: from 09:52 the Controller served the same temperatures
    until it was power-cycled, while the compressor's Status bit kept updating."""

    def overnight(self, rows):
        # Each entity's (time on 2026-10-12, state) rows, as Home Assistant's history rows.
        history = [[{"entity_id": entity_id, "state": state, "last_changed": "2026-10-12T%s+03:00" % time}
                    for time, state in entity_rows] for entity_id, entity_rows in rows.items()]
        client, _ = client_for(self, ReplayHomeAssistant(FakeClock("2026-10-12T12:30:00+03:00"), history=history))
        return flash_check.overnight(client, phase_dir(self), start="2026-10-12T09:00:00+03:00",
                                     end="2026-10-12T12:30:00+03:00",
                                     entity_contract=contract.load(TempFile(self, FREEZE_CONTRACT).path))

    def rows(self, **changes):
        rows = {
            "sensor.geopro_varaaja_yl": [("09:00:00", "50.0"), ("09:49:26", "50.5"), ("09:52:24", "50.7"),
                                         ("11:46:29", "59.4"), ("11:50:23", "59.5")],
            "sensor.geopro_maaliuos": [("09:00:00", "5.0"), ("09:31:06", "4.5"), ("11:46:29", "10.1"),
                                       ("11:47:03", "10.2")],
            "binary_sensor.geopro_kompressori": [("09:00:00", "on"), ("10:20:00", "off"), ("10:21:00", "on"),
                                                 ("11:46:30", "off")],
        }
        for entity_id, extra in changes.items():
            rows["sensor.geopro_" + entity_id] = sorted(rows["sensor.geopro_" + entity_id] + extra)
        return rows

    def test_fails_when_every_temperature_value_holds_one_value_past_the_threshold(self):
        result = self.overnight(self.rows())

        self.assertEqual(result.problems, [
            "every temperature Value held one value from 2026-10-12 09:52:24 to 11:46:29, 114 min; past 60 min"
            " the Controller may be serving frozen measurements (docs/controller.md)"])

    def test_a_node_reboot_ends_the_stretch(self):
        # At 11:16 the Node rebooted, and the frozen values came back the same.
        result = self.overnight(self.rows(varaaja_yl=[("11:16:19", "unavailable"), ("11:16:27", "50.7")],
                                          maaliuos=[("11:16:19", "unavailable"), ("11:16:27", "4.5")]))

        self.assertEqual(result.problems[-1],
                         "every temperature Value held one value from 2026-10-12 09:52:24 to 11:16:19, 83 min;"
                         " past 60 min the Controller may be serving frozen measurements (docs/controller.md)")

    def test_a_stretch_still_held_at_the_end_counts(self):
        rows = self.rows()
        rows["sensor.geopro_varaaja_yl"] = rows["sensor.geopro_varaaja_yl"][:3]
        rows["sensor.geopro_maaliuos"] = rows["sensor.geopro_maaliuos"][:2]

        result = self.overnight(rows)

        self.assertIn("from 2026-10-12 09:52:24 to 12:30:00, 157 min;", result.problems[0])

    def test_passes_when_any_temperature_value_moves(self):
        # The tank top held still the whole time, but the brine changed at least every 40 min.
        result = self.overnight(self.rows(maaliuos=[("10:20:00", "4.4"), ("11:00:00", "4.3")]))

        self.assertEqual(result.problems, [])
        self.assertTrue(result.text().endswith(
            "\npassed: 3 entities, no unavailable or unknown state, no 60 min with every temperature Value"
            " held still\n"), result.text())


def git(*args):
    return subprocess.run(["git", *args], cwd=flash_check.REPO_ROOT, check=True, capture_output=True,
                          text=True).stdout.strip()


class ExpectedRevisionTest(unittest.TestCase):
    def test_defaults_to_the_revision_a_local_build_of_this_checkout_stamps(self):
        commit, _, dirty = flash_check.expected_revision().partition("-")

        self.assertGreaterEqual(len(commit), 7)
        self.assertTrue(git("rev-parse", "HEAD").startswith(commit))
        self.assertIn(dirty, ("", "dirty"))

    def test_resolves_a_ref(self):
        self.assertEqual(flash_check.expected_revision("HEAD"), git("rev-parse", "--short=12", "HEAD"))

    def test_an_unknown_ref_says_so(self):
        with self.assertRaises(SystemExit) as raised:
            flash_check.expected_revision("no-such-ref")

        self.assertIn("no-such-ref", str(raised.exception))


class CommandLineTest(unittest.TestCase):
    def test_runs_from_any_directory(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            run = subprocess.run([sys.executable, "-I", str(flash_check.REPO_ROOT / "tools" / "flash_check.py"),
                                  "--help"], cwd=elsewhere, capture_output=True, text=True)

        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("{before,after,overnight}", run.stdout)

    def test_a_failed_check_prints_its_report_and_exits_with_status_1(self):
        directory = phase_dir(self)
        directory.mkdir()
        (directory / "times.json").write_text(json.dumps({"after": "2026-10-09T19:21:30+03:00"}))
        client, _ = client_for(self)
        entity_contract = contract.load(TempFile(self, HISTORY_DAY_CONTRACT).path)
        out = io.StringIO()
        with mock.patch.object(flash_check, "HomeAssistant", lambda: client), \
                mock.patch.object(contract, "load", lambda: entity_contract), redirect_stdout(out), \
                self.assertRaises(SystemExit) as raised:
            flash_check.main(["overnight", "--dir", str(directory), "--end", "2026-10-10T19:21:30+03:00"])

        self.assertEqual(raised.exception.code, 1)
        self.assertIn('\nFAIL binary_sensor.geopro_kompressori (compressor, "Kompressori"): 1 unavailable or unknown'
                      ' state\n', out.getvalue())
        self.assertIn("\nfailed: ", out.getvalue())


if __name__ == "__main__":
    unittest.main()
