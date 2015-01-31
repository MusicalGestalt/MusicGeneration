from .keystubs import *
from .keyboard import *
import unittest
import time

class TestSends(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock("test")
        self.server = FakeServer(self.clock)
        self.capture = KeyboardCapturer(self.clock, self.server)
        self.catcher = IntervalCatcher()
        self.catcher.register_interval(self.capture)
        self.clock.increment((2 * DEFAULT_SENDS) * DEFAULT_TICKS_BETWEEN)


    def test_sends(self):
        self.assertTrue(self.catcher.caught)
        intv = self.catcher.interval
        self.assertEqual(intv, [('A', 32), ('A', 32), ('A', 32)])

def main():
    unittest.main()