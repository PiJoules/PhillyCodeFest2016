#!/usr/bin/env python
import time
import struct
import random
from serial import Serial
from ConfigParser import ConfigParser

#Request delay in seconds
REQUEST_DELAY = 10

#Send this packet to the Arduino to say goodbye
MESSAGE_BYE = b'\xFF\xFF\xFF'

class BadResponse(Exception):
    def __str__(self):
        return "ERROR: {}".format(self.message)

def read_config(fname):
    """
    Read config from a file and return
    the information.

    :rtype: dict, dict
    :returns: (route_info, serial_info)
    """
    config = ConfigParser()
    config.read(fname)

    #Get the route info
    route_info = dict(config.items('route'))

    #Get the serial port info
    serial_info = dict(config.items('serial'))
    serial_info['baud'] = int(serial_info['baud'])

    return route_info, serial_info

def connect(serial_info):
    """
    Connect to Arduino and return a Serial instance.

    :returns: Serial port connection
    :rtype: serial.Serial
    """
    print "Connecting to Arduino..."
    ser = Serial(serial_info['port'], serial_info['baud'])
    ser.read(1) #Arduino sends a byte when connected
    print "Connected!"
    return ser

def fetch_data(route_info):
    """
    Fetch data about a route

    :param dict route_info: the information about
        the route for sending to the Flask server.
    """
    #TODO: Use Requests
    return {
        'arrival_status': random.randint(-10, 10),
        'eta': random.randint(0, 600),
    }

def pack_data(data):
    """
    Pack the message into a serial message

    :param dict data: JSON data
    :rtype: bytes
    :returns: packet message suitable for sending via pySerial
    """
    #TODO: Add error checking
    arrival_status = data['arrival_status']
    if arrival_status > 6 or arrival_status < -1:
        raise BadResponse("Invalid Arrival status: {}".format(arrival_status))
    if arrival_status == -1:
        arrival_status = 0
    else:
        arrival_status = 1 << arrival_status

    eta = data['eta']

    return struct.pack(">BH", arrival_status, eta)

if __name__ == '__main__':
    route_info, serial_info = read_config('paperweight.conf')
    ser = connect(serial_info)

    print "Press Ctrl + C to exit."
    try:
        while True:
            try:
                data = fetch_data(route_info)
                packed = pack_data(data)
                ser.write(packed)
            except BadResponse as e:
                print e
            finally:
                time.sleep(REQUEST_DELAY)
    except KeyboardInterrupt:
        print "Bye!"
        ser.write(MESSAGE_BYE)
