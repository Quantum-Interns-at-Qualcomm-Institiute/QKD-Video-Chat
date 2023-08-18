import socket
from ConnectionManager import ConnectionManager
from VideoStreamHandler import VideoStreamHandler
from BB84Handler import BB84Handler

class IntegratedClient:
    """
    IntegratedClient class combines the functionalities of the VideoStreamHandler and 
    ConnectionManager modules to manage video streams and server connections.

    Attributes:
    None
    """
    is_connected = False
    server_address = ('127.0.0.1', 65432)

    @classmethod
    def connect(cls) -> bool:
        """
        Attempts to establish a connection to the server using the provided connection code.
        If successful, starts the outgoing video stream. If unsuccessful, displays a placeholder.

        Parameters:
        - connection_code (str): The code to use for establishing the connection.

        Returns:
        - bool: True if the connection is successful, False otherwise.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(cls.server_address)
                cls.is_connected = True
                cls.connection_code = s.recv(1024).decode('utf-8')
                print(f"Received Connection Code: {cls.connection_code}")
            success = ConnectionManager.connectToServer(cls.connection_code)
            if success:
                VideoStreamHandler.startOutgoingStream()
            else:
                VideoStreamHandler.showPlaceholder()
            return success
        except Exception as e:
            print(f"Connection failed with error: {e}")
            raise ConnectionError(e)  

    @classmethod
    def disconnect(cls):
        """
        Stops the outgoing video stream and terminates the connection to the server.
        """
        VideoStreamHandler.stopOutgoingStream()
        ConnectionManager.disconnectFromServer()


    @classmethod
    def runBB84Protocol(cls):
        return BB84Handler.runBB84Protocol()

