#!/usr/bin/env python
DELAY_AMOUNT = 3
from serial import Serial
import time

ser = Serial("COM12", 9600)
#TODO: Use a serial protocol and handshake until we
#can connect.
print "Waiting for connection..."
time.sleep(DELAY_AMOUNT)
print "Connected!"

for arrivalStatus in xrange(-1, 7):
    status = 0 if arrivalStatus == -1 else 1 << arrivalStatus
    #TODO: This should eventually be a short
    eta = status
    data = chr(status) + chr(eta)
    ser.write(data)
    time.sleep(1)

print "Press Ctrl + C to exit."
while True:
    pass
