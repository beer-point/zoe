import RPi.GPIO as GPIO
import time
import sys

data = []
# seconds
dt = 0.1
dt_in_min = dt/60

FLOW_SENSOR_GPIO = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(FLOW_SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

global count
count = 0
total_flow = 0
start_time = time.time()
total_pulse_count = 0


def countPulse(channel):
    global total_pulse_count
    global count
    total_pulse_count += 1
    if start_counter == 1:
        count = count+1


GPIO.add_event_detect(FLOW_SENSOR_GPIO, GPIO.FALLING, callback=countPulse)

while True:
    try:
        start_counter = 1
        time.sleep(dt)
        start_counter = 0
        # Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
        # 450 pulses x liter
        flow = (count / 7.5)
        print("The flow is: %.4f Liter/min" % (flow))
        total_flow += flow*dt_in_min
        count = 0
    except KeyboardInterrupt:
        print('\n')
        print('\n')
        end_time = time.time()
        print("Total counted flow: %.3f" % total_flow)
        total_time = end_time - start_time
        print("Total time: %.3f" % total_time)
        print("Total pulses: %.3f" % total_pulse_count)
        print("Total pulses counted with semaphore: %.3f" %
              total_pulse_counter)
        total_liters = total_pulse_count/450.0
        print("total in liters: %.4f" % total_liters)

        GPIO.cleanup()
        sys.exit()
