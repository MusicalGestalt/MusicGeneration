"""This module contains helper classes for stubbing out and testing
keyboard related operations."""

from . import *
from MusicGeneration.composers.clock import BaseClock
from MusicGeneration.composers import EventSender, EventReceiver

FakeClock = BaseClock


@EventReceiver("tick", "do_tick")
@EventSender("key")
class FakeServer:
    def __init__(self, clock, ticks_between_keys=32, total_sends=4):
        self.register_tick_event(clock)
        self.__wait = ticks_between_keys
        self.__tosend = total_sends

    def do_tick(self, sender, tick):
        if tick % self.__wait == 0 and self.__tosend > 0:
            self.send_key_event("A")
            self.__tosend -= 1