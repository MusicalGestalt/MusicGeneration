"""End-to-End Tests for MusicGeneration."""

import math
import platform
import random
import unittest

from . import *
from MusicGeneration.rhythm import fourfour
from MusicGeneration.instruments import WaveInstrument, DefaultDrumkitInstrument, PrinterInstrument
from MusicGeneration.sample_generators import SAMPLING_RATE, generators
# from MusicGeneration.sample_generators.envelopes import VolumeEnvelope
from MusicGeneration.rhythm.interval_sequences import SimpleIntervalGenerator, ParametricIntervalGenerator
from MusicGeneration.theory.tone_sequences import (CyclicMelodyGenerator, RandomWalkMelodyGenerator,
    ParametricMelodyGenerator)
from MusicGeneration.theory import scales
from MusicGeneration.composers import SimpleComposer 
from MusicGeneration.composers.clock import BasicClock
from MusicGeneration.composers.listening import MixerComposer, SwitchComposer, NoteDurationComposer
from MusicGeneration import wavefile
from MusicGeneration.composers.drum_composers import BasicDrumComposer
from MusicGeneration.composers.drum_composers import BASS, SNARE, TOM_BIG, TOM_SMALL, TOM_FLOOR
from MusicGeneration.composers.drum_composers import HIHAT_OPEN, HIHAT_CLOSED, CLICK, RIDE, CRASH
from MusicGeneration.theory.scales import (major_pentatonic, minor_pentatonic, natural_minor, octaves_for_note, minC, maxC, middleC)

# class TimedWaveWriter:
#     def __init__(self, filename, instrument):
#         self._wf = wavefile.WaveFile(filename)
#         self._instrument = instrument
#         self._samples_written = 0

#     def write_data(self, sender, tick):
#         data = self._instrument.get(int(SAMPLING_RATE * ))
#         self._wf.writeData(data)
#         self._samples_written += len(data)


def PlaySoundIfWindows(filename):
    """Plays a WAV file."""
    my_os = platform.system()
    if my_os == "Windows":
        import winsound
        winsound.PlaySound(filename, winsound.SND_FILENAME)
        # winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
    elif my_os == "Linux":
        pass
        # To implement, see:
        # http://stackoverflow.com/questions/307305/play-a-sound-with-python/311634#311634
        # from wave import open as waveOpen
        # from ossaudiodev import open as ossOpen
        # s = waveOpen('tada.wav','rb')
        # (nc,sw,fr,nf,comptype, compname) = s.getparams( )
        # dsp = ossOpen('/dev/dsp','w')
        # try:
        #   from ossaudiodev import AFMT_S16_NE
        # except ImportError:
        #   if byteorder == "little":
        #     AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
        #   else:
        #     AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
        # dsp.setparameters(AFMT_S16_NE, nc, fr)
        # data = s.readframes(nf)
        # s.close()
        # dsp.write(data)
        # dsp.close()


def get_random_notes_in_scale(root, scale_name, num_notes):
    # Ensures the test is deterministic
    random.seed(1024)
    intervals = scales.get_scale_intervals(scale_name)
    note_list = scales.scale(root, intervals, num_notes=16)
    # Sort notes to get an ascending set.
    return sorted([random.choice(note_list) for i in range(num_notes)])


# class TestBasic(unittest.TestCase):
#     def test_x(self):
#         time_signature = fourfour
#         phrase = None
#         bpm = 250
#         measure_time = time_signature.seconds_per_measure(bpm)
#         sine_instrument = WaveInstrument(bpm, phrase)

#         interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.eighth_note)
#         melody_generator = RandomWalkMelodyGenerator()
#         composer = SimpleComposer(interval_generator, melody_generator)
#         composer.add_phrase_observer(sine_instrument)

#         pp = composer._get()
#         print(pp.notes)
#         print(sine_instrument._next_phrase)

#         cl = BasicClock("conductor")
#         cl.add_tick_observer(composer)
#         cl.increment(time_signature.ticks_per_measure)
#         print(sine_instrument._next_phrase)
#         data = sine_instrument.get(1)
#         #data = sine_instrument.get(int(SAMPLING_RATE * measure_time))


class TestBassMusicGeneration(unittest.TestCase):
    def test_music1(self):
        freq1 = 4186.0
        freq2 = 27.0
        interval = 8.0
        mode = "linear"
        N_max = 8
        k_max = 5
        sfrac = 1.0 / 64.0
        filename = "bass_sweep_%d_%d_%s.wav" % (freq1, freq2, mode)
        wave_file = wavefile.WaveFile(filename)
        last_samp = 0.0
        last_phase = 0.0
        for k in range(0, k_max+1):
            kmult = int(2.0**k)
            t_len = interval / kmult
            for N in range(1, kmult*N_max+1):
                if (N % 2) == 0:
                    sampgen = generators.SweepWaveGenerator(freq1, freq2, t_len, mode, start_phase=last_phase)
                else:
                    sampgen = generators.SweepWaveGenerator(freq2, freq1, t_len, mode, start_phase=last_phase)
                data = sampgen.get(int(SAMPLING_RATE * t_len))
                # smooth the first 0.25 seconds
                # nn = int(SAMPLING_RATE * sfrac)
                # for i in range(nn):
                #     alpha = 1.0 * i / nn
                #     data[i] = alpha*data[i] + (1.0-alpha)*last_samp
                wave_file.writeData(data)
                last_samp = data[-1]
                last_phase = math.asin(last_samp)
                if data[-2] > data[-1]:
                    # descending
                    last_phase = math.pi - last_phase


class TestMusicGeneration():
#class TestMusicGeneration(unittest.TestCase):

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
            print("loop=", loop)
            cl.increment(time_signature.ticks_per_measure)
            data = sine_instrument.get(int(SAMPLING_RATE * measure_time))
            wave_file.writeData(data)

    def test_music2(self):
        """Two instruments playing repeating patterns of 8 and 7 notes respectively."""
        time_signature = fourfour
        bpm = 100

        # setup instruments
        sine_instrument1 = WaveInstrument(bpm, None)
        sine_instrument2 = WaveInstrument(bpm, None, wave_class=generators.GuitarWaveGenerator)

        # interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.eighth_note)
        # melody_generator = CyclicMelodyGenerator(get_random_notes_in_scale(48, "minor_pentatonic", num_notes=8))
        interval_generator = ParametricIntervalGenerator(resolution=2, density=0.5, bias=-0.5, swing=0.25)
        melody_generator = ParametricMelodyGenerator(key=48, length=8, scale=scales.minor_pentatonic, num_unique_notes=8,
                                                     min_note=48, max_note=72, ascend_fraction=1.0)
        composer1 = SimpleComposer(interval_generator, melody_generator, default_time_sig=time_signature)
        composer1.add_phrase_observer(sine_instrument1)

        interval_generator = SimpleIntervalGenerator(num_ticks=time_signature.eighth_note)
        melody_generator = CyclicMelodyGenerator(get_random_notes_in_scale(48, "natural_minor", num_notes=7))
        composer2 = SimpleComposer(interval_generator, melody_generator, default_time_sig=time_signature, default_duration=time_signature.quarter_note)
        composer2.add_phrase_observer(sine_instrument2)

        measure_time = time_signature.seconds_per_measure(bpm)
        delayed_instrument2 = generators.DelayedGenerator(sine_instrument2, measure_time * 4)
        mixer = generators.MixerGenerator([sine_instrument1, delayed_instrument2], scaling=0.3)

        cl = BasicClock("conductor")
        cl.add_tick_observer(composer1)
        cl.add_tick_observer(composer2)
        num_measures = 16
        wave_file = wavefile.WaveFile("demo_music2.wav")
        for loop in range(num_measures):
            print(loop)
            cl.increment(time_signature.ticks_per_measure)
            data = mixer.get(int(SAMPLING_RATE * measure_time))
            wave_file.writeData(data)

#===============================================

# ParametricMelodyGenerator(key, length, scale=major_pentatonic, num_unique_notes=None,
#                  min_note=minC, max_note=maxC, ascend_fraction=None, attempts=100)

# ParametricIntervalGenerator(density, bias=None, swing=None, resolution=4, time_signature=fourfour, tag="Parametric")

# BasicDrumComposer(interval_generator, drum_type, drum_type_mapping=None, time_signature=fourfour)

# SimpleComposer(interval_generator, melody_generator, default_time_sig=fourfour, default_duration=None)

# MixerComposer(*sources, repeat_notifications=False)

# WaveInstrument(bpm, phrase=None, sampling_rate=SAMPLING_RATE, wave_class=generators.SineWaveGenerator)

# TriggerPadInstrument(note_mapping, bpm, phrase=None, sampling_rate=SAMPLING_RATE)

# SwitchComposer(*sources, repeat_notifications=False)

class TestSongGeneration():
# class TestSongGeneration(unittest.TestCase):

    def test_song1(self):
        """
        For n : 1...num_song_sections
         Make drums
         - For each drum type (bass, hi-hat, snare, toms)
           - use BasicDrumComposer with a ParametricIntervalGenerator
         - Combine drums using MixerComposer
         - Save section (composer)
         Make melody
         - Use ParametricMelodyGenerator + ParametricIntervalGenerator
         - Put into SimpleComposer
         - Save section (composer)

        Add drum sections to a switch composer (to be written?)
        Add melody sections to a switch composer (to be written?)

        - Output to drum instrument: ????
        - Output to sine instrument: ????
        """

        random.seed()

        # Clock setup
        cl = BasicClock("conductor")

        drum_class = [
            [BASS],
            [SNARE, TOM_SMALL, TOM_BIG, TOM_FLOOR],
            [HIHAT_CLOSED], # HIHAT_OPEN
            [RIDE, CLICK] # CRASH
        ]

        drum_composers = {}
        melody_composers = {}

        # global params
        num_song_sections = 1
        bpm = 60
        time_signature = fourfour
        key = middleC
        # section_pattern = "AAAABBBBAAAABBBBCCCCCCCCAAAA"
        section_pattern = "AAAA"

        for song_section in range(num_song_sections):
          # High level parameter selection
          drum_density = 0.1 + 0.9*(math.sqrt(10*random.random())/10)
          drum_bias = 1.0 - (2 * random.random())
          drum_swing  = random.random()
          melody_density = 0.1 + (0.9*random.random())
          melody_bias = 1.0 - (2 * random.random())
          melody_swing  = random.random()

          # Make Drums
          composer_list = []
          for drum_types in drum_class[:6]:
            drum_type = random.choice(drum_types)
            print("Preparing section[%d], drum type %d" % (song_section, drum_type))
            drum_swing2 = 0.0 if drum_type == BASS else drum_swing
            interval_generator = ParametricIntervalGenerator(drum_density, bias=drum_bias, swing=drum_swing2)
            num_beats = sum(interval_generator._pattern)
            print("  %d beats" % num_beats)
            composer_list.append(BasicDrumComposer(interval_generator, drum_type))
            cl.add_tick_observer(composer_list[-1])
          # drum_composers[song_section] = composer_list[-1]
          drum_composers[song_section] = MixerComposer(*composer_list)

          # Make Melody
          num_notes = max([1, round(melody_density * 16)])
          melody_density = num_notes / 16.0
          print("Preparing section[%d], melody of %d notes" % (song_section, num_notes))
          interval_generator = ParametricIntervalGenerator(melody_density, bias=melody_bias, swing=melody_swing)
          print(num_notes, sum(interval_generator._pattern))
          assert num_notes == sum(interval_generator._pattern)
          melody_generator = ParametricMelodyGenerator(key, length=num_notes, scale=major_pentatonic, num_unique_notes=(int(num_notes/2)+1),
                  min_note=middleC-12, max_note=middleC+12, ascend_fraction=1.0, attempts=100)
          simple_composer = SimpleComposer(interval_generator, melody_generator, default_time_sig=time_signature, default_duration=None)
          cl.add_tick_observer(simple_composer)
          melody_composers[song_section] = NoteDurationComposer(simple_composer,
            min_length=time_signature.eighth_note, max_length=int(time_signature.quarter_note))

        # Musicians
        for (did, composer) in drum_composers.items():
            print("DrumComposer:", did, composer)
        for (mid, composer) in melody_composers.items():
            print("SimpleComposer:", mid, composer)
        for obs in cl.get_tick_observers():
            print("Observer:", obs)
        drum_musician = SwitchComposer(*[d for d in drum_composers.values()])
        melody_musician = SwitchComposer(*[m for m in melody_composers.values()])

        # Setup to instruments
        drumkit = DefaultDrumkitInstrument(bpm, phrase=None, sampling_rate=SAMPLING_RATE)
        piano = WaveInstrument(bpm, phrase=None, sampling_rate=SAMPLING_RATE, wave_class=generators.SineWaveGenerator)
        mixer = generators.MixerGenerator([drumkit, piano], scaling=[0.3, 0.3])
        # mixer = generators.MixerGenerator([drumkit], scaling=0.3)

        # Assign to instruments
        drum_musician.add_phrase_observer(drumkit)
        melody_musician.add_phrase_observer(piano)

        pr1 = PrinterInstrument("melody")
        melody_musician.add_phrase_observer(pr1)
        pr2 = PrinterInstrument("drums")
        drum_musician.add_phrase_observer(pr2)

        # drum_musician.switch(0)
        # melody_musician.switch(0)
        # cl.increment(time_signature.ticks_per_measure)
        # print("piano:", piano._current_phrase)
        # data = mixer.get(1)


        # for composer in drum_composers.values():
        #     cl.add_tick_observer(composer)
        # for composer in melody_composers.values():
        #     cl.add_tick_observer(composer)
        # num_measures = 16

        measure_time = time_signature.seconds_per_measure(bpm)


        use_hack = True

        if use_hack:
            # Fast hack to get data chunks
            section_wave_data = {}
            for p in range(num_song_sections):
                drum_musician.switch(p)
                melody_musician.switch(p)
                cl.increment(time_signature.ticks_per_measure)
                section_wave_data[p] = mixer.get(int(SAMPLING_RATE * measure_time))

        filename = "song_music1.wav"
        wave_file = wavefile.WaveFile(filename)
        for loop in range(len(section_pattern)):
            print("="*64)
            print("="*30,loop,"="*30)
            print("="*64)
            p = ord(section_pattern[loop]) - ord('A')

            if use_hack:
                data = section_wave_data[p]
            else:
                drum_musician.switch(p)
                melody_musician.switch(p)
                cl.increment(time_signature.ticks_per_measure)
                data = mixer.get(int(SAMPLING_RATE * measure_time))
            wave_file.writeData(data)
        wave_file.close()
        PlaySoundIfWindows(filename)


        # Play and mix N bars


        # Switch to another song section


    #===============================================


def main():
    unittest.main()
