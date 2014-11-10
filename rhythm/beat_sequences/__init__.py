"""These classes form a starting point for simple beat generators."""

from .. import (fourfour, TimeSignature, BeatEvent)

class BaseIntervalGenerator:
    """
    Base class for generating beat patterns. Depends on
    time signatures.
    """
    def __init__(self, time_signature=fourfour, beat_length="quarter_note"):
        self.time_signature = time_signature
        if isinstance(beat_length, str):
            self.note_length = getattr(time_signature, beat_length)
        else:
            self.note_length = beat_length

class DownbeatIntervalGenerator(BaseIntervalGenerator):
    """Given a time signature, this will create
    beat pattern of a down-beat at the top of the
    measure."""
    def __init__(self, time_signature=fourfour, beat_length="quarter_note"):
        super().__init__(time_signature, beat_length)

    def __iter__(self):
        next_event = (0, BeatEvent.note_on)
        last_downbeat = 0
        while (True):
            yield next_event
            if next_event[1] == BeatEvent.note_on: #we just emitted a down beat
                last_downbeat = next_event[0]
                next_event = (next_event[0] + self.note_length,
                    BeatEvent.note_off) #so the next thing we emit 
                                        #is an end to the note
            else:
                next_event = (last_downbeat + self.time_signature.ticks_per_measure,
                    BeatEvent.note_on)

class MetronomeIntervalGenerator(BaseIntervalGenerator):
    """Given a time signature, this will create a note on
    every beat."""
    def __init__(self, time_signature=fourfour, beat_length="quarter_note"):
        super().__init__(time_signature, beat_length)

    def __iter__(self):
        next_event = (0, BeatEvent.note_on)
        last_beat = 0
        while (True):
            yield next_event
            if next_event[1] == BeatEvent.note_on:
                last_beat = next_event[0]
                next_event = (last_beat + self.note_length, BeatEvent.note_off)
            else:
                next_event = (last_beat + self.time_signature.ticks_per_beat,
                    BeatEvent.note_on)




