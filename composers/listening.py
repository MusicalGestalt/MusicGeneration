"""Listening composers can "hear" other phrases and respond to them."""
from . import EventSender, EventReceiver, BaseComposer
import itertools

@EventReceiver("phrase", "listen")
class Listener(BaseComposer):
    def __init__(self, *sources, repeat_notifications=False):
        self.__sources = sources
        for s in sources:
            s.add_phrase_listener(self)
        self.__phrases = dict()
        self.__repeat = repeat_notifications

    def get_phrase(self, phrase_list=None):
        if phrase_list is None:
            phrase_list = self.__phrases.items()
        notes = itertools.chain(*[p.notes for p in phrase_list])
        return Phrase(notes, phrase_list[0].get_time_signature())

    def _get(self, phrase_list=None):
        next_phrase = self.get_phrase(phrase_list)
        self.send_phrase_event(next_phrase)

    def listen(self, sender, details):
        self.__phrases[sender] = details
        if self.__repeat:
            self._get()

