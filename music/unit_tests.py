import unittest
from . import *
from MusicGeneration.rhythm import fourfour

class TestPhrases(unittest.TestCase):
    def setUp(self):
        self.empty_phrase = Phrase([], fourfour)
        self.phrase = Phrase([
                Note(60, 0, fourfour.quarter_note),
                Note(62, fourfour.whole_note, fourfour.half_note)
            ], fourfour)

    def test_phrase_length(self):
        self.assertEqual(self.empty_phrase.phrase_endtime(), 128)
        self.assertEqual(self.phrase.phrase_endtime(), 256)

def main():
    unittest.main()