from datetime import datetime
from controllers.beer_flow_controller.flow_meter_controller import FlowMeterPulsesCounter, FlowPulseObserver, FlowPulseSubject

# 450 pulses -> 1lt
PULSES_PER_LITER = 450


class FlowSession:

    def __init__(self):
        self.is_active = False
        self._flow_pulse_subject = None
        self.started_at = None
        self.ended_at = None

    def start(self):
        self.is_active = True
        self.started_at = datetime.now()
        self._flow_pulse_subject = FlowPulseSubject()
        self._flow_meter_pulses_counter = FlowMeterPulsesCounter()
        self._flow_pulse_subject.attach(self._flow_meter_pulses_counter)
        self._flow_pulse_subject.subscribe_to_gpio_pulse()

    def attach_observer(self, observer: FlowPulseObserver):
        if self._flow_pulse_subject is not None:
            self._flow_pulse_subject.attach(observer)

    def end(self):
        self.ended_at = datetime.now()
        self.is_active = False
        self._flow_pulse_subject.unsubscribe_to_gpio_pulse()
        self._flow_pulse_subject.remove_all()

    def get_flow(self):
        return self._flow_meter_pulses_counter.get_pulses()/PULSES_PER_LITER
