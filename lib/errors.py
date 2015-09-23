__author__ = 'bretmattingly'


class MissingComponentsError(Exception):
    def __init__(self, mtype, required, provided):
        self.req = set(required)
        self.pro = set(provided)
        self.mtype = mtype

    def __str__(self):
        return repr("Message type " + self.mtype + " missing components: " + str(self.req - self.pro))


class UnknownTypeError(Exception):
    def __init__(self, mtype):
        self.mtype = mtype

    def __str__(self):
        return repr("Unknown message type: " + self.mtype)


class NoMessagesError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return repr("No messages available in input queue.")


class MalformedMessageError(Exception):
    def __init__(self, stream, expected_length):
        self.m = stream
        self.el = expected_length
        pass

    def __str__(self):
        return repr("Message was malformed. \nBytes:" + str(self.m) + "\nExpected length: " + self.el)