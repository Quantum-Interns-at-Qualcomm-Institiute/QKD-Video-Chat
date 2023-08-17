import unittest

# Assuming the modules are imported and available for use
from ConnectionHandler import ConnectionHandler
from MetricsMonitor import MetricsMonitor
from EavesdropperDetector import EavesdropperDetector


class TestServerIntegration(unittest.TestCase):

    def setUp(self):
        # Reset all modules to default states before each test
        ConnectionHandler.reset()
        MetricsMonitor.data_volume = 0
        MetricsMonitor.key_exchanges = 0
        EavesdropperDetector.key_sequence = []

    def test_successful_connection_and_data_exchange(self):
        code = "VALID_CODE"
        # Simulate a client connecting with a valid connection code
        connected = ConnectionHandler.connect(code)
        # self.assertTrue(connected)
        # Simulate data exchange and check metrics
        returnv = ConnectionHandler.sendData(code, "Sample Data")
        self.assertEqual(MetricsMonitor.getDataVolume(), len("Sample Data"))

        # Simulate key exchange and eavesdropping detection
        EavesdropperDetector.runBB84Protocol()
        MetricsMonitor.incrementKeyExchanges()
        eavesdropping_detected = EavesdropperDetector.detectEavesdropping()
        self.assertFalse(eavesdropping_detected)
        self.assertEqual(MetricsMonitor.getKeyExchangeRate(), 1)

    def test_eavesdropping_detection_and_reset(self):
        # Simulate a client connecting with a valid connection code
        ConnectionHandler.connect("VALID_CODE")

        # Simulate key exchange with eavesdropping and detection
        EavesdropperDetector.key_sequence = [1, 1, 1, 0, 0, 0, 0, 0]
        eavesdropping_detected = EavesdropperDetector.detectEavesdropping()
        self.assertTrue(eavesdropping_detected)

        # Connection should be reset
        ConnectionHandler.reset()
        self.assertFalse(ConnectionHandler.is_connected)


if __name__ == "__main__":
    unittest.main()
