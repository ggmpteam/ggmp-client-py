__author__ = 'bretmattingly'


class Action:
    def __init__(self, ACK, cl, mid, ar, an, ac1, ac2):
        self.ack = ACK
        self.cl = cl
        self.mid = mid
        self.ar = ar
        self.an = an
        self.ac1 = ac1
        self.ac2 = ac2

        self.stream = bytearray([0x00]) if ACK else bytearray([0x01])
        self.stream.extend((cl & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((mid & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ar & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((an & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ac1 & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ac2 & 0xFFFFFFFF).to_bytes(4, "big", signed=False))


class ActionShort:
    def __init__(self, ACK, cl, mid, ar, an, ac1, ac2):
        self.ack = ACK
        self.cl = cl
        self.mid = mid
        self.ar = ar
        self.an = an
        self.ac1 = ac1
        self.ac2 = ac2

        self.stream = bytearray([0x02]) if ACK else bytearray([0x03])
        self.stream.extend((cl & 0xFF).to_bytes(1, "big", signed=False))
        self.stream.extend((mid & 0xFFFF).to_bytes(2, "big", signed=False))
        self.stream.extend((ar & 0xFF).to_bytes(1, "big", signed=False))
        self.stream.extend((an & 0xFF).to_bytes(1, "big", signed=False))
        self.stream.extend((ac1 & 0xFF).to_bytes(1, "big", signed=False))
        self.stream.extend((ac2 & 0xFF).to_bytes(1, "big", signed=False))


class ActionExtended:
    def __init__(self, ACK, cl, mid, ar, an, ac1, ac2):
        self.ack = ACK
        self.cl = cl
        self.mid = mid
        self.ar = ar
        self.an = an
        self.ac1 = ac1
        self.ac2 = ac2

        self.stream = bytearray([0x04]) if ACK else bytearray([0x05])
        self.stream.extend((cl & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((mid & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ar & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((an & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ac1 & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((ac2 & 0xFFFFFFFF).to_bytes(4, "big", signed=False))


class Data:
    def __init__(self, ACK, cl, mid, pmsg, siz, dat):
        self.ack = ACK
        self.cl = cl
        self.mid = mid
        self.pmsg = pmsg
        self.siz = siz
        self.dat = dat
        self.stream = bytearray([0x0E]) if ACK else bytearray([0x0F])
        self.stream.extend((cl & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((mid & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((pmsg & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((siz & 0xFFFFFFFF).to_bytes(1, "big", signed=False))
        self.stream.extend(dat)


class DataEnd:
    def __init__(self, ACK, cl, mid, pmsg, siz, dat):
        self.ack = ACK
        self.cl = cl
        self.mid = mid
        self.pmsg = pmsg
        self.siz = siz
        self.dat = dat
        self.stream = bytearray([0x0E]) if ACK else bytearray([0x0F])
        self.stream.extend((cl & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((mid & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((pmsg & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((siz & 0xFFFFFFFF).to_bytes(1, "big", signed=False))
        self.stream.extend(dat)


class Ack:
    def __init__(self, cl, mid, pmsg):
        self.cl = cl
        self.mid = mid
        self.pmsg = pmsg
        self.stream = bytearray([0xFF])
        self.stream.extend((cl & 0xFFFFFF).to_bytes(3, "big", signed=False))
        self.stream.extend((mid & 0xFFFFFFFF).to_bytes(4, "big", signed=False))
        self.stream.extend((pmsg & 0xFFFFFFFF).to_bytes(4, "big", signed=False))