"""Library for music composers."""

from MusicGeneration.music import Note, Phrase
from MusicGeneration.rhythm.interval_sequences import BaseIntervalGenerator
from MusicGeneration.theory.tone_sequences import MelodyGenerator
from MusicGeneration.rhythm import TimeSignature, fourfour
from .events import EventSender, EventReceiver


@EventSender("phrase")
@EventReceiver("tick", "next_tick")
class BaseComposer:
    """Base Composer class to generate musical phrases.

        Notes on implementation of sub-clases of BaseComposer
          (1) Override the _get() method to return Phrase objects
          (2) Since a Phrase object encodes a sequence of notes in
          absolute time, the Composer should return a PHRASE THAT
          STARTS AT TIME ZERO. It can then by shifted in time as needed
          by the caller.

    """
    def __init__(self):
        self._current_tick = 0

    def next_tick(self, sender, tick_id):
        if tick_id == self._current_tick:
            next_phrase = self._get()
            assert isinstance(next_phrase, Phrase)
            # Increment current tick by length of phrase (will be an integer multiple of a measure)
            self._current_tick += next_phrase.phrase_endtime()

            # TODO(oconaire): It would be nice to confirm that the phrase starts at time zero.
            # There's no perfect way to do this. Idea: check that the phrase length is <= K measures
            # and print a warning if not (a weak assumption). Idea 2: For long phrases, check that
            # there are some notes in the first measure.

            # Send next Phrase to listeners.
            self.send_phrase_event(next_phrase)
        else:
            # We should never skip the trigger tick
            # nor should we ever forgot to update the trigger tick
            # once it's been seen.
            assert tick_id < self._current_tick

    def _get(self):
        """Generate the next musical phrase."""
        raise Exception("Not implemented")


class SimpleComposer(BaseComposer):
    """A music composer that uses a single interval_generator, combined with
    a single melody_generator to create phrases.
    """
    def __init__(self, interval_generator, melody_generator, default_time_sig=fourfour, default_duration=None):
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
        self._default_duration = default_duration if default_duration else default_time_sig.eighth_note
        self._interval_buffer = []

    def _get(self):
        """Generate the next musical phrase, one measure long."""
        # Determine the key and time signature
        # TODO: Should Phrases store their 'key'? That would make it easier to improvise with them.
        time_sig = self._default_time_sig
        duration = self._default_duration
        past_max_tick = time_sig.ticks_per_measure

        # TODO(oconaire): This code could be simplified by subtracting the tick-shift at the end.

        # TODO(oconaire): It's not clear what should happen if we have a note that starts in
        # this measure, but goes on into the next measure. A hack would be to truncate the last note
        # in the phrase (which is what I do below)

        tick_list = []
        tick_list += self._interval_buffer
        self._interval_buffer = []
        while True:
            (tag, tick) = self._interval_generator.__next__()
            # Normalize time so that the phrase starts at zero
            corrected_tick = tick - self._current_tick
            if corrected_tick < past_max_tick:
                tick_list.append(corrected_tick)
            else:
                # Save the generated interval for the next phrase
                self._interval_buffer = [tick - self._current_tick - time_sig.ticks_per_measure]
                break

        note_list = []
        for tick in tick_list:
            tone = self._melody_generator.__next__()
            if (tick + duration) <= past_max_tick:
                note_list.append(Note(tone, tick, duration))
            else:
                # Truncate last note
                note_list.append(Note(tone, tick, past_max_tick - tick - 1))

        phrase = Phrase(note_list, time_sig)
        return phrase

