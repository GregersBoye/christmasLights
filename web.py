from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime
import time
import json
import RPi.GPIO as GPIO

json_settings = open('/home/pi/dev/lights/settings.json')
settings = json.load(json_settings)

pinlist = settings['pins']
delay = settings['delay']/1000

class SimpleHandler(BaseHTTPRequestHandler):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i, val in enumerate(pinlist):
        print("Setting up pin #"+str(val)) 
        GPIO.setup(val, GPIO.OUT)
        GPIO.output(val, GPIO.HIGH)

    print("Listening on port 1224")
    print("~~~~~~~~~")
    def do_GET(self):
        message  = ""
        if "setlights" in self.path:
            settings = int(self.path.split("/")[2])
            state = "";
            for i, val in enumerate(pinlist):
                newState = GPIO.HIGH
                
                if settings&(2**i):
                    time.sleep(delay)
                    newState = GPIO.LOW
                result = "Pin #"+str(i+1) + "\t(GPIO #" + str(val) + ") \tHIGH: "+ str(not newState)
                print(result)
                state = str(newState) + state
                GPIO.output(val, newState)
            print("~~~~~~~~~~") 
            self.write_log(state)
            self.show_status()
        elif "state" in self.path:
            self.show_status()
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def show_status(self):
        statusList = []
        for i, val in enumerate(pinlist):
            pinState = GPIO.input(val)
            statusList.append({'state': not pinState, 'pin': val})

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(statusList, indent=3), "utf-8"))

    def write_log(self, state):
        today = datetime.now()
        fileformat  = today.strftime("%Y_%m_%d")+".log"
        logFile = open("/var/log/christmas_server/"+fileformat, "a+")
        timestamp = today.strftime("%H:%M:%S.%f")
        logFile.write(timestamp+ ": Set lights to code "+state+"\r\n")

if __name__ == "__main__":
    try:
        HTTPServer(("0.0.0.0", 1224), SimpleHandler).serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')
