from controllers.beer_flow_controller.flow_meter_controller import FlowMeterPulsesCounter, FlowPulseSubject

# 450 pulses -> 1lt
PULSES_PER_LITER = 450


class FlowSession:

    def __init__(self):
        self.is_active = False

    def start(self):
        self.is_active = True
        self._flow_pulse_subject = FlowPulseSubject()
        self._flow_meter_pulses_counter = FlowMeterPulsesCounter()
        self._flow_pulse_subject.attach(self._flow_meter_pulses_counter)
        self._flow_pulse_subject.subscribe_to_gpio_pulse()

    def end(self):
        self.is_active = False
        self._flow_pulse_subject.unsubscribe_to_gpio_pulse()
        self._flow_pulse_subject.remove(self._flow_meter_pulses_counter)

    def get_flow(self):
        return self._flow_meter_pulses_counter.get_pulses()/PULSES_PER_LITER
