__author__ = 'bretmattingly'

import socket
from threading import local, Thread
from .decoding import decode as message_decode
from queue import Queue, Empty


class Dispatch:
    """
    Dispatch is the main handler of logic for GGMP message boxes.
    In particular, Dispatch:
    * Handles automatic resending of ReqAck messages
    * Handles receipt of Ack messages by maintaining a list of ReqAck messages
    * Prepares messages to send on a call of GGMPClient.send_all()
    *

    Dispatch requires access to the input and output socket threads. The flow
    of incoming message data for the entire library looks like this:

                                        process_ack -> awaitbox.remove()
    UDP bytes -> inthread -> Dispatch <
                                       inbox -> read()
    """
    """

    Dispatch needs:
        - Threader
        - Inbox
        - Outbox
        - Awaitbox
        - Lostbox

    Threader needs:
        - Input/Output socket
        - Server IP
        - "inbox"
        - thread definitions

    """
    pass


class _Threader:
    """
    _Threader is the class responsible for managing the input and output threads
    """

    def __init__(self, c_id, ip_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Input/Output socket
        self.sock.bind(("0.0.0.0", 12358))
        self.inq = Queue()  # Input queue
        self.outq = Queue()  # Output queue
        self.server_addr = ip_addr

        self.outthread = Thread(target=sendmsg, daemon=True, args=(self.outq, self.sock, self.server_addr))
        self.inthread = Thread(target=listen, daemon=True, args=(self.inq, self.sock))

        self.outthread.start()
        self.inthread.start()


def listen(inq, sin):
    while True:
        localdata = local()
        localdata.m = sin.recvfrom(512)
        print("Received " + str(localdata.m[0]) + " from " + str(localdata.m[1]))
        inq.put(localdata.m[0], block=False)
        print(message_decode(localdata.m[0]))


def sendmsg(outq, sock, ip_addr):
    while True:
        localdata = local()
        localdata.m = outq.get(block=True)
        sock.sendto(localdata.m.stream, (ip_addr[0], ip_addr[1]))