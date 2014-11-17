"""These classes form a starting point for simple beat generators."""

from .. import (fourfour, TimeSignature)

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

class CompositeIntervalGenerator:
    """Given a set of interval generators, it will return the 
    next tick from ANY of the generators.

    If two generators have an event on the same tick, the tag 
    field of the tuple will contain both."""

    def __init__(self, *args):
        self.generators = args

    def __iter__(self):
        iterators = {g.tag: g.__iter__() for g in self.generators}
        primed = [next(i) for i in iterators.values()]
        while True:
            minv = min(primed, key=lambda x: x[1])[1]
            results = [p[0] for p in primed if p[1] == minv]
            resulting_tag = []
            for tag in results:
                resulting_tag += tag
            yield (resulting_tag, minv)
            primed = [p for p in primed if not p[0] in results]
            for r in results:
                primed.append(next(iterators[r[0]]))





