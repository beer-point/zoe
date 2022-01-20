
import time
from controllers.beer_flow_controller.flow_meter_controller import FlowPulseObserver
from controllers.beer_flow_controller.flow_session import FlowSession
from kivy.clock import Clock


class BeerFlowIdleObserver(FlowPulseObserver):
    def __init__(self, on_idle) -> None:
        self._last_pulse_time = None
        self._on_idle = on_idle

        def check_for_idle(interval):
            if self._last_pulse_time is not None:
                if time.time() - self._last_pulse_time > 5:
                    self._on_idle()
                    return False

        self.check_idle_clock = Clock.schedule_interval(check_for_idle, 0.1)

    def cancel(self):
        self.check_idle_clock.cancel()

    def update(self):
        self._last_pulse_time = time.time()
