from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime
import time
import RPi.GPIO as GPIO
pinlist = [14,15,18,23,24, 25,8,7]

class SimpleHandler(BaseHTTPRequestHandler):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i, val in enumerate(pinlist):
        print("Setting up pin #"+str(val)) 
        GPIO.setup(val, GPIO.OUT)
        GPIO.output(val, GPIO.HIGH)

    print("Listening on port 1224")
    def do_GET(self):
        message  = ""
        GPIO.output(14, 1)
        if "setlights" in self.path:
            settings = int(self.path.split("/")[2])
            state = "";
            for i, val in enumerate(pinlist):
                newState = GPIO.HIGH
                
                if settings&(2**i):
                    newState = GPIO.LOW
                    result = "Turn on pin #"+str(i+1) + "(GPIO #" +str(val) +") value: "+ str(newState)
                else:
                    result = "Turn off pin #"+str(i+1) + "(GPIO #" + str(val) + ") value: "+ str(newState)
                time.sleep(.05)
                print(result)
                message  += result+ "<br />\r\n"
                state = str(newState) + state
                GPIO.output(val, newState)
            print("~~~~~~~~~~") 
            
            today = datetime.now()
            fileformat  = today.strftime("%Y_%m_%d")+".log"
            logFile = open("/var/log/christmas_server/"+fileformat, "a+")
            timestamp = today.strftime("%H:%M:%S.%f")
            print("New state: "+state)
            logFile.write(timestamp+ ": Set lights to code "+state+"\r\n")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Christmas controller</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>"+message+"</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
if __name__ == "__main__":
    try:
        HTTPServer(("0.0.0.0", 1224), SimpleHandler).serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')
