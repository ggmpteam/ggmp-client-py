__author__ = 'bretmattingly'

from lib.messages import *
from lib.client import GGMPClient, Message
from lib.errors import *

ggwp = GGMPClient(1, ('127.0.0.1', 12358))

# This will work
ggwp.build_message(Message.Action, True, ar=1, an=3)

# This won't. We need an action!
try:
    ggwp.build_message(Message.Action, True, ar=2, ac1=2)
except MissingComponentsError as e:
    print(e)

ggwp.build_message(Message.Action, True, ar=2, an=14, ac1=244)
ggwp.send_all()

ggwp.build_message(Message.DataEnd, True, pmsg=1, dat=bytes("tacos.", "utf-8"), siz=len(bytes("tacos.", "utf-8")))
ggwp.send_all()
while True:
    try:
        m = ggwp.try_read()
        print(type(m))
        if type(m) == DataEnd:
            decoded = m.dat.to_bytes((m.dat.bit_length() + 7) // 8, 'big') or b'\0'
            decoded = decoded.decode()
            print(decoded)
    except NoMessagesError as e:
        print("All out of messages.")
        exit(0)

