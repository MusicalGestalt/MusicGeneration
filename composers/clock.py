"""Timing classes to help power all of the time-related activities"""
from . import EventSender
import threading
import time


@EventSender("tick")
class BasicClock():
    """Base Clock class"""
    def __init__(self, name):
        """The name is a useful attribute to help remember 
        which clock object is responsible for the given
        event."""
        self.__tick = 0

    def increment(self, loops=1):
        for loop in range(loops):
            self.send_tick_event(self.__tick)
            self.__tick += 1


class Clock(threading.Thread, BasicClock):
    """A basic clock. It ticks on regularish intervals. 
    Subject to the limits of time.sleep"""
    def __init__(self, name, ticks_per_second):
        """The name is a useful attribute to help remember 
        which clock object is responsible for the given
        event."""
        threading.Thread.__init__(self, name=name, target=self, daemon=True)
        BasicClock.__init__(self, name)
        self.__sleep = 1.0 / ticks_per_second
        self.__stop = False

    def __call__(self):
        while not self.__stop:
            self.increment()
            time.sleep(self.__sleep)

    def stop(self):
        """Cause the thread to stop doing anything. This
        does not support re-starting."""
        self.__stop = True

    def ticks_per_second():
        doc = "How many tick events fire every second"
        def fget(self):
            # TODO(Remy): This seems unusual, returning the sleep time
            # for ticks_per_second. Should it return 1.0 / __sleep ?
            return self.__sleep
        def fset(self, value):
            self.__sleep = 1.0 / value
        def fdel(self):
            del self.__sleep
        return locals()
    ticks_per_second = property(**ticks_per_second())


