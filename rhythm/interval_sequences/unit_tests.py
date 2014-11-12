import unittest

from . import *
from .. import (fourfour, threefour)

class TestDownbeatSequence(unittest.TestCase):
    def do_test_beatgen(self, beat_gen, offset=0):
        tpm = beat_gen.time_signature.ticks_per_measure
        for (index, item) in enumerate(beat_gen):
            self.assertEqual((item-offset) % tpm, 0)
            if index > 20: break

    def test_fourfour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(fourfour))

    def test_threefour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(threefour))

class TestMetronome(unittest.TestCase):
    def do_test_beatgen(self, beat_gen, offset=0):
        tpb = beat_gen.time_signature.ticks_per_beat
        for (index, item) in enumerate(beat_gen):
            self.assertEqual((item - offset) % tpb, 0)
            if index > 20: break

    def test_fourfour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(fourfour, 
            fourfour.ticks_per_beat))

    def test_threefour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(threefour,
            threefour.ticks_per_beat))

    def test_offbeat(self):
        self.do_test_beatgen(SimpleIntervalGenerator(fourfour,
            fourfour.ticks_per_beat, fourfour.ticks_per_beat))
        
def main():
    unittest.main()