
class Note:
    """A note, which combines a pitch/tone, a start time, a duration, and a volume."""
    def __init__(self, tone, start_tick, duration, volume=1.0):
        self.tone = tone
        self.start_tick = start_tick
        self.duration = duration
        self.volume = volume

    def tone():
        doc = "The tone being played, represented as semitones above C-1."
        def fget(self):
            return self._tone
        def fset(self, value):
            self._tone = value
        def fdel(self):
            del self._tone
        return locals()
    tone = property(**tone())

    def start_tick():
        doc = "Which tick of the phrase on which the note should be voiced."
        def fget(self):
            return self._start_tick
        def fset(self, value):
            self._start_tick = value
        def fdel(self):
            del self._start_tick
        return locals()
    start_tick = property(**start_tick())

    def duration():
        doc = "How long, in ticks, this note should be voiced."
        def fget(self):
            return self._duration
        def fset(self, value):
            self._duration = value
        def fdel(self):
            del self._duration
        return locals()
    duration = property(**duration())

    def volume():
        doc = "The volume of the note, between 0.0 (silent) and 1.0."
        def fget(self):
            return self._volume
        def fset(self, value):
            self._volume = value
        def fdel(self):
            del self._volume
        return locals()
    volume = property(**volume())


class Phrase:
    def __init__(self, notes, time_signature):
        self.__notes = notes
        self.__time_signature = time_signature

    @property
    def notes(self):
        return self.__notes

    @property
    def time_signature(self):
        return self.__time_signature

    def phrase_endtime(self):
        """On what tick does this phrase end."""
        return max(map(self.notes, lambda n: n.start_tick + n.duration))














