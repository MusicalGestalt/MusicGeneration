"""End-to-End Tests for MusicGeneration."""

import random
import unittest
from . import *
from MusicGeneration.rhythm import fourfour
from MusicGeneration.instruments import WaveInstrument
from MusicGeneration.sample_generators import SAMPLING_RATE, generators
from MusicGeneration.rhythm.interval_sequences import SimpleIntervalGenerator
from MusicGeneration.theory.tone_sequences import CyclicMelodyGenerator, RandomWalkMelodyGenerator
from MusicGeneration.theory import scales
from MusicGeneration.composers import SimpleComposer
from MusicGeneration.composers.clock import BasicClock
from MusicGeneration import wavefile


# class TimedWaveWriter:
#     def __init__(self, filename, instrument):
#         self._wf = wavefile.WaveFile(filename)
#         self._instrument = instrument
#         self._samples_written = 0

#     def write_data(self, sender, tick):
#         data = self._instrument.get(int(SAMPLING_RATE * ))
#         self._wf.writeData(data)
#         self._samples_written += len(data)


def get_random_notes_in_scale(root, scale_name, num_notes):
    # Ensures the test is deterministic
    random.seed(100)
    intervals = scales.get_scale_intervals(scale_name)
    note_list = scales.scale(root, intervals, num_notes=16)
    return [random.choice(note_list) for i in range(num_notes)]


class TestMusicGeneration(unittest.TestCase):

    def test_music1(self):
        time_signature = fourfour
        phrase = None
        bpm = 250
        measure_time = time_signature.seconds_per_measure(bpm)
        sine_instrument = WaveInstrument(bpm, phrase)

        interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.eighth_note)
        melody_generator = RandomWalkMelodyGenerator()
        composer = SimpleComposer(interval_generator, melody_generator)
        composer.add_phrase_observer(sine_instrument)

        cl = BasicClock("conductor")
        cl.add_tick_observer(composer)
        num_measures = 6
        wave_file = wavefile.WaveFile("demo_music1.wav")
        for loop in range(num_measures):
            cl.increment(time_signature.ticks_per_measure)
            data = sine_instrument.get(int(SAMPLING_RATE * measure_time))
            wave_file.writeData(data)

    def test_music2(self):
        """Two instruments playing repeating patterns of 5 and 7 notes respectively."""
        time_signature = fourfour
        bpm = 100

        # setup instruments
        sine_instrument1 = WaveInstrument(bpm, None)
        sine_instrument2 = WaveInstrument(bpm, None)
        # sine_instrument2 = WaveInstrument(bpm, None, wave_class=generators.SquareWaveGenerator)

        interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.eighth_note)
        melody_generator = CyclicMelodyGenerator(get_random_notes_in_scale(36, "minor_pentatonic", num_notes=5))
        composer1 = SimpleComposer(interval_generator, melody_generator, default_time_sig=time_signature)
        composer1.add_phrase_observer(sine_instrument1)

        interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.eighth_note)
        melody_generator = CyclicMelodyGenerator(get_random_notes_in_scale(60, "minor_pentatonic", num_notes=7))
        composer2 = SimpleComposer(interval_generator, melody_generator, default_time_sig=time_signature)
        composer2.add_phrase_observer(sine_instrument2)

        measure_time = time_signature.seconds_per_measure(bpm)
        delayed_instrument2 = generators.DelayedGenerator(sine_instrument2, measure_time / 16.0)
        mixer = generators.MixerGenerator([sine_instrument1, delayed_instrument2], scaling=0.3)

        cl = BasicClock("conductor")
        cl.add_tick_observer(composer1)
        cl.add_tick_observer(composer2)
        num_measures = 4
        wave_file = wavefile.WaveFile("demo_music2.wav")
        for loop in range(num_measures):
            cl.increment(time_signature.ticks_per_measure)
            data = mixer.get(int(SAMPLING_RATE * measure_time))
            wave_file.writeData(data)


def main():
    unittest.main()
