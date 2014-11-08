"""Unit tests for rhythm helpers."""

from . import *

import unittest

class TestTimeSignature(unittest.TestCase):
    def setUp(self): pass

    def test_fourfour(self):
        self.assertEqual(fourfour.ticks_per_measure, 128)
        self.assertEqual(fourfour.quarter_note, 32)
        self.assertEqual(fourfour.beats_per_measure, 4)

    def test_sixeight(self):
        self.assertEqual(sixeight.ticks_per_measure, 192)
        self.assertEqual(sixeight.quarter_note, 64)

def main():
    unittest.main()
