import unittest

from . import *
from .. import (fourfour, threefour, BeatEvent)

class TestDownbeatSequence(unittest.TestCase):
    def do_test_beatgen(self, beat_gen, beat_length):
        qn = beat_length
        tpm = beat_gen.time_signature.ticks_per_measure
        for (index, item) in enumerate(beat_gen):
            if item[1] == BeatEvent.note_on:
                #down beats only happen at the start of a measure
                self.assertEqual(item[0] % tpm, 0)
            elif item[1] == BeatEvent.note_off:
                #and they're exactly one beat_length long
                self.assertEqual((item[0] - qn) % tpm, 0)
            if index > 20: break

    def test_fourfour(self):
        self.do_test_beatgen(DownbeatIntervalGenerator(fourfour), 
            fourfour.quarter_note)
        self.do_test_beatgen(DownbeatIntervalGenerator(fourfour,"eighth_note"),
            fourfour.eighth_note)

    def test_threefour(self):
        self.do_test_beatgen(DownbeatIntervalGenerator(threefour),
            threefour.quarter_note)
        self.do_test_beatgen(DownbeatIntervalGenerator(threefour,"eighth_note"),
            threefour.eighth_note)

class TestMetronome(unittest.TestCase):
    def do_test_beatgen(self, beat_gen, beat_length):
        tpb = beat_gen.time_signature.ticks_per_beat
        for (index, item) in enumerate(beat_gen):
            if item[1] == BeatEvent.note_on:
                self.assertEqual(item[0] % tpb, 0)
            elif item[1] == BeatEvent.note_off:
                self.assertEqual((item[0] - beat_length) % tpb, 0)
            if index > 20: break

    def test_fourfour(self):
        self.do_test_beatgen(MetronomeIntervalGenerator(fourfour),
            fourfour.quarter_note)
        self.do_test_beatgen(MetronomeIntervalGenerator(fourfour, "eighth_note"),
            fourfour.eighth_note)

    def test_threefour(self):
        self.do_test_beatgen(MetronomeIntervalGenerator(threefour),
            threefour.quarter_note)
        self.do_test_beatgen(MetronomeIntervalGenerator(threefour, "eighth_note"),
            threefour.eighth_note)

def main():
    unittest.main()