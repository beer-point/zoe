import time
from controllers.beer_flow_controller.mock_gpio import GPIO

FLOW_SENSOR_GPIO = 26
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.cleanup()


# pf = pulse frecueny (Hz)
# ppl = pulses per liter
# Q = flow rate in L/min.
#
# pf = ppl/60 * Q
# pf = (450 / 60)*Q
# pf = 7.5*Q
#  ====>   number_of_pulses_in_one_sec / 7.5 = flow rate in L/min
MIN_TIME_BETWEEN_PULSES_CONSIDERED_LIQUID = 1  # TODO: define this threshold


class FlowPulseObserver:
    def update():
        pass


class FlowPulseSubject:

    def __init__(self):
        self.observers: list[FlowPulseObserver] = []
        self._gpio = None

    def notify(self):
        for observer in self.observers:
            observer.update()

    def attach(self, observer: FlowPulseObserver):
        self.observers.append(observer)

    def remove(self, observer: FlowPulseObserver):
        self.observers.remove(observer)

    def unsubscribe_to_gpio_pulse(self):
        if not self._gpio == None:
            self._gpio.close()

    def subscribe_to_gpio_pulse(self):
        self._gpio = GPIO()
        self._gpio.add_event_detect(
            FLOW_SENSOR_GPIO, GPIO.FALLING, callback=self.notify)


class INonLiquidDetector:
    """Detects when flow is non liquid"""
    def is_non_liquid():
        pass


class NonLiquidDetector(FlowPulseObserver, INonLiquidDetector):
    def __init__(self):
        self._last_pulse_timestamp = 0
        self._is_non_liquid = False

    def update(self):
        last_pulse_timestamp = self._last_pulse_timestamp
        self._last_pulse_timestamp = time.time()
        if self._last_pulse_timestamp - last_pulse_timestamp > MIN_TIME_BETWEEN_PULSES_CONSIDERED_LIQUID:
            self._is_non_liquid = True
        else:
            self._is_non_liquid = False

    def is_non_liquid(self):
        return self._is_non_liquid


class IFlowMeterPulsesCounter:
    def get_pulses():
        pass


class FlowMeterPulsesCounter(FlowPulseObserver, IFlowMeterPulsesCounter):
    """Holds information of the flow count in ml"""

    def __init__(self):
        self._pulses = 0
        self._non_liquid_detector = NonLiquidDetector()

    def update(self):
        self._non_liquid_detector.update()
        # dont count pulses if we detect non liquid
        if not self._non_liquid_detector.is_non_liquid():
            self._pulses += 1

    def get_pulses(self):
        return self._pulses
