import unittest
from unittest.mock import Mock

# Assuming the modules are imported and available for use
from ConnectionHandler import ConnectionHandler
from MetricsMonitor import MetricsMonitor
from EavesdropperDetector import EavesdropperDetector
from IntegratedServer import IntegratedServer

class TestServerIntegration(unittest.TestCase):
    def setUp(self):
        self.connection_handler = Mock()
        self.metrics_monitor = Mock()
        self.eavesdropper_detector = Mock()
        self.data_transfer = Mock()
        self.connection_validator = Mock()
        self.stream_manager = Mock()

    def test_successful_connection_and_data_exchange(self):
        # Create a real instance of ConnectionHandler
        connection_handler = ConnectionHandler(self.metrics_monitor, self.eavesdropper_detector)

        # Simulate a client connecting with a valid connection code
        code = "VALID_CODE"
        connected = connection_handler.connect(code)
        self.assertTrue(connected)

        # Simulate data exchange and check metrics
        data = "Sample Data"
        connection_handler.sendData(code, data)
        self.assertEqual(self.metrics_monitor.getDataVolume(), len(data))

    def test_eavesdropping_detection_and_reset(self):
        # Simulate a client connecting with a valid connection code
        self.connection_handler.connect.return_value = True
        self.connection_handler.connect("VALID_CODE")

        # Simulate key exchange with eavesdropping and detection
        self.eavesdropper_detector.key_sequence = [1, 1, 1, 0, 0, 0, 0, 0]
        self.eavesdropper_detector.detectEavesdropping.return_value = True
        eavesdropping_detected = self.eavesdropper_detector.detectEavesdropping()
        self.assertTrue(eavesdropping_detected)

        # Connection should be reset
        self.connection_handler.reset.return_value = None
        self.connection_handler.reset()
        self.connection_handler.is_connected.return_value = False
        self.assertFalse(self.connection_handler.is_connected)

if __name__ == "__main__":
    unittest.main()
