import RPi.GPIO as GPIO
import json
import time
from models.pinState import PinState

class StateList:
    def __init__(self, stateList):
        self.stateList = []
        print(stateList)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for i, val in enumerate(stateList):
            print(f"Setting up pin#{str(pin.pinNo)}")
            GPIO.setup(pin.pinNo, GPIO.OUT)
            GPIO.output(pin.pinNo, GPIO.HIGH)

            pin = PinState(val['pinNo'], GPIO.HIGH, val['name'])
            self.add(pin)

    def add(self, item):
        self.stateList.append(item)
    
    def setLights(self, stateSet, delay):
        state = ""
        for i, val in enumerate(self.stateList):
            newState = GPIO.HIGH

            if stateSet&(2**i):
                time.sleep(delay)
                newState = GPIO.LOW
            val.state = newState
            result = f"Pin #{str(i+1)} \t(GPIO #{str(val.pinNo)}) \tHIGH: {str(not newState)}"
            print(result)
            state = f"{newState}{state}"
            GPIO.output(val.pinNo, newState)
        print("~~~~~~~~~~")
        return state

    def getStatus(self):
        serializableList = []
        for i, val in enumerate(self.stateList):
            serializableList.append(val.serialize())

        return json.dumps(serializableList, indent=3)




        
