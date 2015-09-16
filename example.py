__author__ = 'bretmattingly'

from lib.client import GGMPClient, Message
from lib.errors import *

ggwp = GGMPClient(0, ('127.0.0.1', 8080))

# This will work
ggwp.build_message(Message.Action, True, ar=1, an=3)

# This won't. We need an action!
try:
    ggwp.build_message(Message.Action, True, ar=2, ac1=2)
except MissingComponentsError as e:
    print(e)