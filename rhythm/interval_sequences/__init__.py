"""These classes form a starting point for simple beat generators."""

from .. import (fourfour, TimeSignature, BeatEvent)

class BaseIntervalGenerator:
    """
    Base class for generating beat patterns. Depends on
    time signatures.
    """
    def __init__(self, time_signature=fourfour):
        self.time_signature = time_signature

    def __iter__(self):
        last_beat = None
        while(True):
            next_event = self.step(last_beat)
            yield next_event
            last_beat = next_event

    def step(self, last_beat):
        raise AttributeError("__step is not implemented on BaseIntervalGenerator")

class DownbeatIntervalGenerator(BaseIntervalGenerator):
    """Given a time signature, this will create
    beat pattern of a down-beat at the top of the
    measure."""
    def __init__(self, time_signature=fourfour):
        super().__init__(time_signature)
    
    def step(self, last_beat):
        if not last_beat: return 0
        return last_beat + self.time_signature.ticks_per_measure

class MetronomeIntervalGenerator(BaseIntervalGenerator):
    """Given a time signature, this will create a note on
    every beat. Foo"""
    def __init__(self, time_signature=fourfour, beat_length="quarter_note"):
        super().__init__(time_signature)

    def step(self, last_beat):
        if not last_beat: return 0
        return last_beat + self.time_signature.ticks_per_beat






