"""Various volume envelopes."""

from . import SAMPLING_RATE
from .generators import SampleGenerator


class Envelope(SampleGenerator):
    """The Envelope base-class."""
    def __init__(self, source, sampling_rate=SAMPLING_RATE):
        SampleGenerator.__init__(self, sampling_rate)
        self._source = source.__iter__()
        # Has the envelope completed (i.e. will it be zero hereafter)
        self._finished = False

    def _get(self):
        # Returns early if finished, which is efficient but will no longer
        # be requesting any samples from _source.
        if self._finished: return 0.0
        return self._source.__next__() * self._get_multiplier()

    def _get_multiplier(self):
        raise Exception("Base Class needs to be subclassed")


class VolumeEnvelope(Envelope):
    def __init__(self, source, volume, sampling_rate=SAMPLING_RATE):
        Envelope.__init__(self, source, sampling_rate)
        self._volume = volume

    def _get_multiplier(self):
        return self._volume


class StandardEnvelope(Envelope):
    def __init__(self, source, attack=0.1, decay=0.1, peak=1, level=0.8,
                 sustain=1.0, release=0.5, sampling_rate=SAMPLING_RATE):
        Envelope.__init__(self, source, sampling_rate)
        self._peak = peak
        self._level = level
        # Store the time at which the events terminate
        # (i.e. attack, decay, sustain, release)
        self._attack = attack
        self._decay = decay + attack
        self._sustain = sustain + decay + attack
        self._release = release + sustain + decay + attack

    def _get_multiplier(self):
        if self._time < self._attack:
            return self._peak * self._time / self._attack
        elif self._time < self._decay:
            return self._peak - (self._peak - self._level) * (self._time - self._attack) / (self._decay - self._attack)
        elif self._time < self._sustain:
            return self._level
        elif self._time < self._release:
            return self._level * (1.0 - (self._time - self._sustain) / (self._release - self._sustain))
        self._finished = True
        return 0.0


