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


def main():
    unittest.main()

