import unittest
from VideoStreamHandler import VideoStreamHandler

# # Mock implementation of VideoStreamHandler for demonstration purposes
# class VideoStreamHandler:

#     outgoing_stream_active = False
#     incoming_stream_active = False
#     placeholder_active = False

#     @classmethod
#     def startOutgoingStream(cls):
#         cls.outgoing_stream_active = True

#     @classmethod
#     def stopOutgoingStream(cls):
#         cls.outgoing_stream_active = False

#     @classmethod
#     def startIncomingStream(cls):
#         cls.incoming_stream_active = True

#     @classmethod
#     def stopIncomingStream(cls):
#         cls.incoming_stream_active = False

#     @classmethod
#     def showPlaceholder(cls):
#         cls.placeholder_active = True

#     @classmethod
#     def hidePlaceholder(cls):
#         cls.placeholder_active = False


class TestVideoStreamHandler(unittest.TestCase):

    def test_outgoingStream(self):
        VideoStreamHandler.startOutgoingStream()
        self.assertTrue(VideoStreamHandler.outgoing_stream_active)
        VideoStreamHandler.stopOutgoingStream()
        self.assertFalse(VideoStreamHandler.outgoing_stream_active)

    def test_incomingStream(self):
        VideoStreamHandler.startIncomingStream()
        self.assertTrue(VideoStreamHandler.incoming_stream_active)
        VideoStreamHandler.stopIncomingStream()
        self.assertFalse(VideoStreamHandler.incoming_stream_active)

    def test_placeholder(self):
        VideoStreamHandler.showPlaceholder()
        self.assertTrue(VideoStreamHandler.placeholder_active)
        VideoStreamHandler.hidePlaceholder()
        self.assertFalse(VideoStreamHandler.placeholder_active)


if __name__ == "__main__":
    unittest.main()
