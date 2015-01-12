"""Various objects to help with calculating rhythms."""
from enum import Enum #Enums ARE one P3.4 feature that you might not have.
    #they've been backported, so you should be able to install enum from PIP

class TimeSignature:
    """
    Time signatures are usually represented as something like 4/4
    The numerator is the number of beats per measure.
    The denominator is the type of note that represents one beat.
    So 4/4 time is 4-beats per measure, and a 1/4 note gets one beat.

    """
    def __init__(self, beats_per_measure=4, one_beat_note=4, granularity=32):
        """
        Beats per measure is the numerator.
        One beat note is which note gets one beat, used as a 
        denominator in a few division operations to figure out
        how long various kinds of notes are.

        Granualarity is how many subdivisions we can put in a single beat- 
        it's the number of ticks.

        Each property of the time signature then, tells us how many ticks long a 
        specific note is. For example, in 4/4 time, at 32 ticks-per-beat,
        a quarter note is 32 ticks long, while an eight note is 16 ticks long.
        """
        self.__beats_per_measure = beats_per_measure
        
        ticks_per_beat = granularity
        self.__ticks_per_measure = beats_per_measure * granularity
        self.__quarter_note = (one_beat_note / 4) * ticks_per_beat
        self.__eighth_note = self.__quarter_note // 2
        self.__sixteenth_note = self.__eighth_note // 2
        self.__thirtysecond_note = self.__sixteenth_note // 2
        self.__half_note = self.__quarter_note * 2
        self.__whole_note = self.__ticks_per_measure # a whole note is always 1 measure long!
        # TODO(remy): if we add an assert here to check that
        #   assert self.__whole_note == 2 * self.__half_note
        # It will fail if beats_per_measure != one_beat_note
        # e.g. 7/8, 3/4 time
        # Why does a whole note always need to be one measure long?
        # Why not define it as = 2 * self.__half_note ?
        self.__eighth_note_triplet = self.__quarter_note // 3
        self.__sixteenth_note_triplet = self.__eighth_note // 3
        self.__ticks_per_beat = ticks_per_beat

    @property
    def quarter_note(self): return self.__quarter_note

    @property
    def eighth_note(self): return self.__eighth_note

    @property
    def sixteenth_note(self): return self.__sixteenth_note

    @property
    def thirtysecond_note(self): return self.__thirtysecond_note

    @property
    def half_note(self): return self.__half_note

    @property
    def whole_note(self): return self.__whole_note

    @property
    def eighth_note_triplet(self): return self.__eighth_note_triplet

    @property
    def sixteenth_note_triplet(self): return self.__sixteenth_note_triplet

    @property
    def beats_per_measure(self): return self.__beats_per_measure

    @property
    def ticks_per_measure(self): return self.__ticks_per_measure

    @property
    def ticks_per_beat(self): return self.__ticks_per_beat

    def convert_tick_to_seconds(self, tick, beats_per_minute):
        return convert_tick_to_seconds(tick, self, beats_per_minute)

    def seconds_per_measure(self, beats_per_minute):
        return convert_tick_to_seconds(self.ticks_per_measure, self, beats_per_minute)


fourfour = TimeSignature()
twofour = TimeSignature(2)
threefour = TimeSignature(3)
sixeight = TimeSignature(6,8)


def convert_tick_to_seconds(tick, time_signature, beats_per_minute):
    seconds_per_beat = 60.0 / beats_per_minute

    beats_per_measure = time_signature.beats_per_measure
    ticks_per_measure = time_signature.ticks_per_measure

    beats_per_tick = beats_per_measure / ticks_per_measure
    return tick * beats_per_tick * seconds_per_beat

