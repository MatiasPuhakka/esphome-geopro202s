"""Writes the Register map's rows as C++ initializers for the host tests.

    python3 tests/export_register_map.py components/geopro_202s/register_map.py build/register_map_rows.inc

Each line is one row of VALUES, in order: its key, then a Registration with the
Address, offset, Decode rule and Poll group that __init__.py's to_code() passes to
register_value(). row_line() writes them itself, so keep it in step with to_code()
and _decode_rule(). tests/register_map.cpp includes the file. The Makefile reruns
this whenever register_map.py changes, so the tests never decode with an old copy.
"""

import importlib.util
import sys
import types


def load_register_map(path):
    # register_map.py takes only unit, device-class and state-class strings from
    # esphome.const, and the export writes none of them. A stand-in that answers
    # every name with the name itself lets this run without ESPHome installed.
    esphome = types.ModuleType("esphome")
    const = types.ModuleType("esphome.const")
    const.__getattr__ = lambda name: name
    esphome.const = const
    sys.modules["esphome"] = esphome
    sys.modules["esphome.const"] = const

    spec = importlib.util.spec_from_file_location("register_map", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def row_line(value):
    rule = value.decode
    return (
        f'{{"{value.key}", {{0x{value.address:02X}, {value.offset}, '
        f'DecodeRule({rule.width}, {"true" if rule.signed else "false"}, {rule.divisor}, 0x{rule.mask:02X}), '
        f'PollGroup::{value.group.value}}}}},'
    )


def main(register_map_path, output_path):
    register_map = load_register_map(register_map_path)
    lines = [f"// Generated from {register_map_path} by {sys.argv[0]}. Don't edit."]
    lines += [row_line(value) for value in register_map.VALUES]
    with open(output_path, "w") as output:
        output.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    # Loading register_map.py would otherwise leave a __pycache__ in the component directory.
    sys.dont_write_bytecode = True
    main(*sys.argv[1:])
