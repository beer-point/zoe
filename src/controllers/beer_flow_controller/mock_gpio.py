from random import random
from threading import Thread
import time

MOCKED_FLOW = 500  # ml
MOCKED_SERVING_TIME = 5  # seconds

mocked_flow_in_pulses = (450.0*MOCKED_FLOW) / 1000.0


class GPIO(Thread):
    FALLING = 1

    def __init__(self):
        Thread.__init__(self)
        self._close = False
        self._pulse = None
        self._start_time = time.time()

    def run(self):
        while not self._close:
            time.sleep(MOCKED_SERVING_TIME/mocked_flow_in_pulses)
            if not self.is_idle():
                self._pulse()

    def add_event_detect(self, sensor, mode, callback):
        self._pulse = callback
        self.start()

    def close(self):
        self._close = True

    # mocks a user serving beer
    def is_idle(self):
        now = time.time()
        return (now - self._start_time) < 3 or (now - self._start_time) > 9
