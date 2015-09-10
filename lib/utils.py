__author__ = 'bretmattingly'


def append_hex(a, b):
        sizeof_b = 0

        # get size of b in bits
        while((b >> sizeof_b) > 0):
            sizeof_b += 1

        # align answer to nearest 4 bits (hex digit)
        sizeof_b += sizeof_b % 4

        return (a << sizeof_b) | b
