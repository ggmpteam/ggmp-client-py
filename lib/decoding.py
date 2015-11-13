__author__ = 'bretmattingly'
from .messages import *
from .errors import *

HEAD_CODES = {
    0x00: (Action, True),
    0x01: (Action, False),
    0x02: (ActionShort, True),
    0x03: (ActionShort, False),
    0x04: (ActionExtended, True),
    0x05: (ActionExtended, False),
    0x0E: (Data, True),
    0x0F: (Data, False),
    0x12: (DataEnd, True),
    0x13: (DataEnd, False),
    0xFF: (Ack, False)
}

#  Message structure AFTER common components (HEAD, CL, MID)
#  Define what components are required, in what order (hence lists instead of sets), and size.
#  Undefined sizes === ? Use sentinel value, -1
MESSAGE_STRUCTURE = {
    Action: (['ar', 'an', 'ac1', 'ac2'], [4, 4, 4, 4]),
    ActionShort: (['ar', 'an', 'ac1', 'ac2'], [1, 1, 1, 1]),
    ActionExtended: (['ar', 'an', 'ac1', 'ac2'], [4, 4, 4, 4]),
    Data: (['pmsg', 'siz', 'dat'], [4, 1, -1]),
    DataEnd: (['pmsg', 'siz', 'dat'], [4, 1, -1]),
    Ack: (['pmsg'], [4])
}


def decode(stream):
    mtype = determine_message_type(stream)
    try:
        return parse_message(mtype, stream)
    except Exception as e:
        print(e)
        raise e


def determine_message_type(stream):
    if not type(stream) == bytearray:
        stream = bytearray(stream)

    mtype = HEAD_CODES[stream[0]]
    return mtype


def parse_message(mtype, stream):
    structure = MESSAGE_STRUCTURE[mtype[0]]

    # Sanity check
    if not len(stream) == 8 + sum(structure[1]) and -1 not in structure[1]:
        raise MalformedMessageError(stream, 4 + sum(structure[1]))
    else:
        message = dict()
        mutstream = bytearray(stream)
        message['head'] = int(mutstream[0])
        del mutstream[0]
        message['cl'] = int.from_bytes(mutstream[0:3], byteorder='big', signed=False)
        del mutstream[0:3]
        message['mid'] = int.from_bytes(mutstream[0:4],  byteorder='big', signed=False)
        del mutstream[0:4]
        for i, component in enumerate(structure[0]):
            if structure[1][i] == -1:
                if 'siz' in message:
                    message[component] = int.from_bytes(mutstream[0:message['siz']], byteorder='big', signed=False)
                    del mutstream[0:message['siz']]
            else:
                message[component] = int.from_bytes(mutstream[0:structure[1][i]], byteorder='big', signed=False)
                del mutstream[0:structure[1][i]]
            pass
        message['ACK'] = mtype[1]
        del message['head']
        print(message)

    return mtype[0](**message)
