"""Instrument Library: Classes that produce wave data from musical Phrases."""

from MusicGeneration.composers.events import EventReceiver
from MusicGeneration.rhythm import TimeSignature
from MusicGeneration.music import Phrase
from MusicGeneration.sample_generators import generators, envelopes, SAMPLING_RATE
from MusicGeneration.theory.utils import ToneToFrequency


@EventReceiver("phrase", "set_next_phrase")
class Instrument(generators.SampleGenerator):
    def __init__(self, bpm, phrase=None, sampling_rate=SAMPLING_RATE):
        generators.SampleGenerator.__init__(self, sampling_rate)
        self._current_phrase = phrase
        self._next_phrase = None
        self._bpm = bpm

    def _get(self):
        raise Exception("Not implemented.")

    def set_next_phrase(self, sender, phrase):
      """After the current phrase has played, this phrase will be played."""
      self._next_phrase = phrase


def get_synth_note_generator(wave_class, freq, duration, sampling_rate):
    synth_note = wave_class(freq, sampling_rate)
    print("Make note: freq=%g, duration=%g" % (freq, duration))
    if duration >= 1.0:
        enveloped_note = envelopes.StandardEnvelope(synth_note, attack=0.05, decay=0.0, peak=1,
                                                    level=1, sustain=duration-0.95, release=0.9)
    else:
        enveloped_note = envelopes.StandardEnvelope(synth_note, attack=0, decay=0, peak=1,
                                                    level=1, sustain=duration/2, release=duration/2)
    return enveloped_note


class WaveInstrument(Instrument):
    def __init__(self, bpm, phrase=None, sampling_rate=SAMPLING_RATE, wave_class=generators.SineWaveGenerator):
        Instrument.__init__(self, bpm, phrase, sampling_rate)
        self._wave_class = wave_class
        self._setup_sample_source()

    def _setup_sample_source(self):
        self._source = generators.MixerGenerator()
        self._remaining_samples = 0
        if not self._current_phrase: return
        convert_tick_to_seconds = lambda _tick: self._current_phrase.get_time_signature().convert_tick_to_seconds(_tick, self._bpm)
        for note in self._current_phrase.notes:
            # TODO(ciaran): Handle note volume.
            freq = ToneToFrequency(note.tone)
            start_time = convert_tick_to_seconds(note.start_tick)
            duration = convert_tick_to_seconds(note.duration)
            self._source.add(get_synth_note_generator(self._wave_class, freq, duration, self._sampling_rate),
                             start_time=start_time)
        # TODO: Think about this some more: By looping on an integer number of samples, we might have
        # drift between this and a source that kept full float precision.
        self._remaining_samples = int(convert_tick_to_seconds(self._current_phrase.phrase_endtime()) * self._sampling_rate)

    def _get(self):
        if self._remaining_samples <= 0:
            if self._next_phrase:
                self._current_phrase = self._next_phrase
                self._next_phrase = None
            self._setup_sample_source()

        self._remaining_samples -= 1
        return self._source.__next__()



