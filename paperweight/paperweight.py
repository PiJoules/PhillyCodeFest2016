#!/usr/bin/env python
import time
import struct
import random
from serial import Serial

#Request delay in seconds
REQUEST_DELAY = 10

#TODO: Read this from a config file
STOP_ID = "699"
ROUTE = "44"
DIRECTION = "eastbound"
PORT = "COM12"
BAUD = 9600

#Connect to Arduino
print "Connecting to Arduino..."
ser = Serial(PORT, BAUD)
ser.read(1)
print "Connected!"

print "Press Ctrl + C to exit."
try:
    while True:
        #Query the current status
        #TODO: use requests!
        data = {
            'arrival_status': random.randint(0, 6),
            'eta': random.randint(0, 600),
        }

        arrival_status = data['arrival_status']
        arrival_status = 0 if arrival_status == -1 else 1 << arrival_status

        eta = data['eta']

        data = struct.pack(">BH", arrival_status, eta)
        ser.write(data)
        time.sleep(REQUEST_DELAY)
except KeyboardInterrupt:
    print "Bye!"
    ser.write("\xFF\xFF\xFF")
