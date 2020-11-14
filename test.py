import RPi.GPIO as GPIO
import time 
# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)
print(GPIO.HIGH)
print(GPIO.LOW)
# Turn on/off LED based on user input
try:
    while True:
        GPIO.output(14, 1)
        print("pin 14 is on")
        time.sleep(0.5)
        GPIO.output(14,0)
        print("pin 14 is off")
        time.sleep(.5)
except KeyboardInterrupt:
   GPIO.cleanup()
   print("Goodbye")

