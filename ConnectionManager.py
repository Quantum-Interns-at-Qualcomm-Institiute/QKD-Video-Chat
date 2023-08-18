class ConnectionValidator:
    def validateConnection(cls, connection_code: str) -> bool:
        if connection_code == "VALID_CODE":
            return True
        else:
            return False
        

class ConnectionManager:
    """
    ConnectionManager class manages the connection to the server, including 
    establishing, re-establishing, and terminating the connection.

    Attributes:
    - is_connected (bool): Indicates if a connection to the server is currently active.
    """

    is_connected = False

    @classmethod
    def connectToServer(cls, connection_code: str) -> bool:
        """
        Initiates a connection to the server using the provided connection code.

        Note: This is a mock implementation. In a real-world scenario, this would involve 
              actual network connection mechanisms.

        Parameters:
        - connection_code (str): The code to use for establishing the connection.

        Returns:
        - bool: True if the connection is successful, False otherwise.
        """
        if connection_code == "VALID_CODE":
            cls.is_connected = True
            return True
        else:
            return False

    @classmethod
    def reconnectToServer(cls) -> bool:
        """
        Attempts to re-establish a connection to the server if it was lost.

        Note: This is a mock implementation. In a real-world scenario, this would involve 
              actual network reconnection mechanisms.

        Returns:
        - bool: True if the reconnection is successful, False otherwise.
        """
        if not cls.is_connected:
            cls.is_connected = True
            return True
        return False

    @classmethod
    def disconnectFromServer(cls):
        """
        Terminates the connection to the server.

        Note: This is a mock implementation. In a real-world scenario, this would involve 
              gracefully terminating network connections.
        """
        cls.is_connected = False
