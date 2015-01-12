"""Unit tests for music theory libraries."""

import unittest

from . import scales
from . import harmonies
from . import utils


class TestScalesLib(unittest.TestCase):

    def setUp(self):
        # Misc setup
        pass

    def test_scale(self):
        self.assertEqual(scales.major(scales.middleC),
                         [60, 62, 64, 65, 67, 69, 71])
        self.assertEqual(scales.major(scales.middleC, num_notes=4),
                         [60, 62, 64, 65])
        self.assertEqual(scales.major(scales.middleC, num_notes=14),
                         [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83])
        self.assertEqual(scales.major(scales.middleC + 1, num_notes=14),
                         [x+1 for x in [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]])


    def test_getscale(self):
        scale_list = scales.get_scale_names()
        self.assertTrue("major" in scale_list)
        self.assertTrue("natural_minor" in scale_list)
        major_scale_intervals = scales.get_scale_intervals("major")
        for scale_name in scale_list:
          self.assertIsNotNone(scales.get_scale_intervals(scale_name))


class TestHarmoniesLib(unittest.TestCase):
    def test_scale(self):
        self.assertEqual(harmonies.power_chord(scales.middleC), (60, 67))


class TestUtilsLib(unittest.TestCase):
    def test_tone_to_freq(self):
        self.assertAlmostEqual(utils.ToneToFrequency(scales.middleC), 261.625565, places=3)
        self.assertAlmostEqual(utils.ToneToFrequency(69), 440, places=3)


def main():
    print("Running unit tests for 'theory' module")
    unittest.main()

if __name__ == '__main__':
    main()
