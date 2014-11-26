from . import EventSender
import threading
import time

@EventSender("tick")
class Clock(threading.Thread):
    def __init__(self, name, ticks_per_second):
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
        self.__stop = True

    def set_speed(self, ticks_per_second):
        self.__sleep = 1 / ticks_per_second


