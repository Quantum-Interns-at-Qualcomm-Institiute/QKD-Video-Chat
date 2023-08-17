import socket
from ConnectionHandler import ConnectionHandler
from MetricsMonitor import MetricsMonitor
from EavesdropperDetector import EavesdropperDetector

class IntegratedServer:
    """
    IntegratedServer class integrates the ConnectionHandler, MetricsMonitor, and 
    EavesdropperDetector modules to create a cohesive server system for managing 
    client connections, monitoring metrics, and detecting eavesdropping.

    Attributes:
    - is_connected (bool): Indicates if a client is currently connected.
    """

    is_connected = False
    HOST = '127.0.0.1'
    PORT = 65432

    @classmethod
    def connect(cls, connection_code: str) -> bool:
        """
        Establishes a connection using the ConnectionHandler.

        Parameters:
        - connection_code (str): The code to use for establishing the connection.

        Returns:
        - bool: True if the connection is successful, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((cls.HOST, cls.PORT))
            s.listen()
            print("Server is waiting for client connection...")
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                cls.is_connected = True
                conn.sendall(connection_code.encode('utf-8'))

    @classmethod
    def sendData(cls, data: str):
        """
        Sends data and updates the MetricsMonitor with the data volume.

        Parameters:
        - data (str): Data to be sent.
        """
        ConnectionHandler.sendData(data)
        MetricsMonitor.addDataVolume(len(data))

    @classmethod
    def runBB84Protocol(cls):
        """
        Executes the BB84 protocol and checks for eavesdropping.
        Updates the MetricsMonitor with the key exchange count.
        Resets the connection if eavesdropping is detected.
        """
        EavesdropperDetector.runBB84Protocol()
        MetricsMonitor.incrementKeyExchanges()

        if EavesdropperDetector.detectEavesdropping():
            cls.reset()

    @classmethod
    def reset(cls):
        """
        Resets the connection.
        """
        ConnectionHandler.reset()
        cls.is_connected = False
