# Tests the Makefile's ESPHome targets against a fake esphome script, so they run
# without ESPHome installed. `make test` runs it.
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Answers `esphome version` with $FAKE_VERSION. For `esphome config` it prints a config on
# stdout and $FAKE_LOG on stderr. It logs every call to $FAKE_CALLS.
FAKE_ESPHOME = '''#!/bin/sh
echo "$@" >> "$FAKE_CALLS"
case "$1" in
  version) echo "Version: $FAKE_VERSION" ;;
  config) echo "esphome:"; printf '%b' "$FAKE_LOG" >&2 ;;
esac
'''


class EsphomeTargetsTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.esphome = self.tmp / 'bin' / 'esphome'
        self.esphome.parent.mkdir()
        self.esphome.write_text(FAKE_ESPHOME)
        self.esphome.chmod(0o755)
        self.calls = self.tmp / 'calls'
        self.calls.touch()
        self.env = {key: value for key, value in os.environ.items()
                    if key not in ('MAKEFLAGS', 'MFLAGS', 'MAKELEVEL')}
        self.env.update(FAKE_VERSION='2026.9.1', FAKE_CALLS=str(self.calls), FAKE_LOG='')

    def make(self, target, esphome=None, **fake):
        self.env.update(fake)
        return subprocess.run(
            ['make', '--no-print-directory', target, f'ESPHOME={esphome or self.esphome}',
             f'BUILD_DIR={self.tmp / "build"}'],
            cwd=ROOT, env=self.env, capture_output=True, text=True)

    def assertRefused(self, result, version):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(f'is ESPHome {version}', result.stdout)
        self.assertIn('2026.9.x', result.stdout)
        self.assertIn('ESPHOME=/path/to/esphome', result.stdout)

    def test_every_esphome_target_refuses_an_older_esphome(self):
        for target in ('check-config', 'check-node-config', 'check-trace-config',
                       'check-contract', 'update-contract', 'compile', 'compile-node'):
            with self.subTest(target):
                self.assertRefused(self.make(target, FAKE_VERSION='2025.2.2'), '2025.2.2')
        # Each target asked for the version and ran nothing else.
        self.assertEqual(self.calls.read_text(), 'version\n' * 7)

    def test_node_config_check_prints_warnings_when_it_passes(self):
        result = self.make('check-node-config', FAKE_LOG=(
            'INFO Reading configuration geopro.yaml...\n'
            'WARNING GPIO12 is a strapping PIN\nSee https://esphome.io/guides/faq/\n'
            'INFO Configuration is valid!\n'))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('WARNING GPIO12 is a strapping PIN\nSee https://esphome.io/guides/faq/\n',
                      result.stdout)
        self.assertNotIn('INFO', result.stdout)

    def test_node_config_check_fails_on_a_deprecation(self):
        result = self.make('check-node-config',
                           FAKE_LOG='WARNING The "foo" option is deprecated\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('WARNING The "foo" option is deprecated', result.stdout)

    def test_contract_check_runs_the_python_next_to_esphome(self):
        python = self.esphome.parent / 'python'
        python.write_text('#!/bin/sh\necho "python $@" >> "$FAKE_CALLS"\n')
        python.chmod(0o755)
        result = self.make('check-contract')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('python tests/entity_contract.py check', self.calls.read_text())

    def test_refuses_a_newer_series(self):
        self.assertRefused(self.make('check-config', FAKE_VERSION='2026.10.0'), '2026.10.0')

    def test_refuses_a_missing_esphome(self):
        self.assertRefused(self.make('check-config', esphome=self.tmp / 'none'), '(not found)')

    def test_runs_any_2026_9_release(self):
        result = self.make('check-config', FAKE_VERSION='2026.9.3')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('config tests/all-keys.yaml', self.calls.read_text())


if __name__ == '__main__':
    unittest.main()
