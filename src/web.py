from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime
from models.stateList import StateList
import json

json_settings = open('/home/pi/dev/lights/settings.json')
settings = json.load(json_settings)

pinlist = StateList(settings['pins'])
delay = settings['delay']/1000
allowedModes = settings['modes']
mode = "auto"

class SimpleHandler(BaseHTTPRequestHandler):
    print("Listening on port 1224")
    print("~~~~~~~~~")

    def do_GET(self):
        global mode
        message  = ""
        if "automatic" in self.path and mode != "auto":
            self.write_log("Automatic request received while not in auto-mode")
            self.show_status()
        elif "setlights" in self.path:
            lightPattern = int(self.path.split("/")[2])
            state = pinlist.setLights(lightPattern, delay)
            print("~~~~~~~~~~") 
            self.write_log("Set lights to code "+state)
            self.show_status()
        elif "state" in self.path:
            self.show_status()
            self.write_log("Request for state received")
        elif "setMode" in self.path:
            newMode = self.path.split("/")[2]
            if newMode in allowedModes:
                mode = newMode
                self.write_log("Toggled mode to "+mode)
            else:
                self.write_log("Request to set illegal mode "+newMode)
            self.show_status()
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()

    def show_status(self):
        jsonStateList = pinlist.getStatus()
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(jsonStateList, "utf-8"))

    def write_log(self, text):
        today = datetime.now()
        fileformat  = today.strftime("%Y_%m_%d")+".log"
        logFile = open("/var/log/christmas_server/"+fileformat, "a+")
        timestamp = today.strftime("%H:%M:%S.%f")
        message = timestamp + ": "+text
        print(message)
        logFile.write(message + "\r\n")

if __name__ == "__main__":
    try:
        HTTPServer(("0.0.0.0", 1224), SimpleHandler).serve_forever()
    except KeyboardInterrupt:
        print('shutting down server')
