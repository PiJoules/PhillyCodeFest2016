from nose.tools import raises
from paperweight.serial_packet import *

@raises(ValueError)
def test_too_long():
    """Make sure messages that are too long throw a ValueError"""
    list(make_packet(b'\x00' * 256))

def test_fletcher():
    """
    Make sure we can calculate the checksum properly

    Byte    Value   C0      c1
    H       72      72      72
    E       69      141     213
    L       76      217     174
    L       76      37      211
    O       79      116     71   -> \\x74\\x47 -> tG
    """
    expected = b'\x74\x47'
    actual = fletcher16(b'HELLO')
    assert actual == expected, "{} should be {}".format(
        repr(actual), repr(expected))

def test_fletcher_empty():
    """
    A zero-length message should return a checksum of \\x00\\x00
    """
    expected = b'\x00\x00'
    actual = fletcher16(b'')
    assert actual == expected, "{} should be {}".format(
        repr(actual), repr(expected))

def test_short():
    """Make sure that a 0 byte message works"""
    output = b''.join(make_packet(b''))
    expected = b'\x13\x00\x00\x00\x15'
    assert output == expected, "{} should be {}".format(
        repr(output), repr(expected))

def test_regular():
    """
    Make sure that a regular message works
    Fletcher Calculation:

    Byte    Value   C0      c1
    H       72      72      72
    E       69      141     213
    L       76      217     174
    L       76      37      211
    O       79      116     71   -> \x74\x47 -> tG
    """
    output = b''.join(make_packet(b'HELLO'))
    expected = b'\x13\x05HELLO\x74\x47\x15'
    assert output == expected, "{} should be {}".format(
        repr(output), repr(expected))

def test_escaped():
    """
    Make sure escaped messages work
    """
    message = "\x00\x13\x00\x14\x00\x15\x00"
    expected = "\x00\x14\x13\x00\x14\x14\x00\x14\x15\x00"
    actual = ''.join(escape(message))
    assert actual == expected, "{} should be {}".format(
        repr(actual), repr(expected))
