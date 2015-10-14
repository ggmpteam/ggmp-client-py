__author__ = 'bretmattingly'

import socket
from threading import local, Thread
from queue import Queue, Empty
from .decoding import decode as message_decode
from .messages import *
#  from .errors import *


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
    def __init__(self, c_id, ip_addr):
        self.threader = _Threader(c_id, ip_addr)
        self.inbox = Queue()
        self.outbox = Queue()
        self.awaitbox = _Awaitbox()
        self.lostbox = Queue()
        self.tick_count = 0

    def add_message(self, msg):
        self.outbox.put(msg)

    def send_all(self):
        lost = self.awaitbox.tick()
        for m in lost:
            self.lostbox.put(m)

        self.tick_count += 1
        awaiting_ms = self.awaitbox.pull_resend(self.tick_count)
        self.awaitbox.tick()
        for m in awaiting_ms:
            self.threader.add_message(m)

        while not self.outbox.empty():
            try:
                m = self.outbox.get()
                if m.ack:
                    self.awaitbox.add(m)
                #  "Burst fire"
                self.threader.add_message(m)
                self.threader.add_message(m)
                self.threader.add_message(m)
            except Empty:
                break

    def inprocess(self):
        """
        * Read all from threader.inq
        * Decode
        * If any Acks, process awaitbox
        * Move all non-Acks to inbox
        """
        ms = self.threader.read_all()
        for m in ms:
            if type(m) == Ack:
                self.awaitbox.acknowledge(m.mid)
                continue
            else:
                self.inbox.put(m)


class _Threader:
    """
    _Threader is the class responsible for managing the input and output threads
    """
    def __init__(self, c_id, ip_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Input/Output socket
        self.sock.bind(("0.0.0.0", 12358))
        self.inq = Queue()  # Input queue, stores Message objects
        self.outq = Queue()  # Output queue, stores Message objects
        self.server_addr = ip_addr

        self.inthread = Thread(target=listen, daemon=True, args=(self.inq, self.sock))
        self.outthread = Thread(target=sendmsg, daemon=True, args=(self.outq, self.sock, self.server_addr))

        self.inthread.start()
        self.outthread.start()

    def add_message(self, msg):
        self.inq.put(msg)

    def read_all(self):
        ret = []
        while not self.inq.empty():
            try:
                ret.append(self.inq.get())
            except Empty:
                pass

        return ret


def listen(inq, sin):
    while True:
        localdata = local()
        localdata.m = sin.recvfrom(512)
        print("Received " + str(localdata.m[0]) + " from " + str(localdata.m[1]))
        inq.put(message_decode(localdata.m[0]), block=False)
        print(message_decode(localdata.m[0]))


def sendmsg(outq, sock, ip_addr):
    while True:
        localdata = local()
        localdata.m = outq.get(block=True)
        sock.sendto(localdata.m.stream, (ip_addr[0], ip_addr[1]))


class _Awaitbox:
    def __init__(self):
        self.first = dict()
        self.second = dict()
        self.third = dict()
        self.buckets = [dict, dict, dict]
        self.intervals = [1, 3, 5]

    def tick(self):
        """
        "Ticks" the awaitbox, moving all items in first to second, second to third, etc.
        :return: All items which "ticked out" of third (since they should be moved to the lostbox
        """
        ret = self.buckets[2].values()
        self.buckets[2].clear()
        self.buckets[2] = self.buckets[1].copy()
        self.buckets[1].clear()
        self.buckets[1] = self.buckets[0].copy()
        self.buckets[0].clear()


        return ret

    def add(self, msg):
        self.first[msg.mid] = msg

    def acknowledge(self, mid):
        for bucket in self.buckets:
            if mid in bucket:
                del bucket[mid]

    def pull_resend(self, tick_count):
        ret = []
        for index, interval in enumerate(self.intervals):
            if not tick_count % interval:
                ret.extend(self.buckets[index].values())

        return ret
