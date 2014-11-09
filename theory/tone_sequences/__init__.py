"""These classes form a starting point for simple melody generators."""

from ..scales import (major_pentatonic, minor_pentatonic, octaves_for_note, 
    minC, maxC, middleC)
import random

class RandomWalkMelodyGenerator:
    """Given a key and a scale formula, this iterator returns a random
    walk through the scale. 

    This isn't quite exactly unit-testable."""
    def __init__(self, key=middleC, scale=major_pentatonic, max_step=4):
        """Defaults to generating all of the major pentatonic notes for 
        the entire possible scale. Using major or minor pentatonics 
        guarantees that the generated random walk melody will always
        FIT whatever else is going on, assuming you've got the same 
        root note."""
        self.key = key
        self.starting_notes = octaves_for_note(key)
        self.possibles = scale(self.starting_notes[0],num_notes=51)
        self.max_step = 4

    def __iter__(self):
        next_idx = self.possibles.index(self.key)
        steps = list(range(-1 * self.max_step, self.max_step))
        while True:
            yield self.possibles[next_idx]
            next_idx += random.choice(steps)
            if next_idx < minC: next_idx = minC
            if next_idx > maxC: next_idx = maxC

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