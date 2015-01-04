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


class TestPattern(unittest.TestCase):
    def test_pattern(self):
        """
        q r q q qe
        """
        pattern = [
            0,
            fourfour.quarter_note * 2,
            fourfour.quarter_note * 3,
            fourfour.quarter_note * 4,
            fourfour.quarter_note * 4 + fourfour.eighth_note
        ]
        pi = PatternIntervalGenerator(pattern)
        expected = pattern + [p + fourfour.ticks_per_measure * 2 for p in pattern]
        for (index, item) in enumerate(pi):
            if index > 9: break
            self.assertEqual(item[1], expected[index])


class TestParametric(unittest.TestCase):
    def test_parametric(self):
        # Bias test
        pi = ParametricIntervalGenerator(density=0.5, bias=-1, swing=None)
        expected_intervals = [0, 8, 16, 24, 32, 40, 48, 56]
        self.assertEqual(pi.pattern, expected_intervals)
        pi = ParametricIntervalGenerator(density=0.5, bias=1, swing=None)
        self.assertEqual(pi.pattern, [i+64 for i in expected_intervals])
        # Focus test
        pi = ParametricIntervalGenerator(density=0.25, bias=None, swing=1.0)
        self.assertTrue(0 not in pi.pattern)
        self.assertTrue(64 not in pi.pattern)
        pi = ParametricIntervalGenerator(density=0.25, bias=None, swing=0.0)
        expected_intervals = [0, 32, 64, 96]
        self.assertEqual(pi.pattern, expected_intervals)
        pi = ParametricIntervalGenerator(density=0.5, bias=0.0, swing=0.6)
        self.assertEqual(len(pi.pattern), 8)
        # TODO(oconaire): Add tests with different time signatures.

        
class TestComposite(unittest.TestCase):
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