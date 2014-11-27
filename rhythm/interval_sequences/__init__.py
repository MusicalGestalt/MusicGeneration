"""These classes form a starting point for simple beat generators."""

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
        
    def step(self, last_beat):
        if last_beat is None:
            self.__index = 0
            self.__num_cycles = 0
        else:
            self.__index = (self.__index + 1) % len(self.__pattern)
            if self.__index == 0:
                self.__num_cycles += 1
        return self.__pattern[self.__index] + self.__loop_length * self.__num_cycles


class CompositeIntervalGenerator:
    """Given a set of interval generators, it will return the 
    next tick from ANY of the generators.

    If two generators have an event on the same tick, the tag 
    field of the tuple will contain both."""

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

