"""Listening composers can "hear" other phrases and respond to them."""
from . import EventSender, EventReceiver, BaseComposer
from MusicGeneration.music import Phrase
import itertools

# TODO: add unit tests for MixerListeningComposer

@EventReceiver("phrase", "listen")
class ListeningComposer(BaseComposer):
    """Base class for Composers that listen to other composers and
    generate Phrases using their input."""
    def __init__(self, *sources, repeat_notifications=False):
        self.__sources = sources
        for s in sources:
            s.add_phrase_listener(self)
        self.__phrases = dict()
        # Determines if a phrase event should be triggered every time
        # one of the input composers sends a new phrase.
        self.__repeat = repeat_notifications

    def listen(self, sender, phrase):
        assert isinstance(phrase, Phrase)
        self.__phrases[sender] = phrase
        if self.__repeat:
            self.send_phrase_event(self._get())


class MixerComposer(ListeningComposer):
    """A ListeningComposer that simply mixes the notes received from the
    input composers to generate output Phrases."""
    def __init__(self, *sources, repeat_notifications=False):
        ListeningComposer.__init__(self, *sources, repeat_notifications=repeat_notifications)

    def _get(self):
        phrase_list = self.__phrases.items()
        # Compile all note lists into one big list.
        notes = itertools.chain(*[p.notes for p in phrase_list])
        # Sort notes by start time.
        notes = sorted(notes, key = lambda note: note.start_tick)
        return Phrase(notes, phrase_list[0].get_time_signature())


