import json
import re
import unittest

from tools.tests.fakes import FIXTURES

# Home Assistant's long-lived tokens are JWTs, which start with the base64 of '{"'.
JWT = re.compile(r"eyJ[\w-]+\.[\w-]+")
# A states dump carries context IDs and the user who caused each change; the token, key and
# password names catch a pasted credential.
PRIVATE_KEYS = {"context", "user_id", "parent_id", "access_token", "token", "api_encryption_key", "noise_psk",
                "ota_password", "password"}


def keys(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from keys(item)


class FixtureTest(unittest.TestCase):
    def test_fixtures_hold_no_tokens_or_context(self):
        paths = sorted(FIXTURES.glob("*.json"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path.name):
                text = path.read_text()
                self.assertIsNone(JWT.search(text))
                self.assertNotIn("Bearer", text)
                self.assertEqual(PRIVATE_KEYS & set(keys(json.loads(text))), set())


if __name__ == "__main__":
    unittest.main()
