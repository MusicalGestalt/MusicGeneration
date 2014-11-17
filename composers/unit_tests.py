"""Unit tests for composers."""

import unittest
from MusicGeneration.rhythm import fourfour
from MusicGeneration.rhythm.interval_sequences import SimpleIntervalGenerator
from MusicGeneration.theory.tone_sequences import CyclicMelodyGenerator
from . import *



class TestComposers(unittest.TestCase):
    def test_simple_composer(self):
        interval_generator = SimpleIntervalGenerator(num_ticks=fourfour.ticks_per_beat)
        melody_generator = CyclicMelodyGenerator([60, 63])
        composer = SimpleComposer(interval_generator, melody_generator)

        for phrase_id in range(3):
            phrase = composer.get_phrase() 
            self.assertEqual(phrase.phrase_endtime(), fourfour.ticks_per_beat*3 + fourfour.eighth_note)
            self.assertEqual(phrase.get_num_notes(), 4)
            for (i, note) in enumerate(phrase.notes):
                self.assertEqual(note.tone, 60 if (i % 2) == 0 else 63)
                self.assertEqual(note.start_tick, i * fourfour.ticks_per_beat)
                self.assertEqual(note.duration, fourfour.eighth_note)


def main():
    unittest.main()
