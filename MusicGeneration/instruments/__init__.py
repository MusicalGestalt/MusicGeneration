"""Instrument Library: Classes that produce wave data from musical Phrases."""

import os
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


@EventReceiver("phrase", "print_phrase")
class PrinterInstrument(Instrument):
    """Instruments that just prints the phrases it gets."""
    def __init__(self, name):
        Instrument.__init__(self, bpm=0)
        self._name = name
    
    def print_phrase(self, sender, phrase):
        print("[%s] received phrases from %s" % (self._name, str(sender)))
        for note in phrase.notes:
            print("  %d-->%d" % (note.start_tick, note.tone))


class GeneratorInstrument(Instrument):
    """Base class for Instruments whose notes produce independent generators."""
    def __init__(self, bpm, phrase=None, sampling_rate=SAMPLING_RATE):
        Instrument.__init__(self, bpm, phrase, sampling_rate)
        self._source = None

    def _add_phrase_to_mix(self, phrase):
        assert phrase
        if not self._source:
            self._source = generators.MixerGenerator()
        play_time = self._source.getTime()
        self._update_time = play_time + phrase.phrase_endtime_in_seconds(self._bpm)
        print("Adding notes, time=%g, update_time=%g" % (play_time, self._update_time))
        convert_tick_to_seconds = lambda _tick: phrase.get_time_signature().convert_tick_to_seconds(_tick, self._bpm)
        for note in self._current_phrase.notes:
            generator = self._get_generator(note, convert_tick_to_seconds)
            if not generator: continue
            start_time = convert_tick_to_seconds(note.start_tick)
            self._source.add(generator, start_time=(play_time + start_time))

        # TODO: Think about this some more: By looping on an integer number of samples, we might have
        # drift between this and a source that kept full float precision. It will only be off by <1 sample for
        # each phrase, which is pretty small, but we could add back that sample every Nth round.
        self._remaining_samples = int(convert_tick_to_seconds(self._current_phrase.phrase_endtime()) * self._sampling_rate)

    def _get_generator(self, note, tick_to_seconds):
        raise Exception("Not implemented.")

    def _get(self):
        if self._current_phrase is None:
            self._current_phrase = self._next_phrase
            self._next_phrase = None

        if not self._source:
            self._add_phrase_to_mix(self._current_phrase)

        play_time = self._source.getTime()
        if play_time >= self._update_time:
            if self._next_phrase:
                self._current_phrase = self._next_phrase
                self._next_phrase = None
            self._add_phrase_to_mix(self._current_phrase)
        return self._source.__next__()




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


class WaveInstrument(GeneratorInstrument):
    def __init__(self, bpm, phrase=None, sampling_rate=SAMPLING_RATE, wave_class=generators.SineWaveGenerator):
        GeneratorInstrument.__init__(self, bpm, phrase, sampling_rate)
        self._wave_class = wave_class

    def _get_generator(self, note, tick_to_seconds):
        freq = ToneToFrequency(note.tone)
        duration = tick_to_seconds(note.duration)
        # TODO(ciaran): Handle note volume (could simply enclose in a volume envelope)
        return get_synth_note_generator(self._wave_class, freq, duration, self._sampling_rate)


class TriggerPadInstrument(GeneratorInstrument):
    """Trigger Pad where each note triggers a WAV file to play."""
    def __init__(self, note_mapping, bpm, phrase=None, sampling_rate=SAMPLING_RATE):
        GeneratorInstrument.__init__(self, bpm, phrase, sampling_rate)
        # dictionary mapping a note number to a WAV filename
        assert type(note_mapping) == dict        
        self._note_mapping = note_mapping

    def _get_generator(self, note, tick_to_seconds):
        # TODO(ciaran): Handle note volume (could simply enclose in a volume envelope)
        note_num = note.tone
        if note_num not in self._note_mapping:
            return None
        return generators.WaveFileGenerator(self._note_mapping[note_num], self._sampling_rate)


class DefaultDrumkitInstrument(TriggerPadInstrument):
  """Drumkit Trigger Pad where each note triggers a WAV file to play."""
  def __init__(self, bpm, phrase=None, sampling_rate=SAMPLING_RATE):
    note_mapping = {}
    for (index, note_num) in enumerate(range(0, 42)):
        note_mapping[note_num] = os.path.join("MusicGeneration", "wav_data", "drums", "DR1-%d.WAV" % index)
    TriggerPadInstrument.__init__(self, note_mapping, bpm, phrase=phrase, sampling_rate=sampling_rate)

