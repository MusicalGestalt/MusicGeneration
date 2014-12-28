"""These classes form a starting point for simple beat generators."""

import random
from .. import (fourfour, TimeSignature)
from collections import deque
from math import ceil

class BaseIntervalGenerator:
    """
    Base class for generating beat patterns. Depends on
    time signatures.

    Note that tags are returned as a list. This is to better
    support event composition. See CompositeIntervalGenerator
    """
    def __init__(self, time_signature=fourfour, tag="Basic"):
        self.time_signature = time_signature
        self.tag = tag
        self.last_beat = None

    def __iter__(self):
        return self

    def __next__(self):
        next_event = self.step(self.last_beat)
        self.last_beat = next_event
        return ([self.tag], next_event)

    def step(self, last_beat):
        raise AttributeError("__step is not implemented on BaseIntervalGenerator")


class SimpleIntervalGenerator(BaseIntervalGenerator):
    """Given a time signature and a number of ticks, this 
    generator will output intervals evenly spaced by that number of ticks."""

    def __init__(self, time_signature=fourfour, 
            num_ticks=None, start_on=0, 
            tag="Periodic"):
        super().__init__(time_signature, tag)
        if num_ticks is None:
            num_ticks = time_signature.ticks_per_measure
        assert num_ticks > 0
        self.num_ticks = num_ticks
        self.start_on = start_on
    
    def step(self, last_beat):
        if last_beat is None: return self.start_on
        return last_beat + self.num_ticks


class PatternIntervalGenerator(BaseIntervalGenerator):
    """Given a sequence of integers, this iterator can repeat
    a pattern indefinitely. Each tick is a measure-based multiple of the pattern.
    For example, in 4/4 time, the pattern [1,4,6], will have events on
    [1,4,6,9,12,15]"""
    def __init__(self, pattern, time_signature=fourfour, tag="Pattern"):
        super().__init__(time_signature, tag)
        assert len(pattern) > 0
        # A pattern like [4,6,2] is ambiguous. We could sort it by default
        # but better to throw an assertion error.
        assert pattern == sorted(pattern)

        self.__pattern = pattern
        measure_length = self.time_signature.ticks_per_measure
        self.__loop_length = ceil(pattern[-1] / measure_length) * measure_length

    @property
    def pattern(self): return self.__pattern

    def step(self, last_beat):
        if last_beat is None:
            self.__index = 0
            self.__num_cycles = 0
        else:
            self.__index = (self.__index + 1) % len(self.__pattern)
            if self.__index == 0:
                self.__num_cycles += 1
        return self.__pattern[self.__index] + self.__loop_length * self.__num_cycles


class ParametricIntervalGenerator(PatternIntervalGenerator):
    """
    A pattern interval generator defined by 4 main parameters:
        resolution = the number of slots (potential intervals) per beat in a measure.
            e.g. with resolution == 4, and 4 beats per measure, then we have 16 'slots' for intervals
        density = the fraction of slots that are intervals (range: 0...1)
        bias = the difference between the density of the first half and the second (range: -1...1)
            e.g. a bias of zero would have an equal number of intervals in the first and second
            halves of a measure.
        focus = a measure of how concentrated the intervals are on the 'main' beats
    """
    def __init__(self, density, bias=None, focus=None, resolution=4, time_signature=fourfour, tag="Parametric"):
        assert int(resolution) == resolution
        num_slots = time_signature.beats_per_measure * resolution
        # This check is in place to prevent expensive computation;
        # It can be lifted once I implement a more efficient algorithm.
        assert num_slots <= 16
        assert density > 0 and density <= 1.0
        num_triggers = int(density * num_slots)
        assert num_triggers > 0
        focus_weights = self.__get_focus_weights(num_slots)
        min_focus = sum(sorted(focus_weights)[:num_triggers])
        max_focus = sum(sorted(focus_weights, reverse=True)[:num_triggers])

        # slots is essentially a binary vector, indicating whether an interval happens.
        slots = [1] * num_triggers + [0] * (num_slots - num_triggers)
        assert sum(slots) == num_triggers

        mid = int(num_slots / 2)
        M = min([num_triggers, num_slots - num_triggers])
        if (num_slots % 2) == 0:
            curr_bias = lambda b: (sum(b[mid:]) - sum(b[:mid])) / M
        else:
            curr_bias = lambda b: (sum(b[mid+1:]) - sum(b[:mid])) / M
        # Normalized dot-product of focus_weights and slots
        curr_focus = lambda b: (sum([a*b for (a,b) in zip(focus_weights, b)]) - min_focus) / max([0.001, max_focus - min_focus])

        best_slots = slots
        best_score = float('inf')
        best_candidates = []
        # Iterate through all possible binary vectors with the chosen density
        # and determine which ones best match the (bias, focus) metrics
        # TODO(oconaire): This could be incredibly slow for some parameter choices.
        # For example, if resolution=8 and density=0.5, we have 32 choose 16 = 601080390
        # valid vectors to try.
        while slots:
            cost = 0.0
            if bias is not None:
                cost += abs(bias - curr_bias(slots))
            if focus is not None:
                cost += abs(focus - curr_focus(slots))

            if cost < best_score:
                best_slots = slots
                best_score = cost
                best_candidates = []
            elif cost == best_score:
                best_candidates.append(slots)

            slots = self.__increment_slots(slots)
            if not slots: break

        if best_candidates:
            # We have to choose from several top matches
            best_candidates.append(best_slots)
            best_slots = random.choice(best_candidates)

        print(curr_bias(best_slots), curr_focus(best_slots))

        assert (time_signature.ticks_per_beat % resolution) == 0
        multiplier = time_signature.ticks_per_beat / resolution
        pattern = [p * multiplier for (p,v) in enumerate(best_slots) if v == 1]
        print(best_slots)
        PatternIntervalGenerator.__init__(self, pattern, time_signature=time_signature, tag=tag)

    def __increment_slots(self, slots):
        # Find rightmost '0'
        i0 = max([p for (p,v) in enumerate(slots) if v == 0])
        # Find rightmost '1' (that occurs before rightmost 0)
        candidates = [p for (p,v) in enumerate(slots) if v == 1 and p < i0]
        if not candidates: return None
        i1 = max(candidates)
        assert slots[i0] == 0
        assert slots[i1] == 1
        assert i1 < i0
        c1 = sum(slots[i1:])
        c0 = len(slots) - i1 - sum(slots[i1:])
        new_slots = slots[:i1] + [0] + ([1] * c1) + ([0] * (c0-1))
        assert len(new_slots) == len(slots)
        return new_slots

    def __get_focus_weights(self, n):
        weights = [0] * n;
        k = n
        while k > 1:
            divisor = k
            for i in range(2, k):
                if (k % i) == 0:
                    divisor = i
                    break
            assert divisor > 1
            assert (k % divisor) == 0
            k = int(k / divisor)
            for i in range(0, n, k):
                weights[i] += 1
        return weights



class CompositeIntervalGenerator:
    """Given a set of interval generators, it will return the 
    next tick from ANY of the generators.

    If two generators have an event on the same tick, the tag 
    field of the tuple will contain both."""

    # TODO(oconaire): Rewrite this to be a BaseIntervalGenerator. 

    def __init__(self, *args):
        self.generators = args

    def __iter__(self):
        self.__start();
        return self;

    def __reprime(self, consumed_tags):
        self.__primed = [p for p in self.__primed if not p[0] in consumed_tags]
        for ct in consumed_tags:
            next_val = next(self.__iterators[ct[0]])
            self.__primed.append(next_val)

    def __start(self):
        #grab the iterators from all of the sub-generators
        self.__iterators = {g.tag: g.__iter__() for g in self.generators}
        #prime the pump by getting the next tick from every iterator
        self.__primed = [next(i) for i in self.__iterators.values()]

    def __next__(self):
        # look at the primed pump, and find the lowest tick
        minv = min(self.__primed, key=lambda x: x[1])[1]; 
        # find all of the generators with an event on that tick
        result_tags = [p[0] for p in self.__primed if p[1] == minv]
        self.__reprime(result_tags)
        return (result_tags, minv)

