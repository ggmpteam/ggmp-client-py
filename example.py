__author__ = 'bretmattingly'

from lib.client import GGMPClient

# ggwp = GGMPClient(0, ('127.0.0.1', 8080))

# ggwp.send(0x01, 0x04, 0x03)

# header
message = 0xFF

# client id
message <<= 8
message += 0x01
# message id
message <<= 8 * 4
message += 0x0000EF20
# actor id
message <<= 8
message += 0x0F
# action id
message <<= 8
message += 0x2E
# Condition 1
message <<= 8
message += 0x2E
# Condition 2
message <<= 8
message += 0x00


print(hex(message))

message2 = 0xEF20
message2 &= 0xFFFFFFFF
print(hex(message2))

message3 = 0xF3F20
message3 &= 0xFFFF
print(hex(message3))