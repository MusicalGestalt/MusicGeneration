import unittest

from . import *
from .. import (fourfour, threefour, BeatEvent)

class TestDownbeatSequence(unittest.TestCase):
    def do_test_beatgen(self, beat_gen):
        data = []
        qn = beat_gen.time_signature.quarter_note
        tpm = beat_gen.time_signature.ticks_per_measure
        for (index, item) in enumerate(beat_gen):
            if item[1] == BeatEvent.note_on:
                #down beats only happen at the start of a measure
                self.assertEqual(item[0] % tpm, 0)
            elif item[1] == BeatEvent.note_off:
                #and they're exactly one quarter note long
                self.assertEqual((item[0] - qn) % tpm, 0)
            if index > 20: break

    def test_fourfour(self):
        self.do_test_beatgen(DownbeatIntervalGenerator(fourfour))

    def test_threefour(self):
        self.do_test_beatgen(DownbeatIntervalGenerator(threefour))


def main():
    unittest.main()