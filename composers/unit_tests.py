"""Unit tests for composers."""

import unittest
from MusicGeneration.rhythm import fourfour
from MusicGeneration.rhythm.interval_sequences import SimpleIntervalGenerator
from MusicGeneration.theory.tone_sequences import CyclicMelodyGenerator
from . import *



class TestComposers(unittest.TestCase):
    def test_simple_composer(self):
        interval_generator = SimpleIntervalGenerator(num_ticks=fourfour.ticks_per_beat)
        melody_generator = CyclicMelodyGenerator([60, 63])
        composer = SimpleComposer(interval_generator, melody_generator)

        for phrase_id in range(3):
            phrase = composer.get_phrase() 
            self.assertEqual(phrase.phrase_endtime(), 128) #this rounds to the nearest measure end
            self.assertEqual(phrase.get_num_notes(), 4)
            for (i, note) in enumerate(phrase.notes):
                self.assertEqual(note.tone, 60 if (i % 2) == 0 else 63)
                self.assertEqual(note.start_tick, i * fourfour.ticks_per_beat)
                self.assertEqual(note.duration, fourfour.eighth_note)

@EventReceiver("test", "event_handler")
class EventHandler:
    def __init__(self):
        self.got_event = False
        self.details = None
    def event_handler(self, details):
        self.got_event = True
        self.details = details

@EventReceiver("test", "rename")
class RenameEventHandler:
    def rename(self, details): pass

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
        self.instance.add_test_observer(self.handler)
        self.assertEqual(len(self.instance.get_test_observers()), 1)

    def test_remove(self):
        self.test_add()
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
