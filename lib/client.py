__author__ = 'bretmattingly'
from . import messages
from . import errors
import socket
from enum import Enum
from queue import Queue


class GGMPClient:
    def __init__(self, c_id, ip_addr, use_message_ids=True):
        self.client_id = c_id
        self.use_message_ids = use_message_ids
        self.message_id = 0x000000
        self.sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sout.bind(ip_addr)
        self.sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sin.bind((ip_addr[0], ip_addr[1] - 1))
        self.inq = Queue()
        self.outq = Queue()

        # Todo: Create a thread receiving on the designated socket and listen on it
        # Todo: Sanity checks

    def send(self):
        pass

    def build_message(self, type, ack=False, **kwargs):
        if type == Message.Action:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("Action", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.Action(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        elif type == Message.ActionShort:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("ActionShort", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.ActionShort(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        elif type == Message.ActionExtended:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("ActionExtended", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.ActionExtended(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        else:
            raise errors.UnknownTypeError(type)

        self.outq.put(m, block=False)


class Message(Enum):
    Action          = 1
    ActionShort     = 2
    ActionExtended  = 3
    Data            = 4
    DataEnd         = 5
    Ack             = 6



