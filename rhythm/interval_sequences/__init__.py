"""These classes form a starting point for simple beat generators."""

from .. import (fourfour, TimeSignature)

class BaseIntervalGenerator:
    """
    Base class for generating beat patterns. Depends on
    time signatures.
    """
    def __init__(self, time_signature=fourfour, tag="Basic"):
        self.time_signature = time_signature
        self.tag = tag

    def __iter__(self):
        last_beat = None
        while(True):
            next_event = self.step(last_beat)
            yield (self.tag, next_event)
            last_beat = next_event

    def step(self, last_beat):
        raise AttributeError("__step is not implemented on BaseIntervalGenerator")

class SimpleIntervalGenerator(BaseIntervalGenerator):
    """Given a time signature and a number of ticks, this 
    generator will output intervals evenly spaced by that number of ticks."""

    def __init__(self, time_signature=fourfour, 
            num_ticks=fourfour.ticks_per_measure, start_on=0, 
            tag="Periodic"):
        super().__init__(time_signature, tag)
        self.num_ticks = num_ticks
        self.start_on = start_on
    
    def step(self, last_beat):
        if not last_beat: return self.start_on
        return last_beat + self.num_ticks






