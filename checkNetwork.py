#!/usr/bin/python
import os
import time
import urllib.request
import time

try:
    while True:
        try:
            urllib.request.urlopen("http://www.google.com").close()
        except:
            print("Not Connected")
        else:
            print("Connected")
        time.sleep(1)
except KeyboardInterrupt:
    print("Keyboard stopped the show")
    
