#!/usr/bin/python3

"""!
Copyright © 2023 Vrije Universiteit Amsterdam
Electronica-Beta-VU
A. Denker (a.denker@vu.nl)

Makes random beeps
"""

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

buzz.start(0)

buzz.ChangeDutyCycle(50)
for loop in range(0, 10, 1):
	buzz.ChangeFrequency(random.randint(50,750))
	buzz.ChangeDutyCycle(50)
	sleep(0.05)
	buzz.ChangeDutyCycle(0)
	sleep(0.05)

buzz.ChangeDutyCycle(0)
buzz.stop()