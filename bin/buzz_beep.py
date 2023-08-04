#!/usr/bin/python3

# beeps for 100 mS

import RPi.GPIO as GPIO
from time import sleep
import random

buzz_pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz_pin, GPIO.OUT)

buzz = GPIO.PWM(buzz_pin, 1000)

buzz.start(0)
buzz.ChangeDutyCycle(50)

sleep(0.1)
buzz.ChangeDutyCycle(0)
buzz.stop()

