"""Public tests visible to the tool-calling contestant."""
import unittest
from slug import make_slug


class SlugTests(unittest.TestCase):
    def test_spaces_and_case(self):
        self.assertEqual(make_slug("  Hello World  "), "hello-world")

    def test_punctuation(self):
        self.assertEqual(make_slug("A__B + C"), "a-b-c")

    def test_already_clean(self):
        self.assertEqual(make_slug("alpha123"), "alpha123")

    def test_punctuation_only(self):
        self.assertEqual(make_slug("!!!"), "")


if __name__ == "__main__":
    unittest.main()
