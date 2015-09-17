__author__ = 'bretmattingly'
from . import messages
from . import errors
import socket
from enum import Enum
from queue import Queue, Empty
from threading import local, Thread


class GGMPClient:
    """The primary class exported by the library.

    GGMPClient is designed to be an "automatic" client. Upon creation
    it will spawn two threads, `inbox` and `outbox`, which are
    responsible for the listening and sending of messages.
    """
    def __init__(self, c_id, ip_addr, use_message_ids=True):
        """Constructor


        :param c_id: Client ID. This must be received from the server (generally via another protocol)
        :param ip_addr: IP Address of the server to connect to. Must be tuple of the form (IPv4/v6, Port)
        :param use_message_ids: Whether or not to use Message IDs. Defaults to true.
        :return:
        """
        self.client_id = c_id
        self.use_message_ids = use_message_ids
        self.message_id = 0x000000
        self.sout = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Output socket
        self.sout.bind(ip_addr)
        self.sin = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Input socket
        self.sin.bind((ip_addr[0], ip_addr[1] - 1))
        self.inq = Queue()  # Input queue
        self.outq = Queue()  # Output queue
        self.server_addr = ip_addr

        self.outbox = Thread(target=_sendmsg, args=(self.outq, self.sout, self.server_addr))
        self.inbox = Thread(target=_listen, args=(self.inq, self.sin))

        self.outbox.start()
        self.inbox.start()

        # Todo: Sanity checks

    def send(self):
        pass

    def try_read(self):
        """Non-blocking read.

        Raises `NoMessagesError` if no messages available.
        :return:
        """
        try:
            m = self.inq.get(block=False)
        except Empty:
            raise errors.NoMessagesError

        print("Received message: " + str(m))

    def read(self):
        """Blocking read

        This will block the main client thread (not necessarily the inbox thread).
        :return:
        """

        m = self.inq.get(block=True)
        print("Received message: " + str(m))

    def build_message(self, mtype, ack=False, **kwargs):
        """Builds and enqueues a GGMP message
        This method is used to build any Game State Message Type. Upon
        successful message creation, the message is enqueued in the
        GGMPClient's outbox, and can be sent with a `send()` call or automatically

        :param mtype: Message type. See documentation on `Message` for details.
        :param ack: Whether or not to require an Ack for this message.
        :param kwargs: Values of Components
        :return:
        """
        if mtype == Message.Action:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("Action", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.Action(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        elif mtype == Message.ActionShort:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("ActionShort", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.ActionShort(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        elif mtype == Message.ActionExtended:
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


def _listen(inq, sin):
    while True:
        localdata = local()
        localdata.m = sin.recvfrom(512)
        print("Received " + str(localdata.m[0]) + " from " + str(localdata.m[1]))
        inq.put(localdata.m[0], block=False)


def _sendmsg(outq, sout, ip_addr):
    while True:
        localdata = local()
        localdata.m = outq.get(block=True)
        sout.sendto(localdata.m.stream.to_bytes(21, "big"), (ip_addr[0], ip_addr[1]-1))





