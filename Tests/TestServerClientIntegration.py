import unittest

# Assuming the modules are imported and available for use
from IntegratedServer import IntegratedServer
from IntegratedClient import IntegratedClient
from EavesdropperDetector import EavesdropperDetector
from VideoStreamHandler import VideoStreamHandler
from ConnectionManager import ConnectionManager

class TestServerClientIntegration(unittest.TestCase):

    def setUp(self):
        # Reset states before each test
        IntegratedServer.reset()
        VideoStreamHandler.outgoing_stream_active = False
        VideoStreamHandler.placeholder_active = False
        ConnectionManager.is_connected = False

    def test_successful_key_exchange_and_connection(self):
        # Client attempts to connect to the server
        success = IntegratedClient.connect("VALID_CODE")
        self.assertTrue(success)

        # Server and client proceed with BB84 protocol
        IntegratedServer.runBB84Protocol()
        IntegratedClient.runBB84Protocol()

        # Check if eavesdropping was detected
        eavesdropping_detected = EavesdropperDetector.detectEavesdropping()
        self.assertFalse(eavesdropping_detected)

        # Check if client video stream is active
        self.assertTrue(VideoStreamHandler.outgoing_stream_active)

    def test_eavesdropping_detection_and_reset(self):
        # Simulate eavesdropping by setting a suspicious key sequence
        EavesdropperDetector.key_sequence = [1, 1, 1, 0, 0, 0, 0, 0]

        # Client attempts to connect to the server
        IntegratedClient.connect("VALID_CODE")

        # Server and client proceed with BB84 protocol
        IntegratedServer.runBB84Protocol()
        IntegratedClient.runBB84Protocol()

        # Check if eavesdropping was detected and connection reset
        eavesdropping_detected = EavesdropperDetector.detectEavesdropping()
        self.assertTrue(eavesdropping_detected)
        self.assertFalse(ConnectionManager.is_connected)

        # Client should show placeholder
        self.assertTrue(VideoStreamHandler.placeholder_active)


if __name__ == "__main__":
    unittest.main()
