import unittest

from . import *
from .. import (fourfour, threefour)

class TestDownbeatSequence(unittest.TestCase):
    def do_test_beatgen(self, beat_gen, offset=0):
        tpm = beat_gen.time_signature.ticks_per_measure
        expected = [offset+i*tpm for i in range(20)]
        intervals = []
        for (tag, tick) in beat_gen:
            intervals.append(tick)
            if len(intervals) >= 20: break
        self.assertEqual(intervals, expected)

    def test_fourfour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(fourfour))

    def test_fourfour_call_twice(self):
        gen = SimpleIntervalGenerator(fourfour)
        tpm = fourfour.ticks_per_measure
        # TODO(Remy): We should talk about what we want these generators
        # to do. My intuition is that they should simply be streams of data
        # and if you loop 4 times through it, then loop 4 times again,
        # it would be the same as looping 8 times once.
        # Before my changes, looping 4 times to get [X] and then looping
        # 4 times again to get [Y] would result in [X]==[Y]
        #
        # Generators can be messy. Oftentimes we just want a single sample,
        # and want to be able to simply call .next()
        # Let's make Iterators, instead of generators.
        # I've rewritten interval_sequences and tone_sequences to do this.


        # Calling the interval generator twice should not return
        # the same series of values. It should return the next
        # intervals in the sequence.
        vals = []
        for (i, interval) in enumerate(gen):
            tag, tick = interval
            self.assertEqual(tick, i*tpm)
            vals.append(tick)
            if (i+1) >= 10: break
        for (i, interval) in enumerate(gen):
            tag, tick = interval
            self.assertEqual(tick, (i+10)*tpm)
            vals.append(tick)
            if (i+1) >= 10: break
        print(vals)

    def test_threefour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(threefour))

    def test_tag(self):
        testTag = "Test"
        sv = SimpleIntervalGenerator(threefour, tag=testTag)
        val = next(sv.__iter__())
        self.assertEqual(val[0][0], testTag)

class TestMetronome(unittest.TestCase):
    def do_test_beatgen(self, beat_gen, offset=0):
        tpb = beat_gen.time_signature.ticks_per_beat
        expected = [offset+i*tpb for i in range(20)]
        intervals = []
        for (tag, tick) in beat_gen:
            intervals.append(tick)
            if len(intervals) >= 20: break
        self.assertEqual(intervals, expected)

    def test_fourfour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(fourfour, 
            fourfour.ticks_per_beat))

    def test_threefour(self):
        self.do_test_beatgen(SimpleIntervalGenerator(threefour,
            threefour.ticks_per_beat))

    def test_offbeat(self):
        self.do_test_beatgen(SimpleIntervalGenerator(fourfour,
            fourfour.ticks_per_beat, fourfour.ticks_per_beat), 32)
        
class CompositeTest(unittest.TestCase):
    def test_overlap(self):
        eighth = SimpleIntervalGenerator(num_ticks=fourfour.eighth_note, 
            tag="Eighth")
        quarter = SimpleIntervalGenerator(num_ticks=fourfour.quarter_note,
            tag="Quarter")
        composite = CompositeIntervalGenerator(eighth, quarter)
        for (index, item) in enumerate(composite):
            if index > 20: break
            if index % 2 == 0:
                self.assertEqual(len(item[0]), 2)
            else:
                self.assertEqual(len(item[0]), 1)

def main():
    unittest.main()