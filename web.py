import BaseHTTPServer
import urlparse
from datetime import datetime
import RPi.GPIO as GPIO
pinlist = [14,15,18,23]
class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i, val in enumerate(pinlist):
        print("Setting up pin #"+str(val)) 
        GPIO.setup(val, GPIO.OUT)
        GPIO.output(val, GPIO.HIGH)

    print("Listening on port 1224")
    def do_GET(self):
        GPIO.output(14, 1)
        self.send_response(200)
        if "setlights" in self.path:
            settings = int(self.path.split("/")[2])
            state = "";
            for i, val in enumerate(pinlist):
                newState = GPIO.LOW
                
                if settings&(2**i):
                    newState = GPIO.HIGH
                    print("Turn on pin #"+str(i+1) + "(GPIO #" +str(val) +") value: "+ str(newState))
                else:
                    print("Turn off pin #"+str(i+1) + "(GPIO #" + str(val) + ") value: "+ str(newState))

                state = str(newState) + state
                GPIO.output(val, newState)
                print(GPIO.input(val))
            print("~~~~~~~~~~") 
            
            today = datetime.now()
            fileformat  = today.strftime("%Y_%m_%d")+".log"
            logFile = open("logs/"+fileformat, "a+")
            timestamp = today.strftime("%H:%M:%S.%f")
            print("New state: "+state)
            logFile.write(timestamp+ ": Set lights to code "+state+"\r\n")

if __name__ == "__main__":
    try:
        BaseHTTPServer.HTTPServer(("0.0.0.0", 1224), SimpleHandler).serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')
