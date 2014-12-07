"""Unit tests for clock, events, composers."""

import time
import unittest
from MusicGeneration.rhythm import fourfour
from MusicGeneration.rhythm.interval_sequences import SimpleIntervalGenerator
from MusicGeneration.theory.tone_sequences import CyclicMelodyGenerator
from MusicGeneration.composers.clock import Clock
from . import *

# === Tests for Clock ===

@EventReceiver("tick", "ticked")
class ClockHandler:
    def __init__(self):
        self.ticks = []

    def ticked(self, sender, details):
        self.ticks.append(details)


class TestClock(unittest.TestCase):
    """Since time.sleep has unknown accuracy, these tests
    have to be a little bit sloppy."""  
    def test_clock(self):
        handle = ClockHandler()
        cl = Clock("conductor", 32)
        cl.add_tick_observer(handle)
        cl.start()
        time.sleep(1)
        cl.stop()
        self.assertLessEqual(30, len(handle.ticks))
        self.assertLessEqual(len(handle.ticks), 34)

    def test_speed_change(self):
        handle = ClockHandler()
        cl = Clock("conductor", 32)
        cl.add_tick_observer(handle)
        cl.start()
        time.sleep(0.5)
        cl.ticks_per_second = 64
        time.sleep(0.55)
        cl.stop()
        self.assertLessEqual(44, len(handle.ticks))
        self.assertLessEqual(len(handle.ticks), 54)


# === Tests for Composers ===

@EventReceiver("phrase", "phrase_handler")
class TestSimpleComposer(unittest.TestCase):
    def setUp(self):
        interval_generator = SimpleIntervalGenerator(num_ticks=fourfour.ticks_per_beat)
        melody_generator = CyclicMelodyGenerator([60, 63])
        self.composer = SimpleComposer(interval_generator, melody_generator)
        self.composer.add_phrase_observer(self)
        self.num_phrases_observed = 0

    def test_simple_composer(self):
        # Very fast clock (for shorter test)
        cl = Clock("conductor", 32000)
        cl.add_tick_observer(self.composer)
        cl.start()

        # Sleep for (at most) 5 seconds
        total_sleep = 0.0
        while self.num_phrases_observed < 3:
            time.sleep(0.1)
            total_sleep += 0.1
            if total_sleep > 5:
                break
        self.assertGreaterEqual(self.num_phrases_observed, 3)

    def phrase_handler(self, sender, phrase):
        self.assertEqual(sender, self.composer)
        self.num_phrases_observed += 1
        # Phrase should be one measure lone
        self.assertEqual(phrase.phrase_endtime(), 128)
        self.assertEqual(phrase.get_num_notes(), 4)
        for (i, note) in enumerate(phrase.notes):
            self.assertEqual(note.tone, 60 if (i % 2) == 0 else 63)
            self.assertEqual(note.start_tick, i * fourfour.ticks_per_beat)
            self.assertEqual(note.duration, fourfour.eighth_note)


# === Tests for Event Sending/Handling ===

@EventReceiver("test", "event_handler")
class EventHandler:
    def __init__(self):
        self.got_event = False
        self.details = None
    def event_handler(self, sender, details):
        self.got_event = True
        self.details = details

@EventReceiver("test", "rename")
class RenameEventHandler:
    def rename(self, sender, details): pass

@EventSender("test")
class EventTest:
    pass

class TestObservableAndObservers(unittest.TestCase):

    def setUp(self):
        self.instance = EventTest()
        self.handler = EventHandler()

    def test_method_creation(self):
        self.assertTrue(hasattr(self.instance, "add_test_observer"))
        self.assertTrue(hasattr(self.instance, "remove_test_observer"))
        self.assertTrue(hasattr(self.instance, "send_test_event"))
        self.assertTrue(hasattr(RenameEventHandler(), "test_event"))

    def test_add(self):
        self.assertEqual(len(self.instance.get_test_observers()), 0)
        self.instance.add_test_observer(self.handler)
        self.assertEqual(len(self.instance.get_test_observers()), 1)

    def test_remove(self):
        self.assertEqual(len(self.instance.get_test_observers()), 0)
        self.test_add()
        self.assertEqual(len(self.instance.get_test_observers()), 1)
        self.instance.remove_test_observer(self.handler)
        self.assertEqual(len(self.instance.get_test_observers()), 0)

    def test_send(self):
        self.test_add()
        value = "success"
        self.instance.send_test_event(value)
        self.assertTrue(self.handler.got_event)
        self.assertEqual(self.handler.details, value)


def main():
    unittest.main()
