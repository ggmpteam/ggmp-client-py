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
    structure = MESSAGE_STRUCTURE[mtype]
    if not len(stream) == 4 + sum(structure[1]):
        raise MalformedMessageError(stream, 4 + sum(structure[1]))
    else:
        message = dict()
        message['head'] = stream.pop(0)
        message['cl'] = bytes.join(stream[0:3])
        del stream[0:3]
        message['mid'] = bytes.join(stream[0:4])
        del stream[0:4]
        for i, component in enumerate(structure[0]):
            if not structure[1][i] == -1:
                if 'siz' in message:
                    message[component] = bytes.join(stream[0:message['siz']])
                    del stream[0:message['siz']]
            else:
                message[component] = bytes.join(stream[0:structure[1][i]])
                del stream[0:structure[1][i]]
            pass
        message['ACK'] = mtype[1]

    return mtype[0](**message)