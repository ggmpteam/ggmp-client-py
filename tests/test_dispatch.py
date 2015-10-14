__author__ = 'bretmattingly'
import sys
sys.path.append('..')
import unittest
from lib import dispatch
from lib import messages
from lib import errors
from lib.decoding import decode as message_decode


class TestDispatch(unittest.TestCase):

    def setUp(self):
        self.dispatch = dispatch.Dispatch(0, ("0.0.0.0", 12358))

    def test_awaitbox_add(self):
        self.dispatch.awaitbox.buckets[0][0] = messages.Action(True, 0, 0, 15, 13, 420, 8008)
        self.assertEqual(len(self.dispatch.awaitbox.buckets[0]), 1)

    def test_awaitbox_shift(self):
        self.dispatch.awaitbox.buckets[0][0] = messages.Action(True, 0, 0, 15, 13, 420, 8008)
        lost = self.dispatch.awaitbox.shift()
        self.assertEqual(len(self.dispatch.awaitbox.buckets[0]), 0)
        self.assertEqual(len(self.dispatch.awaitbox.buckets[1]), 1)
        self.assertEqual(len(lost), 0)

    def test_awaitbox_fullshift(self):
        self.dispatch.awaitbox.buckets[0][0] = messages.Action(True, 0, 0, 15, 13, 420, 8008)
        self.dispatch.awaitbox.buckets[1][11] = messages.Action(True, 0, 11, 17, 13, 420, 8008)
        self.dispatch.awaitbox.buckets[2][13] = messages.Action(True, 0, 13, 19, 220, 420, 8008)
        lost = self.dispatch.awaitbox.shift()
        self.assertEqual(len(self.dispatch.awaitbox.buckets[0]), 0, msg='{0}'.format(self.dispatch.awaitbox.buckets[0]))
        self.assertEqual(len(self.dispatch.awaitbox.buckets[1]), 1, msg='{0}'.format(self.dispatch.awaitbox.buckets[1]))
        self.assertEqual(len(self.dispatch.awaitbox.buckets[2]), 1, msg='{0}'.format(self.dispatch.awaitbox.buckets[2]))
        self.assertEqual(len(lost), 1, msg='{0}'.format(lost))

    def tearDown(self):
        self.dispatch.threader.sock.close()







