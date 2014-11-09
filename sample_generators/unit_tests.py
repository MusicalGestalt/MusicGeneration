"""Unit tests for sample generators."""

from . import *

import unittest

class TestSampleGeneration(unittest.TestCase):
    def test_squarewave(self):
        sq_gen = SquareWaveGenerator(2,4)
        data = sq_gen.get(4)
        self.assertEqual(data, [1.0, -1.0, 1.0, -1.0])

        sq_gen = SquareWaveGenerator(200)
        data = sq_gen.get(40)
        self.assertEqual(data, 40 * [1.0])

    def test_sawtoothwave(self):
        saw_gen = SawtoothWaveGenerator(2,8)
        data = saw_gen.get(8)
        self.assertEqual(data, [-1.0, -0.5, 0.0, 0.5, -1.0, -0.5, 0.0, 0.5])


def main():
    unittest.main()
