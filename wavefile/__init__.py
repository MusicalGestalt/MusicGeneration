
import array
import wave


MONO = 1
STEREO = 2
SAMPLING_16BIT = 2
SAMPLING_RATE = 44100


def scale_and_clip_data(d, scaling):
  v = int(d * scaling)
  if v >= scaling:
    return scaling - 1
  if v < -scaling:
    return -scaling
  return v


class WaveFile:
    """Class to facilitate simple WAV file output from float data.

      from math import sin, pi
      from wavefile import WaveFile, SAMPLING_RATE
      # Create a 1000Hz signal that lasts 5 seconds
      data = [sin(2*pi*x/SAMPLING_RATE*1000) for x in range(SAMPLING_RATE*5)]
      with WaveFile("test_1000Hz.wav") as wave_file:
        wave_file.writeData(data)
    """

    def __init__(self, filename):
        self._wavefile = wave.open(filename, 'wb')
        sample_width = SAMPLING_16BIT
        self._wavefile.setparams((MONO, sample_width, SAMPLING_RATE, 0, "NONE", "not compressed"))
        self._scaling = 2 ** ((sample_width * 8) - 1)
        assert self._scaling == 32768

    def writeData(self, data, correct_nframes=False):
        """Writes the given data to the wave file.

        data should be a list of floats in the range -1.0 .. 1.0
        Values outside this range will be clipped"""
        # Hard-coded to use signed-short data-type
        byte_data = array.array("h", [scale_and_clip_data(d, self._scaling) for d in data])
        self._wavefile.writeframesraw(byte_data.tostring())
        if correct_nframes:
            # Calling writeframes with no data will ensure the WAV header contains
            # the correct value for nframes.
            # Closing _wavefile will also correct nframes in the header, so this
            # correction is not necessary in general, just conservative, or if you want
            # to be able to play the WAV file while it's still being written to.
            self._wavefile.writeframes([])

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wavefile.close()


def test():
    # Not the best test, since it doesn't actually check the output
    # but if it doesn't crash, it probably created a WAV file in the
    # current directory.
    from math import sin, pi
    freq = 1000
    data = [sin(2*pi*x/SAMPLING_RATE*freq) for x in range(SAMPLING_RATE*5)]
    with WaveFile("test_%dHz.wav" % int(freq)) as wave_file:
      wave_file.writeData(data)


if __name__ == '__main__':
    test()
