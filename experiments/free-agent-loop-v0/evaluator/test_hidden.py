"""Evaluator-only tests. Must never be copied into agent's tool-visible workspace."""
import unittest
from slug import make_slug


class HiddenSlugTests(unittest.TestCase):
    def test_repeated_mixed_separators(self):
        self.assertEqual(make_slug("  A...b---c_+_9 "), "a-b-c-9")

    def test_empty(self):
        self.assertEqual(make_slug(""), "")

    def test_uppercase_with_digit(self):
        self.assertEqual(make_slug("V2 API"), "v2-api")

    def test_unicode_is_separator(self):
        self.assertEqual(make_slug("Café déjà vu"), "caf-d-j-vu")

    def test_leading_trailing_nonalnum(self):
        self.assertEqual(make_slug("--x&&"), "x")


if __name__ == "__main__":
    unittest.main()
