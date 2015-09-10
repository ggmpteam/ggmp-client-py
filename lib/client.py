__author__ = 'bretmattingly'
from .utils import append_hex
import socket

class GGMPClient:
    def __init__(self, c_id, ip_addr, use_message_ids=True):
        self.client_id = c_id
        self.use_message_ids = use_message_ids
        self.message_id = 0x00000000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(ip_addr)
        # Todo: Create a thread receiving on the designated socket and listen on it
        # Todo: Sanity checks

    def send(self, actor_id, action_id, condition1=0x0000, condition2=0x0000):
        message = 0xFF  # Initial message to contain header
        message = append_hex(message, bin(self.client_id))
        message = append_hex(message, bin(self.message_id))
        self.message_id += 1
        message = append_hex(message, bin(actor_id))
        message = append_hex(message, bin(action_id))
        message = append_hex(message, bin(condition1))
        message = append_hex(message, bin(condition2))
        print(hex(message))
        self.s.sendto(str(message).encode(), ("127.0.0.1", 8081))

    def build_message(self, actor_id, action_id, condition1, condition2):
        # 0xFF  00  00000000    00  00  00  00
        # HEAD  CL  MESS_ID     AC  AR  C1  C2

        # header
        message = 0xFF

        # client id
        message <<= 8
        message += (self.client_id & 0xFF)

        # message id
        message <<= 8 * 4
        message += (self.message_id & 0xFFFFFFFF)
        self.message_id += 1

        # actor id
        message <<= 8
        message += (actor_id & 0xFF)

        # action id
        message <<= 8
        message += (action_id & 0xFF)

        # Condition 1
        message <<= 8
        message += (condition1 & 0xFF)

        # Condition 2
        message <<= 8
        message += (condition2 & 0xFF)

        return message





