from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from datetime import datetime
from models.stateList import StateList
import json

json_settings = open('/home/pi/dev/lights/settings.json')
settings = json.load(json_settings)

pinlist = StateList(settings['pins'])
delay = settings['delay']/1000

class SimpleHandler(BaseHTTPRequestHandler):
    print("Listening on port 1224")
    print("~~~~~~~~~")
    def do_GET(self):
        message  = ""
        if "setlights" in self.path:
            settings = int(self.path.split("/")[2])
            state = "";

            state = pinlist.setLights(settings, delay)
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
        jsonStateList = pinlist.getStatus()
        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(jsonStateList, "utf-8"))

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
