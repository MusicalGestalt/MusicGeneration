"""Various sample generator classes."""

import math
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
    def __init__(self, source_list=None, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        source_list = [] if source_list is None else source_list
        self._source_list = source_list

    def _get(self):
        return sum([source.__next__() for source in self._source_list])

    def add(self, source, start_time=None):
        if start_time:
            assert start_time > 0
            self._source_list.append(
                    DelayedGenerator(source, start_time, self._sampling_rate))
        else:
            self._source_list.append(source)

