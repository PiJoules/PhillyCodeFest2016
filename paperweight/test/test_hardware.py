"""
This test can be run through nosetests, but
it requires user input since we need to pause to
check the Arduino.

This test suite is designed to be run by humans, not
by Travis or other automated build system.

This has to be run as:

nosetests -s

to enable printing to stdout.
"""
import struct
import time
from serial import Serial

PORT = "COM12"
BAUD = 9600
MESSAGE_BYE = b"\xFF\xFF\xFF"
MESSAGE_NORMAL = b"\x04\x00\x0D"
MESSAGE_MISALIGNED = MESSAGE_NORMAL + b"\x01"

def prompt_success(message):
    """
    Ask the test operator (me) if each test looks
    successful on the Arduino.

    :param str message: the message to display
    """
    print message
    while True:
        result = raw_input('Success? ').lower()
        if result in ['yes', 'y']:
            return True
        elif result in ['no', 'n']:
            return False

def test_bye():
    print "TEST BYE ========================"
    serial = Serial(PORT, BAUD)
    serial.read(1)
    serial.write(MESSAGE_BYE)
    assert prompt_success("LEDS: all off\nDisplay: Bye!")
    serial.close()

def test_normal():
    print "TEST NORMAL INPUT ===================="
    serial = Serial(PORT, BAUD)
    serial.read(1)
    serial.write(MESSAGE_NORMAL)
    assert prompt_success("LEDS: 0000100\nDisplay: Next bus arrives in 13 min")
    serial.close()

def test_misaligned():
    print "TEST MISALIGNED DATA ==========="
    serial = Serial(PORT, BAUD)
    serial.read(1)
    serial.write(MESSAGE_MISALIGNED)
    assert prompt_success("LEDS: 0000001\nDisplay: Next bus arrives in 13 min")
    serial.write(MESSAGE_NORMAL)
    assert prompt_success("LEDS: 0001101\nDisplay: Next bus arrives in 1024 min")
    serial.close()

def test_spam():
    print "TEST SPAM ======================="
    serial = Serial(PORT, BAUD)
    serial.read(1)
    for x in xrange(1000):
        eta = x % 30
        arrival_status = 1 << (eta % 7)
        message = struct.pack(">BH", eta, arrival_status)
        serial.write(message)
    assert prompt_success("ETA: {} arrival_status: {}".format(eta, bin(arrival_status)))
    serial.close()
