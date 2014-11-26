"""Timing classes to help power all of the time-related activities"""
from . import EventSender
import threading
import time

@EventSender("tick")
class Clock(threading.Thread):
    """A basic clock. It ticks on regularish intervals. 
    Subject to the limits of time.sleep"""
    def __init__(self, name, ticks_per_second):
        """The name is a useful attribute to help remember 
        which clock object is responsible for the given
        event."""
        self.__tick = 0
        self.__sleep = 1 / ticks_per_second
        super().__init__(name=name, target=self, daemon=True)
        self.__stop = False

    def __call__(self):
        while not self.__stop:
            self.send_tick_event(self.__tick)
            self.__tick += 1
            time.sleep(self.__sleep)

    def stop(self):
        """Cause the thread to stop doing anything. This
        does not support re-starting."""
        self.__stop = True

    def ticks_per_second():
        doc = "How many tick events fire every second"
        def fget(self):
            return self.__sleep
        def fset(self, value):
            self.__sleep = 1 / value
        def fdel(self):
            del self.__sleep
        return locals()
    ticks_per_second = property(**ticks_per_second())


