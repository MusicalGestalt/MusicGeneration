"""Listening composers can "hear" other phrases and respond to them."""
from . import EventSender, EventReceiver, BaseComposer
from MusicGeneration.music import Phrase
import copy
import itertools

# TODO: add unit tests for MixerListeningComposer

@EventReceiver("phrase", "listen")
class ListeningComposer(BaseComposer):
    """Base class for Composers that listen to other composers and
    generate Phrases using their input."""
    def __init__(self, *sources, repeat_notifications=False):
        BaseComposer.__init__(self)
        self._sources = sources
        for s in sources:
            s.add_phrase_observer(self)
        print("Listening to %d sources" % len(sources))
        self._phrases = dict()
        # Determines if a phrase event should be triggered every time
        # one of the input composers sends a new phrase.
        # NB: Ideally this should be TRUE, since if not, then it needs
        # to listen to a clock so that it knowns when to send the updates.
        # However, then the order of the updates is important, since it might
        # send an update before one of its sources does.
        # TL;DR This architecture with push notifications is problematic!!
        self.__repeat = repeat_notifications

    def listen(self, sender, phrase):
        assert isinstance(phrase, Phrase)
        self._phrases[sender] = phrase
        if self.__repeat:
            self.send_phrase_event(self._get())


class NoteDurationComposer(ListeningComposer):
    """A ListeningComposer that changes the durations of input notes."""
    def __init__(self, *sources, min_length=0, max_length=256, repeat_notifications=True):
        ListeningComposer.__init__(self, *sources, repeat_notifications=repeat_notifications)
        self._min_length = min_length
        self._max_length = max_length

    def ModifyPhraseDurations(self, phrase):
        notes = [copy.deepcopy(n) for n in phrase.notes]
        for i in range(0, len(notes)-1):
            dif = notes[i+1].start_tick - notes[i].start_tick
            if dif > self._min_length:
                notes[i].duration = min([self._max_length, dif])
            else:
                notes[i].duration = self._min_length
        return Phrase(notes, phrase.get_time_signature())

    def _get(self):
        # Should only listen to one composer
        assert len(self._phrases) == 1
        phrase = [p for p in self._phrases.values()][0]
        return self.ModifyPhraseDurations(phrase)


class MixerComposer(ListeningComposer):
    """A ListeningComposer that simply mixes the notes received from the
    input composers to generate output Phrases."""
    def __init__(self, *sources, repeat_notifications=True):
        ListeningComposer.__init__(self, *sources, repeat_notifications=repeat_notifications)

    def _get(self):
        phrase_list = [phrase for phrase in self._phrases.values()]
        # Compile all note lists into one big list.
        notes = itertools.chain(*[p.notes for p in phrase_list])
        # Sort notes by start time.
        notes = sorted(notes, key = lambda note: note.start_tick)
        return Phrase(notes, phrase_list[0].get_time_signature())


class SwitchComposer(ListeningComposer):
    """A ListeningComposer that simply outputs Phrases from
    one of its sources, and can switch between them."""
    def __init__(self, *sources):
        ListeningComposer.__init__(self, *sources, repeat_notifications=True)
        self._source_index = 0

    def switch(self, source_index):
        self._source_index = source_index

    def _get(self):
        if (self._source_index < 0):
            print("too low!:", self._source_index, len(self._sources))
        if (self._source_index >= len(self._sources)):
            print("too high!:", self._source_index, len(self._sources))
        source_to_output = self._sources[self._source_index]
        # If we haven't yet got a phrase from our selected source, then
        # simply output another phrase from some source
        if source_to_output not in self._phrases:
            valid_sources = [s for s in self._sources if s in self._phrases]
            # we need at least one valid phrase
            assert valid_sources
            source_to_output = valid_sources[0]
            print("defaulting to ", source_to_output, " since ", self._sources[self._source_index], " not available")
        return self._phrases[source_to_output]


