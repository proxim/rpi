'''
Uses 1 LED, 1 buzzer, 1 distance sensor.
Buzzer plays frequency based on distance sensed. 
LED also turns on if in set minimum range.
'''

import RPi.GPIO as GPIO
import time

TRIG = 24
ECHO = 23
LED = 3
Buzzer = 2
minrange = 100
freq = 525
delay = .5

# basic setup for the different pins 
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(Buzzer, GPIO.OUT)
    global Buzz
    Buzz = GPIO.PWM(Buzzer, freq)

setup()
try:
    while True:
        GPIO.output(TRIG, False)
        print('waiting for sensor')
        time.sleep(delay)

        GPIO.output(TRIG, True)
        time.sleep(.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            start = time.time()
        while GPIO.input(ECHO) == 1:
            end = time.time()

        duration = end-start
        distance = duration * 17150
        distance = round(distance, 2)
        if (distance < minrange):
            GPIO.output(LED, True)
            Buzz.stop()
        else:
            GPIO.output(LED, False)
        Buzz.ChangeFrequency(distance * 10)
        print('Distance: ', distance, 'cm')

except KeyboardInterrupt:
    GPIO.output(LED, False)
    GPIO.output(TRIG, False)
    GPIO.output(Buzzer, False)
    GPIO.cleanup()
    print('keyboard interrupted')
