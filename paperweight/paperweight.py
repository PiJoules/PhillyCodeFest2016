#!/usr/bin/env python
import time
import struct
import sys
import requests
import signal
from serial import Serial
from serial.serialutil import SerialException
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

#Config file name
CONFIG_FILE = "paperweight.conf"
#Request delay in seconds
REQUEST_DELAY = 60
#Send this packet to the Arduino to say goodbye
MESSAGE_BYE = b'\xFF\xFF\xFF'

class BadResponse(Exception):
    def __str__(self):
        return "ERROR: {}".format(self.message)

def read_config(fname):
    """
    Read config from a file and return
    the information.

    :param str fname: the filename of the config file

    :rtype: dict, dict
    :returns: (route_info, serial_info)
    """
    config = ConfigParser()
    config.read(fname)

    #Get the route info
    try:
        route_info = dict(config.items('route'))
    except NoSectionError as e:
        print "Error reading bus route information: {}".format(e)
        print "Please check the config file, {}".format(CONFIG_FILE)
        sys.exit(1)

    #Get the serial port info
    try:
        serial_info = dict(config.items('serial'))
        serial_info['baud'] = int(serial_info['baud'])
    except NoSectionError as e:
        print "Error reading serial port information: {}".format(e)
        print "Please check the config file, {}".format(CONFIG_FILE)
        sys.exit(1)
    except ValueError as e:
        print "Baud rate must be an integer."
        print "Please check the config file, {}".format(CONFIG_FILE)
        sys.exit(1)

    try:
        url = config.get('main', 'url')
    except NoOptionError as e:
        print "Missing Server URL."
        print "Please check the config file, {}".format(CONFIG_FILE)
        sys.exit(1)

    return route_info, serial_info, url

def connect(serial_info):
    """
    Connect to Arduino and return a Serial instance.

    :returns: Serial port connection
    :rtype: serial.Serial
    """
    try:
        print "Connecting to Arduino..."
        ser = Serial(serial_info['port'], serial_info['baud'])
        ser.read(1) #Arduino sends a byte when connected
        print "Connected!"
        return ser
    except SerialException as e:
        print "Error connecting to Arduino: {}".format(e)

def fetch_data(url, route_info):
    """
    Fetch data about a route

    :param dict route_info: the information about
        the route for sending to the Flask server.
    """
    response = requests.get(url, params=route_info)
    if response.status_code == 200:
        try:
            return response.json()
        except Exception:
            print response.text
            raise BadResponse("whoops")
    else:
        raise BadResponse("{}: {} - {}".format(response.status_code, response.text, url))

def pack_data(data):
    """
    Pack the message into a serial message

    :param dict data: JSON data
    :rtype: bytes
    :returns: packet message suitable for sending via pySerial
    """
    try:
        arrival_status = data['arrival_status']
        if arrival_status > 6 or arrival_status < -1:
            raise BadResponse("Invalid Arrival status: {}".format(arrival_status))
        elif arrival_status == -1:
            arrival_status = 0
        else:
            arrival_status = 1 << arrival_status

        eta = data['eta'] / 60

        return struct.pack(">BH", arrival_status, eta)
    except Exception as e:
        raise BadResponse(e)

if __name__ == '__main__':
    route_info, serial_info, url = read_config(CONFIG_FILE)
    ser = connect(serial_info)

    def bye(signal, frame):
        print "Bye!"
        ser.write(MESSAGE_BYE)
        ser.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, bye)
    signal.signal(signal.SIGTERM, bye)

    print "Press Ctrl + C to exit."
    while True:
        try:
            data = fetch_data(url, route_info)
            packed = pack_data(data)
            ser.write(packed)
        except BadResponse as e:
            print e
        finally:
            time.sleep(REQUEST_DELAY)
