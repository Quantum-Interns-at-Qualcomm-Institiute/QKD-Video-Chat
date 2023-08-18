import unittest
import threading
from IntegratedServer import IntegratedServer
from VideoStreamHandler import VideoStreamHandler
from ConnectionManager import ConnectionManager
from IntegratedClient import IntegratedClient

class TestServerClientConnection(unittest.TestCase):

    def setUp(self):
        # Reset states before each test
        IntegratedServer.reset()
        VideoStreamHandler.outgoing_stream_active = False
        VideoStreamHandler.placeholder_active = False
        ConnectionManager.is_connected = False
        
        self.server_thread = threading.Thread(target=IntegratedServer.connect, args=("VALID_CODE",))
        self.server_thread.start()

    def tearDown(self):
      IntegratedServer.reset()
      self.server_thread.join()
    
    def test_server_waiting_for_connection(self):
        self.assertFalse(IntegratedServer.is_connected)
        IntegratedServer.connect("VALID_CODE")
        self.assertTrue(IntegratedServer.is_connected)

    def test_client_receives_unique_connection_code(self):
        IntegratedClient.server_address = ('localhost', 65432)  
        success = IntegratedClient.connect()
        self.assertTrue(success)
        self.assertIsNotNone(IntegratedClient.connection_code)
        self.assertEqual(len(IntegratedClient.connection_code), 8)

    def test_connection_failure_handled_gracefully(self):
        IntegratedClient.server_address = ('localhost', 9999)  # Non-listening port
        with self.assertRaises(ConnectionError):
            IntegratedClient.connect()