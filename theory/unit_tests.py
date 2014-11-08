"""Unit tests for music theory libraries."""

import unittest

from . import scales
from . import harmonies

#
# This file is mostly a placeholder for future tests and example code
#

class TestScalesLib(unittest.TestCase):

    def setUp(self):
        # Misc setup
        pass

    def test_scale(self):
        self.assertEqual(scales.major(60), [60, 62, 64, 65, 67, 69, 71, 72])

    def test_getscale(self):
        scale_list = scales.get_scale_names()
        self.assertTrue("major" in scale_list)
        self.assertTrue("natural_minor" in scale_list)
        major_scale_intervals = scales.get_scale_intervals("major")
        for scale_name in scale_list:
          self.assertIsNotNone(scales.get_scale_intervals(scale_name))


class TestHarmoniesLib(unittest.TestCase):

    def test_scale(self):
        self.assertEqual(harmonies.power_chord(60), (60, 67))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
