import unittest
from . import *
from MusicGeneration.rhythm import fourfour

class TestPhrases(unittest.TestCase):
    def setUp(self):
        self.empty_phrase = Phrase([], fourfour)
        # Create phrases that are 'full' of notes: a set of N equal notes
        # with each one's duration set equal to the spacing between them.
        self.full_phrase_1 = Phrase([Note(60, 0, fourfour.whole_note)], fourfour)
        self.full_phrase_4 = Phrase([
                Note(60, i * fourfour.quarter_note, fourfour.quarter_note)
                for i in range(4)
            ], fourfour)
        self.full_phrase_8 = Phrase([
                Note(60, i * fourfour.eighth_note, fourfour.eighth_note)
                for i in range(8)
            ], fourfour)
        self.test_phrase = Phrase([
                Note(60, 0, fourfour.quarter_note),
                Note(62, fourfour.whole_note, fourfour.half_note)
            ], fourfour)

    def test_phrase_length(self):
        self.assertEqual(self.empty_phrase.phrase_endtime(), 128)
        self.assertEqual(self.full_phrase_1.phrase_endtime(), 128)
        self.assertEqual(self.full_phrase_4.phrase_endtime(), 128)
        self.assertEqual(self.full_phrase_8.phrase_endtime(), 128)
        self.assertEqual(self.test_phrase.phrase_endtime(), 256)

def main():
    unittest.main()