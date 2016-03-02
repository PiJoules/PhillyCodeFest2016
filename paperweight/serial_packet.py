START_BYTE = b'\x13'
ESC_BYTE = b'\x14'
STOP_BYTE = b'\x15'

def fletcher16(data):
    """
    Calculate the Fletcher-16
    checksum of a bytes object

    :param bytes data: the input data in bytes
    :returns: the fletcher-16 checksum (2 bytes)
    """
    c0 = 0
    c1 = 0
    for b in data:
        c0 += ord(b)
        c0 &= 0xFF
        c1 += c0
        c1 &= 0xFF
    return chr(c0) + chr(c1)

def escape(msg):
    """
    Escape a message with the escape value

    :param bytes msg: the message to escape
    :returns: a generator that generates the bytes,
        escaping START_BYTE, ESC_BYTE and STOP_BYTE
    """
    for b in msg:
        if b in [START_BYTE, ESC_BYTE, STOP_BYTE]:
            yield ESC_BYTE
        yield b

def make_packet(msg):
    """
    Create a packet from a binary message

    :param bytes: mssg: the message to turn into
        a packet

    :returns: a new bytes object after prefixing
        the length, adding the fletcher-16 checksum
        and framing the packet with start and

    :raises: ValueError if msg is too large after
        escaping.
    """
    #Escape the payload and check the length of the output
    payload = ''.join(escape(msg))
    if len(payload) > 0xFF:
        raise ValueError("Packets must be within 256 bytes for now")

    #Return the packet
    return (START_BYTE
        + chr(len(payload))
        + payload
        + fletcher16(payload)
        + STOP_BYTE)
