"""This module contains helper classes for stubbing out and testing
keyboard related operations."""

from . import *
from MusicGeneration.composers.clock import BasicClock
from MusicGeneration.composers import EventSender, EventReceiver

FakeClock = BasicClock

DEFAULT_TICKS_BETWEEN = 32
DEFAULT_SENDS = 4


@EventReceiver("tick", "do_tick")
@EventSender("key")
class FakeServer:
    def __init__(self, clock, ticks_between_keys=DEFAULT_TICKS_BETWEEN, 
        total_sends=DEFAULT_SENDS):
        self.register_tick(clock)
        self.__wait = ticks_between_keys
        self.__tosend = total_sends

    def do_tick(self, sender, tick):
        if tick % self.__wait == 0 and self.__tosend > 0:
            self.send_key_event("A")
            self.__tosend -= 1

@EventReceiver("interval", "catch")
class IntervalCatcher:
    def __init__(self):
        self.caught = False
        self.interval = None

    def catch(self, sender, interval):
        self.interval = interval
        self.caught = True