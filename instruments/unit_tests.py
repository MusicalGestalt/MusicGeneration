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
    for (i, tone) in enumerate(tone_list):
        if tone <= 0: continue
        note = Note(tone, i * time_signature.eighth_note, duration)
        note_list.append(note)
    return Phrase(note_list, time_signature)


# TODO: add tests for changing the phrases mid-way through playing
# i.e. using the EventReceiver/Phrase-Listener functionality.

class TestSineInstrument(unittest.TestCase):

    def test_sine_instrument(self):
        time_signature = rhythm.fourfour
        phrase = create_phrase([60, 0, 0, 0, 67], time_signature)
        # phrase = create_phrase([60, 0, 64, 0, 67, 0, 71, 0], time_signature)
        # phrase = create_phrase([60, 62, 64, 65, 67, 69, 71, 72], time_signature)
        bpm = 150
        num_loops = 2
        sine_instrument = WaveInstrument(bpm, phrase)
        end_time = phrase.phrase_endtime_in_seconds(bpm)
        data = sine_instrument.get(int(SAMPLING_RATE * end_time * num_loops))

        L = len(data)
        note_length = int(L / 8 / num_loops)
        for loop in range(num_loops):
            error_msg = "Failed on loop %d" % (loop+1)
            loop_data = data[int(loop*(L/num_loops)) : int((loop+1)*(L/num_loops)-1)]
            self.assertLess(min(loop_data[:note_length]), -0.75, msg=error_msg)
            self.assertGreater(max(loop_data[:note_length]), 0.75, msg=error_msg)
            self.assertLess(max(loop_data[note_length+1:4*note_length-1]), 0.01, msg=error_msg)
            self.assertGreater(min(loop_data[note_length+1:4*note_length-1]), -0.01, msg=error_msg)

        with wavefile.WaveFile("test_sine_instrument1.wav") as wave_file:
            wave_file.writeData(data)

    def test_sawtooth_instrument(self):
        time_signature = rhythm.fourfour
        phrase = create_phrase([60, 62, 64, 65, 67, 69, 71, 72], time_signature)
        bpm = 150
        num_loops = 2
        sawtooth_instrument = WaveInstrument(bpm, phrase, wave_class=generators.SawtoothWaveGenerator)
        end_time = phrase.phrase_endtime_in_seconds(bpm)
        data = sawtooth_instrument.get(int(SAMPLING_RATE * end_time * num_loops))

        note_length = int(len(data) / 8 / num_loops)
        for i in range(8 * num_loops):
            self.assertLess(min(data[i*note_length:(i+1)*note_length]), -0.75)
            self.assertGreater(max(data[i*note_length:(i+1)*note_length]), 0.75)

        with wavefile.WaveFile("test_sawtooth_instrument1.wav") as wave_file:
            wave_file.writeData(data)



def main():
    print("Running unit tests for 'instrument' module")
    unittest.main()

if __name__ == '__main__':
    main()
