import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG1 = 17
ECHO1 = 27

TRIG2 = 22  # Change to your GPIO pin number
ECHO2 = 23  # Change to your GPIO pin number

GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)

GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

def get_distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    start_time = time.time()
    end_time = time.time()

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        end_time = time.time()

    duration = end_time - start_time
    distance = (duration * 34300) / 2
    return distance

try:
    while True:
        distance1 = get_distance(TRIG1, ECHO1)
        distance2 = get_distance(TRIG2, ECHO2)
        print(f"Distance from Sensor 1: {distance1:.2f} cm")
        print(f"Distance from Sensor 2: {distance2:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
