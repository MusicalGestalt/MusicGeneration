"""End-to-End Tests for MusicGeneration."""
import unittest
from . import *
from MusicGeneration.rhythm import fourfour
from MusicGeneration.instruments import WaveInstrument
from MusicGeneration.sample_generators import SAMPLING_RATE, generators
from MusicGeneration.rhythm.interval_sequences import SimpleIntervalGenerator
from MusicGeneration.theory.tone_sequences import CyclicMelodyGenerator
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


class TestMusicGeneration(unittest.TestCase):

    def test_music1(self):
        time_signature = fourfour
        phrase = None
        bpm = 250
        measure_time = time_signature.seconds_per_measure(bpm)
        sine_instrument = WaveInstrument(bpm, phrase)

        interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.ticks_per_beat)
        melody_generator = CyclicMelodyGenerator([60, 63, 65])
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


def main():
    unittest.main()