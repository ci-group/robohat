#!/usr/bin/python3
# Makes random beeps

import RPi.GPIO as GPIO
from time import sleep
import random

buzz_pin = 18
buzz_freq = 1000
buzz_dutycycle = 50

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz_pin, GPIO.OUT)
buzz = GPIO.PWM(buzz_pin, buzz_freq)

# Start with 0% duty cycle (0.0 <= DC <= 100.0)
buzz.start(0)

buzz.ChangeDutyCycle(50)
for loop in range(0, 10, 1):
	buzz.ChangeFrequency(random.randint(50,750))
	buzz.ChangeDutyCycle(50)
	sleep(0.05)
	buzz.ChangeDutyCycle(0)
	sleep(0.05)


# added to shutdown the PWM by arnoud 3-8-23
buzz.ChangeDutyCycle(0)
buzz.stop()