__author__ = 'bretmattingly'
from . import messages
from . import errors
from enum import Enum
from .dispatch import Dispatch


class GGMPClient:
    """The primary class exported by the library.

    GGMPClient is designed to be an "automatic" client. Upon creation
    it will spawn two threads, `inbox` and `outbox`, which are
    responsible for the listening and sending of messages.
    """
    def __init__(self, c_id, ip_addr, use_message_ids=True):
        """Constructor


        :param c_id: Client ID. This must be received from the server (generally via another protocol)
        :param ip_addr: IP Address of the server to connect to. Must be tuple of the form (IPv4/v6, Port)
        :param use_message_ids: Whether or not to use Message IDs. Defaults to true.
        :return:
        """
        self.client_id = c_id
        self.use_message_ids = use_message_ids
        self.message_id = 0x000000
        self._dispatch = Dispatch(c_id, ip_addr)

        # Todo: Sanity checks

    def send_all(self):
        """
        Send all messages queued
        :return:
        """
        self._dispatch.send_all()

    def try_read(self):
        """Non-blocking read.

        Raises `NoMessagesError` if no messages available.
        :return:
        """
        try:
            m = self._dispatch.try_read()
        except errors.NoMessagesError:
            return None
        print("Received message: " + str(m))
        return m

    def build_message(self, mtype, ack=False, **kwargs):
        """Builds and enqueues a GGMP message
        This method is used to build any Game State Message Type. Upon
        successful message creation, the message is enqueued in the
        GGMPClient's outbox, and can be sent with a `send()` call or automatically

        :param mtype: Message type. See documentation on `Message` for details.
        :param ack: Whether or not to require an Ack for this message.
        :param kwargs: Values of Components
        :return:
        """
        if mtype == Message.Action:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("Action", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.Action(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        elif mtype == Message.ActionShort:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("ActionShort", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.ActionShort(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        elif mtype == Message.ActionExtended:
            if {"ar", "an"} - set(kwargs):
                raise errors.MissingComponentsError("ActionExtended", ["ar", "an"], kwargs)
            else:
                ac1 = kwargs["ac1"] if "ac1" in kwargs else 0x00
                ac2 = kwargs["ac2"] if "ac2" in kwargs else 0x00
                m = messages.ActionExtended(ack, self.client_id, self.message_id, kwargs["ar"], kwargs["an"], ac1, ac2)

        else:
            raise errors.UnknownTypeError(type)

        self.message_id += 1
        self._dispatch.add_message(m)


class Message(Enum):
    Action = 1
    ActionShort = 2
    ActionExtended = 3
    Data = 4
    DataEnd = 5
    Ack = 6
