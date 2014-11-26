"""Library for music composers."""

from MusicGeneration.music import Note, Phrase
from MusicGeneration.rhythm.interval_sequences import BaseIntervalGenerator
from MusicGeneration.theory.tone_sequences import MelodyGenerator
from MusicGeneration.rhythm import TimeSignature, fourfour
from .events import EventSender, EventReceiver
@EventSender("phrase")
class BaseComposer:
    def __init__(self):
        self._current_tick = 0
        self._phrase_id = 0


    def get_phrase(self, phrase_list=None):
        if phrase_list:
            for phrase in phrase_list:
                assert isinstance(phrase, Phrase)
                # TODO: check each phrase is only one measure long (at most)
        next_phrase = self._get()
        # The output phrase should be one measure long
        # TODO: confirm this is true
        # (Is this assumption too strict?)
        # Yes, this assumption is too strict. We should expect a phrase
        # to be a MULTIPLE of one measure long.
        self._current_tick += next_phrase.get_time_signature().ticks_per_measure
        self._phrase_id += 1
        assert isinstance(next_phrase, Phrase)
        return next_phrase

    def _get(self, phrase_list=None):
        """Generate the next musical phrase."""
        raise Exception("Not implemented")

#
# Notes on implementation of sub-clases of BaseComposer
#   Since a Phrase object encodes a sequence of notes in
#   absolute time, the phrase returned by a Composer should
#   start at time zero. It can then by shifted in time as needed
#   by the caller.
#

class SimpleComposer(BaseComposer):
    """A music composer 
    """
    def __init__(self, interval_generator, melody_generator, default_time_sig=fourfour):
        BaseComposer.__init__(self)
        # I don't think we want these asserts- let's rely on duck typing
        # instead
        # I say this because CompositeIntervalGenerator doesn't inherit
        # from BIG. We could push the the inheritance hierarchy around
        # but I feel like that just makes things messy.
        assert isinstance(interval_generator, BaseIntervalGenerator)
        assert isinstance(melody_generator, MelodyGenerator)
        self._interval_generator = interval_generator
        self._melody_generator = melody_generator
        self._default_time_sig = default_time_sig
        self._interval_buffer = []

    def _get(self, phrase_list=None):
        """Generate the next musical phrase."""
        # Determine the key and time signature
        # TODO: Should Phrases store their 'key'? That would make it easier to improvise with them.
        # key = self._melody_generator.key if not phrase_list else phrase_list[0].get_time_signature()
        time_sig = self._default_time_sig if not phrase_list else phrase_list[0].get_time_signature()
        # Hard-code duration
        duration = time_sig.eighth_note
        max_tick = time_sig.ticks_per_measure - 1

        # TODO: if we want to have the ability to improvise music using the input
        # phrase_list, perhaps we need to be able to tell the melody generators
        # to shift key. ALTERNATIVELY (and more simply), we can just shift the melody
        # to match the target key!

        tick_list = []
        tick_list += self._interval_buffer
        self._interval_buffer = []
        print(tick_list)
        while True:
            (tag, tick) = self._interval_generator.__next__()
            # Normalize time so that the phrase starts at zero
            corrected_tick = tick - self._current_tick
            print(max_tick, tag, corrected_tick)
            if corrected_tick <= max_tick:
                tick_list.append(corrected_tick)
            else:
                # Save the generated interval for the next phrase
                self._interval_buffer = [tick - self._current_tick - time_sig.ticks_per_measure]
                break

        note_list = []
        for tick in tick_list:
            tone = self._melody_generator.__next__()
            note_list.append(Note(tone, tick, duration))        

        phrase = Phrase(note_list, time_sig)
        return phrase

