#!/usr/bin/env python
import time
import struct
import sys
import requests
import signal
from serial import Serial
from serial.serialutil import SerialException
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from requests.exceptions import ConnectionError

#Config file name
CONFIG_FILE = "paperweight.conf"
#Request delay in seconds
REQUEST_DELAY = 60
#Send this packet to the Arduino to say goodbye
MESSAGE_BYE = b'\xFF\xFF\xFF'

class BadResponse(Exception):
    """
    We sent a request and got back garbage. Whoops.
    """
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
    except (ValueError, KeyError) as e:
        print "baud must be an integer."
        print "Please check the config file, {}".format(CONFIG_FILE)
        sys.exit(1)

    try:
        misc_info = dict(config.items('main'))
    except NoSectionError as e:
        print "Error reading main info section."
        print "Please check the config file, {}".format(CONFIG_FILE)
        sys.exit(1)

    return route_info, serial_info, misc_info

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

def fetch_data(misc_info, route_info):
    """
    Fetch data about a route

    :param dict misc_info: main config params, including
        the server url
    :param dict route_info: the information about
        the route for sending to the Flask server.
    """
    try:
        response = requests.get(misc_info['url'], params=route_info)
    except ConnectionError as e:
        raise BadResponse("Error when connecting to server: {}".format(e.message))

    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            print response.text
            raise BadResponse("Error when reading JSON: {} Response: {}".format(e, response.text))
    else:
        raise BadResponse("{}: {} - {}".format(response.status_code, response.text, misc_info['url']))

def pack_data(data):
    """
    Pack the message into a serial message

    :param dict data: JSON data
    :param dict misc_info: miscellaneous config params, including
        the adjusted time
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
    route_info, serial_info, misc_info = read_config(CONFIG_FILE)
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
            data = fetch_data(misc_info, route_info)
            packed = pack_data(data)
            ser.write(packed)
        except BadResponse as e:
            print e
        except Exception as e:
            print e
        finally:
            time.sleep(REQUEST_DELAY)
