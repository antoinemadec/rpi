#!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN)
GPIO.setup(25,GPIO.OUT)
while True:
	if GPIO.input(24):
		GPIO.output(25,GPIO.HIGH)
		time.sleep(0.1)
    		GPIO.output(25,GPIO.LOW)
    		time.sleep(0.1)
	else:
		GPIO.output(25,GPIO.LOW)
    		time.sleep(1)
