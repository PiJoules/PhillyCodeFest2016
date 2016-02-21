#!/usr/bin/env python
import time
import struct
from serial import Serial

ser = Serial("COM12", 9600)
ser.read(1)

for arrivalStatus in xrange(-1, 7):
    status = 0 if arrivalStatus == -1 else 1 << arrivalStatus
    eta = status * 5
    data = struct.pack(">BH", status, eta)
    ser.write(data)
    time.sleep(1)

print "Press Ctrl + C to exit."
while True:
    pass
