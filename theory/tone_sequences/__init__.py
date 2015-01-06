"""These classes form a starting point for simple melody generators."""

from ..scales import (major_pentatonic, minor_pentatonic, octaves_for_note, 
    minC, maxC, middleC)
import random


# Helper function
def get_notes_in_key(key, scale):
    starting_notes = octaves_for_note(key)
    possibles = scale(starting_notes[0], num_notes=12*8)
    possibles = [n for n in possibles if n >= minC and n <= maxC]
    return possibles


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

    def get(self, length):
        return [self.__next__() for i in range(length)]

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


class ParametricMelodyGenerator(CyclicMelodyGenerator):
    """This iterator cycles through a melody composed from the given parameters.

    length = length of the cycle (number of notes)
    num_unique_notes = number of unique notes in the cycle
    ascend_fraction = (desired) fraction of consecutive note pairs that ascend (note_1 < note_2)
    """
    def __init__(self, key, length, scale=major_pentatonic, num_unique_notes=None,
                 min_note=minC, max_note=maxC, ascend_fraction=None, attempts=100):
        assert length > 0
        assert attempts > 0
        assert num_unique_notes is None or num_unique_notes <= length
        assert num_unique_notes is None or num_unique_notes >= 1
        note_candidates = get_notes_in_key(key, scale)
        note_candidates = [n for n in note_candidates if n >= min_note and n <= max_note]
        assert note_candidates
        assert len(note_candidates) > 1 or (num_unique_notes is None or num_unique_notes == 1)
        assert num_unique_notes is None or num_unique_notes <= len(note_candidates)

        best_tone_list = []
        best_score = float('inf')
        # Use a simple approach to find a note cycle that meets the requested parameters
        # Basically, generate a series of random patterns and score each one: Use the best found.
        for attempt in range(attempts):
            if num_unique_notes is None:
                tone_list = [random.choice(note_candidates) for i in range(length)]
            else:
                tone_list = random.sample(note_candidates, num_unique_notes)
                assert len(tone_list) == num_unique_notes
                while len(tone_list) < length:
                    # Insert one of the 'unique' notes from the set
                    tone_list.append(random.choice(tone_list[:num_unique_notes]))
                assert len(set(tone_list)) == num_unique_notes

            assert len(tone_list) == length
            if ascend_fraction == 0.0:
                tone_list = sorted(tone_list, reverse=True)
            elif ascend_fraction == 1.0:
                tone_list = sorted(tone_list)
            else:
                random.shuffle(tone_list)

            # score the resulting tone_list
            score = 0.0
            if length > 1 and ascend_fraction is not None:
                ascends = 0
                for i in range(length-1):
                    if tone_list[i] < tone_list[i+1]:
                        ascends += 1
                score = abs(1.0 * ascends / (length - 1) - ascend_fraction)

            if score < best_score:
                best_score = score
                best_tone_list = tone_list

        CyclicMelodyGenerator.__init__(self, best_tone_list, key=key)
