import unittest
from VideoStreamHandler import VideoStreamHandler
from ConnectionManager import ConnectionManager
# Assuming the modules are imported and available for use
# from client_modules import VideoStreamHandler, ConnectionManager


class IntegratedClient:
    @classmethod
    def connect(cls, connection_code: str) -> bool:
        success = ConnectionManager.connectToServer(connection_code)
        if success:
            VideoStreamHandler.startOutgoingStream()
        else:
            VideoStreamHandler.showPlaceholder()
        return success

    @classmethod
    def disconnect(cls):
        VideoStreamHandler.stopOutgoingStream()
        ConnectionManager.disconnectFromServer()


class TestClientIntegration(unittest.TestCase):

    def setUp(self):
        # Reset the states before each test
        VideoStreamHandler.outgoing_stream_active = False
        VideoStreamHandler.placeholder_active = False
        ConnectionManager.is_connected = False

    def test_successful_connection_starts_video_stream(self):
        success = IntegratedClient.connect("VALID_CODE")
        self.assertTrue(success)
        self.assertTrue(VideoStreamHandler.outgoing_stream_active)

    def test_failed_connection_shows_placeholder(self):
        success = IntegratedClient.connect("INVALID_CODE")
        self.assertFalse(success)
        self.assertTrue(VideoStreamHandler.placeholder_active)

    def test_disconnect_stops_video_stream(self):
        IntegratedClient.connect("VALID_CODE")
        IntegratedClient.disconnect()
        self.assertFalse(VideoStreamHandler.outgoing_stream_active)


if __name__ == "__main__":
    unittest.main()
