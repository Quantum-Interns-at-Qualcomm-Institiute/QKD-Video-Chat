import socket
from ConnectionHandler import ConnectionHandler
from MetricsMonitor import MetricsMonitor
from EavesdropperDetector import EavesdropperDetector

class SocketHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def listen_for_connection(self):
        self.socket.listen()
        print("Server is waiting for client connection...")
        self.conn, self.addr = self.socket.accept()
        print('Connected by', self.addr)

    def send_connection_code(self, connection_code):
        self.conn.sendall(connection_code.encode('utf-8'))

class IntegratedServer:
    """
    IntegratedServer class integrates the ConnectionHandler, MetricsMonitor, and 
    EavesdropperDetector modules to create a cohesive server system for managing 
    client connections, monitoring metrics, and detecting eavesdropping.

    Attributes:
    - is_connected (bool): Indicates if a client is currently connected.
    """

    def __init__(self, socket_handler, metrics_monitor, eavesdropper_detector):
        self.socket_handler = socket_handler
        self.metrics_monitor = metrics_monitor
        self.eavesdropper_detector = eavesdropper_detector

    
    def connect(self, connection_code: str):
        """
        Establishes a connection using the ConnectionHandler.

        Parameters:
        - connection_code (str): The code to use for establishing the connection.

        Returns:
        - bool: True if the connection is successful, False otherwise. # Actually not rn
        """
        self.socket_handler.create_socket()
        self.socket_handler.listen_for_connection()
        self.socket_handler.send_connection_code(connection_code)

    
    def sendData(self, data: str):
        """
        Sends data and updates the MetricsMonitor with the data volume.

        Parameters:
        - data (str): Data to be sent.
        """
        ConnectionHandler.sendData(data)
        MetricsMonitor.addDataVolume(len(data))

    
    def runBB84Protocol(self):
        """
        Executes the BB84 protocol and checks for eavesdropping.
        Updates the MetricsMonitor with the key exchange count.
        Resets the connection if eavesdropping is detected.
        """
        EavesdropperDetector.runBB84Protocol()
        MetricsMonitor.incrementKeyExchanges()

        if EavesdropperDetector.detectEavesdropping():
            self.reset()

    
    def reset(self):
        """
        Resets the connection.
        """
        ConnectionHandler.reset()
        self.is_connected = False
