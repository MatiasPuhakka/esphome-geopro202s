"""Tests register_map.py: each row's entity kind, and the checks it runs on its rows when it loads.

Plain Python: run with `python3 -m unittest discover -s tests -p '*_test.py'`.
"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import entity_contract
from export_register_map import load_register_map

REGISTER_MAP_PATH = Path(__file__).resolve().parent.parent / "components" / "geopro_202s" / "register_map.py"


def load(path=REGISTER_MAP_PATH):
    # load_register_map() puts an esphome stand-in in sys.modules; keep it out of other tests,
    # and keep a __pycache__ out of the component directory.
    with mock.patch.dict(sys.modules), mock.patch.object(sys, "dont_write_bytecode", True):
        return load_register_map(str(path))


register_map = load()
Value = register_map.Value
S8, U8, U16 = register_map.S8, register_map.U8, register_map.U16
BANK, VALUE = register_map.PollGroup.BANK, register_map.PollGroup.VALUE
SENSOR = register_map.EntityKind.SENSOR


def bank_row(key, offset, decode=S8, group=BANK):
    return Value(key, SENSOR, 0x0B, decode, offset=offset, address_kind=register_map.AddressKind.BANK, group=group)


def check(*rows):
    register_map.check_rows(rows)


class RegisterMapCheckTest(unittest.TestCase):
    def test_the_register_map_loads(self):
        self.assertIn("comp_lock", {value.key for value in register_map.VALUES})

    def test_a_bank_row_at_the_last_data_byte_fits(self):
        check(bank_row("last", 30))

    def test_a_bank_row_in_the_value_poll_group_passes(self):
        check(bank_row("fast", 14, group=VALUE))

    def test_a_bank_offset_past_the_data_fails(self):
        message = r"late: offset 31 \+ 1 byte\(s\) runs past the 31 data bytes of Bank 0x0B"
        with self.assertRaisesRegex(ValueError, message):
            check(bank_row("late", 31))

    def test_a_two_byte_bank_row_at_the_last_byte_fails(self):
        with self.assertRaisesRegex(ValueError, r"late: offset 30 \+ 2 byte"):
            check(bank_row("late", 30, decode=U16))

    def test_single_value_rows_that_disagree_on_reply_length_fail(self):
        message = "word and low_byte share Address 0x2D but expect 2 and 1 data bytes"
        with self.assertRaisesRegex(ValueError, message):
            check(Value("word", SENSOR, 0x2D, U16), Value("low_byte", SENSOR, 0x2D, U8))

    def test_a_bank_row_and_a_single_value_row_at_one_address_fail(self):
        message = "setting and single share Address 0x0B but expect 31 and 1 data bytes"
        with self.assertRaisesRegex(ValueError, message):
            check(bank_row("setting", 0), Value("single", SENSOR, 0x0B, S8))

    def test_rows_that_disagree_on_poll_group_fail(self):
        message = "slow and fast share Address 0x0B but are in Poll groups BANK and VALUE"
        with self.assertRaisesRegex(ValueError, message):
            check(bank_row("slow", 1), bank_row("fast", 2, group=VALUE))

    def test_a_repeated_key_fails(self):
        with self.assertRaisesRegex(ValueError, "config keys must be unique: twice"):
            check(bank_row("twice", 1), bank_row("once", 2), bank_row("twice", 3))

    def test_loading_a_register_map_with_a_bank_offset_past_the_data_fails(self):
        source = REGISTER_MAP_PATH.read_text()
        broken = source.replace('_bank_temperature("comp_lock", 0x0B, 14,', '_bank_temperature("comp_lock", 0x0B, 31,')
        self.assertNotEqual(broken, source)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register_map.py"
            path.write_text(broken)
            with self.assertRaisesRegex(ValueError, "comp_lock: offset 31"):
                load(path)


def contract_platforms():
    """Each key's platform as tests/entity-contract.txt records it, from its key lines."""
    with open(entity_contract.CONTRACT, encoding="utf-8") as file:
        lines = [line for line in file.read().splitlines() if " unit=" in line]
    return {key: platform for key, platform, *_ in (line.replace(":", "", 1).split(" ") for line in lines)}


class EntityKindTest(unittest.TestCase):
    def test_each_row_publishes_on_the_platform_the_contract_records(self):
        # Changing a row's entity kind orphans its Home Assistant entity (ADR 0004), so it
        # has to show up in the contract too. This catches it without ESPHome installed.
        platforms = contract_platforms()
        for value in register_map.VALUES:
            with self.subTest(value.key):
                self.assertEqual(value.entity_kind.value, platforms[value.key])

    def test_a_row_without_an_entity_kind_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "entity_kind"):
            Value("no_kind", address=0x12, decode=register_map.CENTI_S16)


if __name__ == "__main__":
    unittest.main()
