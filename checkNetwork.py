#!/usr/bin/python
import RPi.GPIO as GPIO
import urllib.request
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT)
try:
    while True:
        GPIO.output(2,GPIO.LOW)
        time.sleep(0.25)
        try:
            urllib.request.urlopen("http://www.google.com").close()
        except:
            print("Not Connected")
        else:
            print("Connected")
            GPIO.output(2, GPIO.HIGH)
        time.sleep(1)
except KeyboardInterrupt:
    print("Keyboard stopped the show")
    GPIO.cleanup()
