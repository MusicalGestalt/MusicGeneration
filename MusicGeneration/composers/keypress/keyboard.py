"""This keyboard-driven composer will detect time differences
between keyboard events and use those to build new patterns."""

from MusicGeneration.rhythm import fourfour
from MusicGeneration.rhythm.interval_sequences import BaseIntervalGenerator
from collections import namedtuple
from ..clock import Clock
from ..events import EventReceiver, EventSender
from .keyserver import start_server, stop_server

def keyfilter(*args):
    return lambda x: x in args

@EventSender("interval")
@EventReceiver("tick", "do_tick")
@EventReceiver("key", "do_key")
class KeyboardCapturer:
    def __init__(self, clock, server, time_signature=fourfour, 
        capture_idle_time=None, filt=None):

        if capture_idle_time is None:
            capture_idle_time = time_signature.whole_note
        if filt is None:
            filt = lambda x: True
        self.__capture_started = False
        self.__clock = clock
        self.__start_tick = 0
        self.__captures = []
        self.__idle = capture_idle_time
        self.__filt = filt
        self.register_key(server)
        self.register_tick(clock)

    def __prep_capture(self):
        self.__captures = []
        self.__start_tick = self.__clock.current_tick
        self.__capture_started = True

    @property
    def __delta(self):
        return self.__clock.current_tick - self.__start_tick

    def do_key(self, sender, key):
        if self.__capture_started:
            if self.__filt(key):
                self.__captures += [(key, self.__delta)]
                self.__start_tick = self.__clock.current_tick
        else:
            self.__prep_capture()

    def do_tick(self, sender, tick):
        if self.__delta > self.__idle:
            self.send_interval_event(self.__captures)
            self.__capture_started = False

@EventReceiver("interval", "new_interval")
class KeyboardSequenceGenerator:
    def __init__(self, capturer):
        self.__capture = capturer
        self.register_interval(capturer)
        self.__intervals = None
        self.__ticker = -1

    def new_interval(self, sender, sequence):
        self.__intervals = sequence

    def step(self, last_beat=0):
        if self.__intervals is None:
            return [0]
        self.__ticker += 1
        self.__ticker %= len(self.__intervals)
        return self.__intervals[self.__ticker][1]
        

