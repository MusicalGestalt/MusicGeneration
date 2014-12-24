"""These classes form a starting point for simple melody generators."""

from ..scales import (major_pentatonic, minor_pentatonic, octaves_for_note, 
    minC, maxC, middleC)
import random


class MelodyGenerator:
    def __init__(self, key=middleC):
        self.key = key

    def __iter__(self):
        return self

    def __next__(self):
        tone = self._get()
        assert tone >= minC
        assert tone <= maxC
        return tone

    def _get(self):
        raise Exception("Not implemented")

    def key():
        doc = "The root note of the scale."
        def fget(self):
            return self._key
        def fset(self, value):
            self._key = value
        def fdel(self):
            del self._key
        return locals()
    key = property(**key())


class RandomWalkMelodyGenerator(MelodyGenerator):
    """Given a key and a scale formula, this iterator returns a random
    walk through the scale."""
    def __init__(self, key=middleC, scale=major_pentatonic, max_step=4):
        """Defaults to generating all of the major pentatonic notes for 
        the entire possible scale. Using major or minor pentatonics 
        guarantees that the generated random walk melody will always
        FIT whatever else is going on, assuming you've got the same 
        root note."""
        MelodyGenerator.__init__(self, key)
        self.starting_notes = octaves_for_note(key)
        self.possibles = scale(self.starting_notes[0], num_notes=51)
        self.possibles = [n for n in self.possibles if n >= minC and n <= maxC]
        self.max_step = 4
        self.next_idx = self.possibles.index(self.key)
        self.steps = list(range(-1 * self.max_step, self.max_step + 1))

    def _get(self):
        old_idx = self.next_idx
        self.next_idx += random.choice(self.steps)
        if self.next_idx < 0: self.next_idx = 0
        if self.next_idx >= len(self.possibles): self.next_idx = len(self.possibles) - 1
        return self.possibles[old_idx]

    def starting_notes():
        doc = "Every octave of the root note of the scale"
        def fget(self):
            return self._starting_notes
        def fset(self, value):
            self._starting_notes = value
        def fdel(self):
            del self._starting_notes
        return locals()
    starting_notes = property(**starting_notes())
    def possibles():
        doc = "Every possible note contained in every octave of the scale"
        def fget(self):
            return self._possibles
        def fset(self, value):
            self._possibles = value
        def fdel(self):
            del self._possibles
        return locals()
    possibles = property(**possibles())
    def max_step():
        doc = """The largest "leap" the random walk may take"""
        def fget(self):
            return self._max_step
        def fset(self, value):
            self._max_step = value
        def fdel(self):
            del self._max_step
        return locals()
    max_step = property(**max_step())


class CyclicMelodyGenerator(MelodyGenerator):
    """Given a set of notes, this iterator cycles through them."""
    def __init__(self, tone_list, key=None):
        assert type(tone_list) in [tuple, list]
        # If the key is not provided, make a guess.
        key = key if key else tone_list[0]
        MelodyGenerator.__init__(self, key=key)
        self._tone_list = tone_list
        self._index = 0

    def _get(self):
        old_index = self._index
        self._index = (self._index + 1) % len(self._tone_list)
        return self._tone_list[old_index]

