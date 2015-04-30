"""Various sample generator classes."""

import array
import math
import random
import wave
from . import SAMPLING_RATE


class SampleGenerator:
    """
    A SampleGenerator is an object that returns audio wave samples.
    Each sample is a floating point number in the range -1.0 ... +1.0
    It can be used as:
    (i) an iterator, useful for applying volume envelopes to wave data
    or
    (ii) a source of "whole wave" segements, via the get(num_samples) method.
    """
    def __init__(self, sampling_rate):
        self._sampling_rate = sampling_rate
        self._sample_time = 1.0 / sampling_rate
        # _time represents the time of the last sample generated
        self._time = -self._sample_time
        # Has the envelope completed (i.e. will it be zero hereafter)?
        # Mark as True when the generator is finished producing data
        # and will return 0.0 always.
        self._finished = False

    def __next__(self):
        self._time += self._sample_time
        return self._get()

    def __iter__(self):
        return self

    def _get(self):
        raise Exception("Base Class needs to be subclassed")

    def get(self, num_samples):
        """Returns a list of floating point samples."""
        if num_samples == 0: return []
        assert num_samples > 0
        return [self.__next__() for _ in range(num_samples)]

    def getTime(self):
        """Returns the time of the next sample."""
        return self._time + self._sample_time


class ConstantGenerator(SampleGenerator):
    """A Sine-wave sample generator."""
    def __init__(self, constant=1.0, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._constant = constant

    def _get(self):
        return self._constant


class SineWaveGenerator(SampleGenerator):
    """A Sine-wave sample generator."""
    def __init__(self, freq, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._freq = freq
        self._freq_constant = 2 * math.pi * self._freq

    def _get(self):
        return math.sin(self._freq_constant * self._time)


class SquareWaveGenerator(SampleGenerator):
    """A Square-wave sample generator."""
    def __init__(self, freq, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._freq = freq
        self._cycle_time = 1.0 / self._freq

    def _get(self):
        cycle_position = (self._time % self._cycle_time) / self._cycle_time
        return 1.0 if cycle_position < 0.5 else -1.0


class SawtoothWaveGenerator(SampleGenerator):
    """A Sawtooth-wave sample generator."""
    def __init__(self, freq, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._freq = freq
        self._cycle_time = 1.0 / self._freq

    def _get(self):
        cycle_position = (self._time % self._cycle_time) / self._cycle_time
        return (cycle_position * 2) - 1


class SweepWaveGenerator(SampleGenerator):
    """A Frequency-Sweep sample generator."""
    def __init__(self, freq1, freq2, interval, mode="linear", start_phase=0.0, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._freq1 = freq1
        self._freq2 = freq2
        self._interval = interval
        self._mode = mode
        self._b = math.log(self._freq2/self._freq1) / self._interval
        self._a = 2 * math.pi * self._freq1 / self._b
        self._a0 = -self._a + start_phase

    def _get(self):
        if self._mode == "linear":
            phase = 2 * math.pi * self._time * (self._freq1 + (self._freq2 - self._freq1) * self._time / self._interval / 2)
        elif self._mode == "exp":
            phase = self._a0 + self._a * math.exp(self._b * self._time)
        else:
            assert False
        return math.sin(phase)


class GuitarWaveGenerator(SampleGenerator):
    """A Guitar-string sample generator."""
    def __init__(self, freq, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._freq = freq
        self._setup_buffer()

    def _setup_buffer(self):
        self._bufsize = int(self._sampling_rate / self._freq)
        assert self._bufsize > 0
        # TODO(oconaire): We can also initialize this with a squarewave or sawtooth
        # wave to get a different guitar string sound.
        self._buffer = [random.uniform(-1.0, 1.0) for i in range(self._bufsize)]
        self._bufindex = 0;

    def _get(self):
        value = (self._buffer[self._bufindex] + self._buffer[(self._bufindex+1) % self._bufsize]) / 2.0;
        self._buffer[self._bufindex] = value;
        self._bufindex = (self._bufindex + 1) % self._bufsize;
        return value


class DelayedGenerator(SampleGenerator):
    """A delayed sample generator."""
    def __init__(self, source, start_time, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._source = source
        self._start_time = start_time

    def _get(self):
        if self._time < self._start_time:
            return 0.0
        return self._source.__next__()


class MixerGenerator(SampleGenerator):
    """A sample generator to combines other generators."""
    def __init__(self, source_list=None, scaling=1.0, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        source_list = [] if source_list is None else source_list
        self._source_list = source_list
        self._scaling = scaling
        if type(self._scaling) == list:
            assert len(scaling) == len(source_list)

    # TODO(oconaire): Include a MarkFinished() method in Generator, which will tell listeners
    # that it's being marked as finished. That way, the mixer can remove it.
    def _get(self):
        if not self._source_list: return 0.0
        if type(self._scaling) == list:
            return sum([volume * source.__next__() for (volume, source) in zip(self._scaling, self._source_list)])
        return self._scaling * sum([source.__next__() for source in self._source_list])

    def add(self, source, start_time=None):
        if start_time:
            assert start_time > 0
            self._source_list.append(
                    DelayedGenerator(source, start_time - self.getTime(), self._sampling_rate))
        else:
            self._source_list.append(source)


class WaveFileGenerator(SampleGenerator):
    """A sample generator made from a WAV file."""
    def __init__(self, filename, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._filename = filename
        self._wf = wave.open(self._filename, 'rb')
        (nchannels, sample_width, framerate, nframes, comptype, compname) = self._wf.getparams()
        assert framerate == self._sampling_rate
        assert nchannels in [1, 2]
        assert sample_width == 2
        self._stereo = (nchannels == 2)
        self._scaling = 2.0 ** ((sample_width * 8) - 1)
        self.reset()

    def reset(self):
        # TODO(oconaire): Instead of always reading from a WAV file, we might
        # just buffer the whole file in memory. Perhaps using a different class:
        # e.g. WaveSampleGenerator
        self._wf.rewind()
        self._nsamples = self._wf.getnframes()
        self._index = -1
        self._buffer = []
        self._finished = False

    def _get(self):
        if self._nsamples <= 0:
            self._finished = True
            return 0.0
        if self._index >= (len(self._buffer) - 1):
            # Read (at most) one second of data
            self._index = -1
            raw_data = array.array("h")
            raw_string = self._wf.readframes(self._sampling_rate)
            raw_data.frombytes(raw_string)
            raw_values = raw_data.tolist()
            if self._stereo:
                # Drop every second value, so that a mono signal is returned
                raw_values = [r for (i,r) in enumerate(raw_values) if (i%2)==0]
            self._buffer = [v / self._scaling for v in raw_values]

        self._nsamples -= 1
        self._index += 1
        return self._buffer[self._index]
