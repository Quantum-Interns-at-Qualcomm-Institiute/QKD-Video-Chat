import unittest
from ConnectionManager import ConnectionManager

# # Mock implementation of ConnectionManager for demonstration purposes
# class ConnectionManager:

#     is_connected = False

#     @classmethod
#     def connectToServer(cls, connection_code: str) -> bool:
#         # This is a mock implementation; in reality, this would involve actual connection mechanisms
#         if connection_code == "VALID_CODE":
#             cls.is_connected = True
#             return True
#         else:
#             return False

#     @classmethod
#     def reconnectToServer(cls) -> bool:
#         # This is a mock implementation
#         if not cls.is_connected:
#             cls.is_connected = True
#             return True
#         return False

#     @classmethod
#     def disconnectFromServer(cls):
#         cls.is_connected = False


class TestConnectionManager(unittest.TestCase):

    def test_connectToServer(self):
        self.assertTrue(ConnectionManager.connectToServer("VALID_CODE"))
        self.assertFalse(ConnectionManager.connectToServer("INVALID_CODE"))

    def test_reconnectToServer(self):
        ConnectionManager.disconnectFromServer()
        self.assertTrue(ConnectionManager.reconnectToServer())
        self.assertTrue(ConnectionManager.is_connected)

    def test_disconnectFromServer(self):
        ConnectionManager.connectToServer("VALID_CODE")
        ConnectionManager.disconnectFromServer()
        self.assertFalse(ConnectionManager.is_connected)


if __name__ == "__main__":
    unittest.main()
