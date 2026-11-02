"""Tests for the fixture sanitizer: identifying values must never survive."""
import unittest

from _common import sanitize


class SanitizeTests(unittest.TestCase):
    def test_identifying_keys_hashed_and_stable(self):
        src = {"name": "Realcharname", "battletag": "Person#1234",
               "level": 90, "items": [{"name": "Some Dagger", "level": 250}]}
        a, b = sanitize(src, salt="s"), sanitize(src, salt="s")
        self.assertEqual(a, b)
        self.assertNotIn("Realcharname", str(a))
        self.assertNotIn("Person#1234", str(a))
        self.assertEqual(a["level"], 90)
        self.assertEqual(a["items"][0]["level"], 250)

    def test_salt_changes_hash(self):
        self.assertNotEqual(sanitize({"name": "x"}, "a"), sanitize({"name": "x"}, "b"))


if __name__ == "__main__":
    unittest.main()
