"""These classes form a starting point for simple beat generators."""

from .. import (fourfour, TimeSignature, BeatEvent)

class DownbeatIntervalGenerator:
    """Given a time signature, this will create
    beat pattern of a down-beat at the top of the
    measure."""
    def __init__(self, time_signature=fourfour):
        self.time_signature = time_signature

    def __iter__(self):
        next_event = (0, BeatEvent.note_on)
        last_downbeat = 0
        while (True):
            yield next_event
            if next_event[1] == BeatEvent.note_on: #we just emitted a down beat
                last_downbeat = next_event[0]
                next_event = (next_event[0] + self.time_signature.quarter_note,
                    BeatEvent.note_off) #so the next thing we emit 
                                        #is an end to the note
            else:
                next_event = (last_downbeat + self.time_signature.ticks_per_measure,
                    BeatEvent.note_on)


