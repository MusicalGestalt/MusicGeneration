"""Unit tests for rhythm helpers."""

from . import *

import unittest

class TestTimeSignature(unittest.TestCase):
    def setUp(self): pass

    def test_fourfour(self):
        fourfour = TimeSignature()
        self.assertEqual(fourfour.ticks_per_measure, 128)
        self.assertEqual(fourfour.quarter_note, 32)
        self.assertEqual(fourfour.beats_per_measure, 4)

def main():
    unittest.main()
