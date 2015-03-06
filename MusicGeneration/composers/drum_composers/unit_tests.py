"""Unit tests for clock, events, composers."""

import time
import unittest
from MusicGeneration.rhythm import fourfour
from MusicGeneration.composers.clock import Clock, BasicClock
from . import *

# === Tests for DrumComposers ===

@EventReceiver("phrase", "phrase_handler")
class TestSimpleDrumComposer(unittest.TestCase):
    def setUp(self):
        gap = fourfour.eighth_note
        self.drum_composer = SimpleDrumComposer([0, gap, gap*5, gap*6, gap*7], drum_type=BASS)
        self.drum_composer.add_phrase_observer(self)
        self.num_phrases_observed = 0

    def test_simple_drum_composer(self):
        cl = BasicClock("conductor")
        cl.add_tick_observer(self.drum_composer)
        while self.num_phrases_observed < 3:
            cl.increment(32)
        self.assertGreaterEqual(self.num_phrases_observed, 3)

    def phrase_handler(self, sender, phrase):
        self.assertEqual(sender, self.drum_composer)
        self.num_phrases_observed += 1
        # Phrase should be one measure long
        self.assertEqual(phrase.phrase_endtime(), 128)
        self.assertEqual(phrase.get_num_notes(), 5)
        print("Observed phrase %d" % self.num_phrases_observed)
        expected_tick = [0, 16, 16*5, 16*6, 16*7]
        for (i, note) in enumerate(phrase.notes):
            print("  Note %d: %d %d %d" % (i+1, note.tone, note.start_tick, note.duration))
            self.assertTrue(note.tone in [10, 12, 13])
            self.assertEqual(note.start_tick, expected_tick[i])
            self.assertEqual(note.duration, fourfour.eighth_note)

def main():
    unittest.main()
