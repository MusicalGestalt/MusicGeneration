"""Unit tests for sample generators."""

import unittest
from . import *
from .. import scales


class TestRandomWalk(unittest.TestCase):
    def test_randomwalk(self):
        melody_gen = RandomWalkMelodyGenerator(key=60)
        data = []
        for (index, item) in enumerate(melody_gen):
            data.append(item)
            if index > 20: break
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
        data = []
        for (index, item) in enumerate(melody_gen):
            data.append(item)
            if len(data) >= 20: break

        self.assertEqual(data, [30, 36, 42, 48, 54, 60, 66, 72, 78, 84,
                                90, 30, 36, 42, 48, 54, 60, 66, 72, 78])



def main():
    unittest.main()

