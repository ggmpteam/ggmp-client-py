__author__ = 'bretmattingly'


class Action:
    def __init__(self, ACK, cl, mid, ar, an, ac1, ac2):
        self.stream = bytearray([0x01]) if ACK else bytearray([0x00])
        self.stream.extend((cl & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((mid & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((ar & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((an & 0xFFFF).to_bytes(2, "big", signed=False))
        self.stream.extend((ac1 & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ac2 & 0xFFFFFFFF).to_bytes(4, "big", signed=False))


class ActionShort:
    def __init__(self, ACK, cl, mid, ar, an, ac1, ac2):
        self.stream = 0x02
        if ACK:
            self.stream += 0x01
        self.stream <<= 8 * 1

        self.stream += (cl & 0xFF)
        self.stream <<= 8 * 1

        self.stream += (mid & 0xFFFF)
        self.stream <<= 8 * 2

        self.stream += (ar & 0xFF)
        self.stream <<= 8 * 1

        self.stream += (an & 0xFF)
        self.stream <<= 8 * 1

        self.stream += (ac1 & 0xFF)
        self.stream <<= 8 * 1

        self.stream += (ac2 & 0xFF)
        self.stream <<= 8 * 1


class ActionExtended:
    def __init__(self, ACK, cl, mid, ar, an, ac1, ac2):
        self.stream = 0x04
        if ACK:
            self.stream += 0x01
        self.stream <<= 8 * 1

        self.stream += (cl & 0xFFFFFF)
        self.stream <<= 8 * 3

        self.stream += (mid & 0xFFFFFF)
        self.stream <<= 8 * 3

        self.stream += (ar & 0xFFFFFF)
        self.stream <<= 8 * 3

        self.stream += (an & 0xFFFF)
        self.stream <<= 8 * 2

        self.stream += (ac1 & 0xFFFFFFFF)
        self.stream <<= 8 * 4

        self.stream += (ac2 & 0xFFFFFFFF)
        self.stream <<= 8 * 4


class Data:
    pass


class DataEnd:
    pass


class Ack:
    pass