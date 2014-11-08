"""Various objects to help with calculating rhythms."""

class TimeSignature:
    def __init__(self, beats_per_measure=4, one_beat_note=4, granularity=32):
        """
        Time signatures are usually represented as something like 4/4
        The numerator is the number of beats per measure.
        The denominator is the type of note that represents one beat.
        So 4/4 time is 4-beats per measure, and a 1/4 note gets one beat.

        Granualarity is how many subdivisions we can put in a single beat.
        """
        self.__beats_per_measure = beats_per_measure
        
        ticks_per_beat = beats_per_measure * granularity / one_beat_note
        self.__ticks_per_measure = beats_per_measure * granularity
        self.__quarter_note = (4 / one_beat_note) * ticks_per_beat
        self.__eighth_note = self.__quarter_note // 2
        self.__sixteenth_note = self.__eighth_note // 2
        self.__thirtysecond_note = self.__sixteenth_note // 2
        self.__half_note = self.__quarter_note * 2
        self.__whole_note = self.__half_note * 2
        self.__eighth_note_triplet = self.__quarter_note // 3
        self.__sixteenth_note_triplet = self.__eighth_note // 3

    @property
    def quarter_note(self): return self.__quarter_note

    @property
    def eight_note(self): return self.__eighth_note

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




