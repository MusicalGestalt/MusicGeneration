"""Unit tests for music theory libraries."""

import unittest

import scales
import harmonies


#
# This file is mostly a placeholder for future tests and example code
#

class TestScalesLib(unittest.TestCase):

    def setUp(self):
        # Misc setup
        pass

    def test_scale(self):
        self.assertEqual(scales.major(60), [60, 62, 64, 65, 67, 69, 71, 72])


class TestHarmoniesLib(unittest.TestCase):

    def test_scale(self):
        self.assertEqual(harmonies.power_chord(60), (60, 67))


if __name__ == '__main__':
    unittest.main()

