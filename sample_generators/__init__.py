"""Various sample generator classes."""
import math


SAMPLING_RATE = 44100


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
        self._time = 0.0

    def __iter__(self):
        while True:
          yield self._get()
          self._time += self._sample_time

    def _get(self):
        raise Exception("Base Class needs to be subclassed")

    def get(self, num_samples):
        """Returns a list of floating point samples."""
        if num_samples == 0: return []
        assert num_samples > 0
        data = []
        for x in self:
          data.append(x)
          if len(data) == num_samples:
            return data



class SineGenerator(SampleGenerator):
    """A Sine-wave sample generator."""
    def __init__(self, freq, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._freq = freq
        self._freq_constant = 2 * math.pi * self._freq / self.sampling_rate

    def _get(self):
        yield math.sin(self._freq_constant * self.time)


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
