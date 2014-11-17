"""Unit tests for instrument libraries."""

import unittest

from MusicGeneration.music import Phrase, Note
from MusicGeneration import rhythm
from MusicGeneration.sample_generators import SAMPLING_RATE, generators
from MusicGeneration import wavefile

from . import WaveInstrument


def create_phrase(tone_list, time_signature):
    duration = time_signature.eighth_note
    note_list = []
    for (i,tone) in enumerate(tone_list):
        if tone <= 0: continue
        note = Note(tone, i * time_signature.ticks_per_measure / 8, duration)
        note_list.append(note)
    return Phrase(note_list, time_signature)


class TestSineInstrument(unittest.TestCase):

    def test_sine_instrument(self):
        time_signature = rhythm.fourfour
        phrase = create_phrase([60, 0, 0, 0, 67], time_signature)
        # phrase = create_phrase([60, 0, 64, 0, 67, 0, 71, 0], time_signature)
        # phrase = create_phrase([60, 62, 64, 65, 67, 69, 71, 72], time_signature)
        bpm = 150
        sine_instrument = WaveInstrument(bpm, phrase)
        end_time = phrase.phrase_endtime_in_seconds(bpm)
        data = sine_instrument.get(int(SAMPLING_RATE*end_time))

        note_length = int(len(data) / 5)
        self.assertLess(min(data[:note_length]), -0.75)
        self.assertGreater(max(data[:note_length]), 0.75)
        self.assertLess(max(data[note_length+1:4*note_length-1]), 0.01)
        self.assertGreater(min(data[note_length+1:4*note_length-1]), -0.01)

        with wavefile.WaveFile("test_sine_instrument1.wav") as wave_file:
            wave_file.writeData(data)

    def test_sawtooth_instrument(self):
        time_signature = rhythm.fourfour
        phrase = create_phrase([60, 62, 64, 65, 67, 69, 71, 72], time_signature)
        bpm = 150
        sawtooth_instrument = WaveInstrument(bpm, phrase, wave_class=generators.SawtoothWaveGenerator)
        end_time = phrase.phrase_endtime_in_seconds(bpm)
        data = sawtooth_instrument.get(int(SAMPLING_RATE*end_time))

        note_length = int(len(data) / 8)
        for i in range(8):
          self.assertLess(min(data[i*note_length:(i+1)*note_length]), -0.75)
          self.assertGreater(max(data[i*note_length:(i+1)*note_length]), 0.75)

        with wavefile.WaveFile("test_sawtooth_instrument1.wav") as wave_file:
            wave_file.writeData(data)



def main():
    print("Running unit tests for 'instrument' module")
    unittest.main()

if __name__ == '__main__':
    main()
