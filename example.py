__author__ = 'bretmattingly'

from lib.client import GGMPClient, Message
from lib.errors import *
from queue import Empty

ggwp = GGMPClient(1, ('127.0.0.1', 8080))

# This will work
ggwp.build_message(Message.Action, True, ar=1, an=3)

# This won't. We need an action!
try:
    ggwp.build_message(Message.Action, True, ar=2, ac1=2)
except MissingComponentsError as e:
    print(e)

while True:
    try:
        ggwp.try_read()
    except Empty as e:
        pass

