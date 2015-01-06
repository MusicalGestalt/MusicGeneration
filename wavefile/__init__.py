import array
import wave
from pyaudio import PyAudio
from collections import namedtuple
import threading, time

WaveParams = namedtuple("WaveParams", "nchannels sampwidth framerate nframes comptype compname")

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

class PlayThread(threading.Thread):
    def __init__(self, stream, name="PlayThread"):
        super().__init__(name=name, target=self, daemon=True)
        sample_width = SAMPLING_16BIT
        self.__stream = stream
        self.__pending = []
        self.__stop = False
        self.__scaling = 2 ** ((sample_width * 8) - 1)

    def stop(self):
        self.__stop = True
        self.__stream.stop_stream()
        self.__stream.close()

    def started(self):
        return not self.__stop

    def __exit__(self):
        self.stop()

    def write(self, frames):
        self.__pending += frames

    def __call__(self):
        while not self.__stop:
            if len(self.__pending) > 0:
                data = self.__pending
                self.__pending = []
                frames = array.array("h", [scale_and_clip_data(d, self.__scaling) for d in data])
                self.__stream.write(frames.tobytes())
            else:
                time.sleep(1/1000)


class WaveStream:
    """Class to wrap the PortAudio API in an object that mirrors the wavefile approach."""

    def __init__(self, filename, mode):
        self.__wavefile = wave.open(filename, mode)
        self.__playing = False
        self.__pyaudio = PyAudio()
        self.__playthread = None
        self.__basestream = None

    def __build_stream(self):
        p = self.__pyaudio
        params = self.__params
        self.__basestream = p.open(format=p.get_format_from_width(params.sampwidth),
            channels=params.nchannels,
            rate=params.framerate,
            output=True)
        return self.__basestream

    def __build_playthread(self):
        if self.__playthread:
            self.__playthread.stop()
        self.__playthread = PlayThread(self.__build_stream())
        self.__playthread.start()
        return self.__playthread

    def __get_playthread(self):
        if not self.__playthread:
            return self.__build_playthread()
        return self.__playthread

    def setparams(self, params):
        self.__wavefile.setparams(params)
        self.__params = WaveParams(*params)

    def writeframesraw(self, bytes):
        self.__get_playthread().write(bytes)
        self.__wavefile.writeframesraw(bytes)

    def writeframes(self, bytes):
        self.__get_playthread().write(bytes)
        self.__wavefile.writeframes(bytes)

    @staticmethod
    def open(filename, mode):
        return WaveStream(filename, mode)

    def close(self):
        self.__wavefile.close()
        self.__basestream.close()

class WaveFile:
    """Class to facilitate simple WAV file output from float data.

      from math import sin, pi
      from wavefile import WaveFile, SAMPLING_RATE
      # Create a 1000Hz signal that lasts 5 seconds
      data = [sin(2*pi*x/SAMPLING_RATE*1000) for x in range(SAMPLING_RATE*5)]
      with WaveFile("test_1000Hz.wav") as wave_file:
        wave_file.writeData(data)
    """

    def __init__(self, filename, audio_factory=wave):
        self._wavefile = audio_factory.open(filename, 'wb')
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
        self._wavefile.writeframesraw(byte_data.tobytes())
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
