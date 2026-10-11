import asyncio
import os
import unittest
from pathlib import Path
from unittest import mock

from tools import count_states, device_info
from tools.node import Node, count_state_messages, read_device_info, secrets_file
from tools.tests.fakes import EXPECTED, FAKE_KEY, RecordedNode, TempSecrets, node_for


class SecretsTest(unittest.TestCase):
    def test_connects_with_the_key_from_secrets_yaml(self):
        node, api = node_for(self)

        node.device_info()

        self.assertEqual(api.connections, [("192.168.1.92", 6053, FAKE_KEY)])

    def test_takes_the_address_from_the_same_file(self):
        api = RecordedNode()
        secrets = TempSecrets(self, 'api_encryption_key: "%s"\nnode_address: 10.0.0.7\n' % FAKE_KEY)

        Node(secrets_path=secrets.path, api=api).device_info()

        self.assertEqual(api.connections[0][:2], ("10.0.0.7", 6053))

    def test_finds_the_file_named_by_geopro_secrets_file(self):
        api = RecordedNode()
        with mock.patch.dict(os.environ, {"GEOPRO_SECRETS_FILE": str(TempSecrets(self).path)}):
            node = Node(api=api)

        node.device_info()

        self.assertEqual(api.connections[0][2], FAKE_KEY)

    def test_defaults_to_the_secrets_yaml_next_to_geopro_yaml(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(secrets_file(), Path(__file__).resolve().parents[2] / "secrets.yaml")

    def test_a_missing_file_names_the_path_and_the_override(self):
        with self.assertRaises(SystemExit) as raised:
            Node(secrets_path="/nonexistent/secrets.yaml", api=RecordedNode())

        self.assertIn("/nonexistent/secrets.yaml", str(raised.exception))
        self.assertIn("GEOPRO_SECRETS_FILE", str(raised.exception))

    def test_a_file_without_a_key_says_so(self):
        secrets = TempSecrets(self, "ota_password: fake\n")
        with self.assertRaises(SystemExit) as raised:
            Node(secrets_path=secrets.path, api=RecordedNode())

        self.assertIn("api_encryption_key", str(raised.exception))

    def test_never_shows_the_key(self):
        node, _ = node_for(self)

        self.assertNotIn(FAKE_KEY, repr(node))
        self.assertEqual(repr(node), "Node('192.168.1.92:6053')")


class DeviceInfoTest(unittest.TestCase):
    def test_prints_the_version_and_build_time(self):
        node, api = node_for(self)

        self.assertEqual(device_info.summary(node), (EXPECTED / "device_info.txt").read_text())
        self.assertFalse(api.connected)


class CountStatesTest(unittest.TestCase):
    def test_counts_state_messages_per_entity(self):
        node, api = node_for(self)

        self.assertEqual(count_states.summary(node, 0), (EXPECTED / "count_states.txt").read_text())
        self.assertFalse(api.connected)

    def test_returns_the_counts_by_entity_name(self):
        node, _ = node_for(self)

        counts = node.count_states(0)

        # The dump on subscribing, then a Value every 10 s and a Bank setting every 60 s.
        self.assertEqual(counts["Maaliuos"], 9)
        self.assertEqual(counts["ML VarYlä Kesä"], 2)
        self.assertEqual(counts["Kompressori"], 1)


class OneConnectionTest(unittest.TestCase):
    def test_reads_device_info_and_counts_states_in_one_connection(self):
        node, api = node_for(self)

        async def both():
            async with node.connected() as client:
                return await read_device_info(client), await count_state_messages(client, 0)

        info, counts = asyncio.run(both())

        self.assertEqual(info.esphome_version, "2026.9.1")
        self.assertEqual(counts["Tila Muuttuja"], 9)
        self.assertEqual(len(api.connections), 1)
        self.assertFalse(api.connected)


if __name__ == "__main__":
    unittest.main()
