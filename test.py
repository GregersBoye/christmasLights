import RPi.GPIO as GPIO
import time 
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)

GPIO.setup(15,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
print(GPIO.HIGH)
print(GPIO.LOW)
# Turn on/off LED based on user input
try:
    while True:
        GPIO.output(14, 1)
        time.sleep(.5)
        GPIO.output(15,1)
        time.sleep(.5)
        GPIO.output(18,1)
        time.sleep(.5)
        GPIO.output(23,1)
        print("pin 14 is on")
        GPIO.output(14,0 )
        time.sleep(.5)
        GPIO.output(15,0)
        time.sleep(.5)
        GPIO.output(18,0)
        time.sleep(.5)
        GPIO.output(23,0)
        print("pin 14 is off")
except KeyboardInterrupt:
   GPIO.cleanup()
   print("Goodbye")

