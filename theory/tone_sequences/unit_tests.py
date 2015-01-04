"""Unit tests for sample generators."""

import unittest
from . import *
from .. import scales


class TestRandomWalk(unittest.TestCase):
    def test_randomwalk(self):
        melody_gen = RandomWalkMelodyGenerator(key=60)
        data = melody_gen.get(21)
        # Generate pentatonic scale
        valid_notes = [60, 62, 64, 68, 70]
        for shift in range(-4, 4):
            if shift == 0: continue
            valid_notes += [x + 12*shift for x in valid_notes]
        # Ensure that all notes generated on the random walk are part
        # of the pentatonic scale.
        for item in data:
            self.assertTrue(item in valid_notes)
        # In 20 random notes, they should not all be the same.
        # Test could be flaky, but it's unlikely
        self.assertTrue(max(data) > min(data))


class TestCyclic(unittest.TestCase):
    def test_cyclic(self):
        melody_gen = CyclicMelodyGenerator([i*6 for i in range(5, 16)])
        data = melody_gen.get(20)

        self.assertEqual(data, [30, 36, 42, 48, 54, 60, 66, 72, 78, 84,
                                90, 30, 36, 42, 48, 54, 60, 66, 72, 78])

    def test_cyclic_repeat(self):
        melody_gen = CyclicMelodyGenerator([60, 63, 65])
        data = []
        for (index, item) in enumerate(melody_gen):
            data.append(item)
            if len(data) >= 16: break
        data2 = data[8:]
        data = data[:8]

        self.assertEqual(data, [60, 63, 65, 60, 63, 65, 60, 63])
        self.assertEqual(data2, [65, 60, 63, 65, 60, 63, 65, 60])


class TestParametricMelodyGenerator(unittest.TestCase):
    def test_parametric(self):
        melody_gen = ParametricMelodyGenerator(key=60, length=8, scale=scales.major, num_unique_notes=8,
                 min_note=60, max_note=72, ascend_fraction=1.0)
        self.assertEqual(melody_gen.get(8), [60, 62, 64, 65, 67, 69, 71, 72])
        melody_gen = ParametricMelodyGenerator(key=60, length=8, scale=scales.major, num_unique_notes=2,
                 min_note=60, max_note=72, ascend_fraction=None)
        self.assertEqual(len(set(melody_gen.get(8))), 2)
        melody_gen = ParametricMelodyGenerator(key=48, length=16, num_unique_notes=4, ascend_fraction=0.5)
        notes = melody_gen.get(16)
        notes2 = melody_gen.get(16)
        self.assertEqual(len(set(notes)), 4)
        self.assertEqual(notes, notes2)
        self.assertEqual(len(notes), 16)



def main():
    unittest.main()

