from .keystubs import *
from .keyboard import *
import unittest
import time

class TestSends(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock("test")
        self.server = FakeServer(self.clock)
        self.capture = KeyboardCapturer(self.clock, self.server,
            filt=keyfilter('A'))
        self.catcher = IntervalCatcher()
        self.catcher.register_interval(self.capture)
        self.clock.increment((2 * DEFAULT_SENDS) * DEFAULT_TICKS_BETWEEN)
        self.seqgen = KeyboardSequenceGenerator(self.capture)


    def test_sends(self):
        self.assertTrue(self.catcher.caught)
        intv = self.catcher.interval
        self.assertEqual(intv, [('A', 32), ('A', 32), ('A', 32)])

    def test_keys(self):
        sg = self.seqgen
        sg.new_interval(self, [('A', 43), ('A', 64)])
        acc = []
        for i in range(4):
            acc += [sg.step()]
        self.assertEqual(acc, [43,64,43,64])

def main():
    unittest.main()