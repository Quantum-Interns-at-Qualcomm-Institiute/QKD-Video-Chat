import unittest
from ConnectionHandler import ConnectionHandler


class TestConnectionHandler(unittest.TestCase):

    def test_generateConnectionCode(self):
        code1 = ConnectionHandler.generateConnectionCode()
        code2 = ConnectionHandler.generateConnectionCode()
        self.assertIsNotNone(code1)
        self.assertIsNotNone(code2)
        self.assertNotEqual(code1, code2)
        self.assertEqual(len(code1), 8)
        self.assertEqual(len(code2), 8)

    def test_validateConnectionCode(self):
        code = ConnectionHandler.generateConnectionCode()
        self.assertTrue(ConnectionHandler.validateConnectionCode(code))
        self.assertFalse(ConnectionHandler.validateConnectionCode(code))
        self.assertFalse(
            ConnectionHandler.validateConnectionCode("InvalidCode"))

    def test_sendReceiveData(self):
        code = ConnectionHandler.generateConnectionCode()
        sampleData = "Hello, Client!"
        self.assertTrue(ConnectionHandler.sendData(code, sampleData))
        receivedData = ConnectionHandler.receiveData(code)
        self.assertEqual(receivedData, sampleData)
        self.assertFalse(ConnectionHandler.sendData("InvalidCode", sampleData))


if __name__ == "__main__":
    unittest.main()

# import unittest

# class TestConnectionHandler(unittest.TestCase):

#     def setUp(self):
#         # Reset connection state before each test
#         ConnectionHandler.is_connected = False

#     def test_connect_with_valid_code(self):
#         success = ConnectionHandler.connect("VALID_CODE")
#         self.assertTrue(success)
#         self.assertTrue(ConnectionHandler.is_connected)

#     def test_connect_with_invalid_code(self):
#         success = ConnectionHandler.connect("INVALID_CODE")
#         self.assertFalse(success)
#         self.assertFalse(ConnectionHandler.is_connected)

#     def test_send_data_when_connected(self):
#         ConnectionHandler.connect("VALID_CODE")
#         # Ideally, we'd capture the data sent and verify it. For simplicity, we'll check connection status.
#         ConnectionHandler.sendData("Sample Data")
#         self.assertTrue(ConnectionHandler.is_connected)

#     def test_send_data_when_not_connected(self):
#         # Again, in a real-world scenario, we'd verify that the data wasn't sent.
#         # Here, we'll just check connection status.
#         ConnectionHandler.sendData("Sample Data")
#         self.assertFalse(ConnectionHandler.is_connected)

#     def test_reset_connection(self):
#         ConnectionHandler.connect("VALID_CODE")
#         ConnectionHandler.reset()
#         self.assertFalse(ConnectionHandler.is_connected)

# if __name__ == "__main__":
#     unittest.main()
