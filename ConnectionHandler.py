import string
import random


class ConnectionHandler:
    """
    ConnectionHandler class manages client connections and generates codes for clients to connect.

    Attributes:
    - active_codes (set): A set to store currently active connection codes.
    """

    active_codes = set()
    is_connected = False

    @classmethod
    def generateConnectionCode(cls):
        """
        Generates a unique 8-character alphanumeric connection code.

        Returns:
        - str: The generated connection code.
        """
        while True:
            code = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for _ in range(8))
            if code not in cls.active_codes:
                cls.active_codes.add(code)
                return code

    @classmethod
    def validateConnectionCode(cls, code):
        """
        Validates the provided connection code. If valid, deactivates the code to prevent reuse.

        Parameters:
        - code (str): The connection code to validate.

        Returns:
        - bool: True if the code is valid and active, False otherwise.
        """
        if code in cls.active_codes:
            cls.active_codes.remove(code)
            return True
        return False

    @classmethod
    def sendData(cls, code, data):
        """
        Sends data to the designated client using the provided connection code.

        Parameters:
        - code (str): The connection code.
        - data (str): The data to send.

        Returns:
        - bool: True if data was successfully sent, False if the connection code is not valid or active.
        """
        # In this mock implementation, we simply check the validity of the code.
        # In a real-world application, this method would involve actual data transfer mechanisms.
        return code in cls.active_codes

    @classmethod
    def receiveData(cls, code):
        """
        Receives data from the designated client using the provided connection code.

        Parameters:
        - code (str): The connection code.

        Returns:
        - str: Received data if the connection code is valid and active, None otherwise.
        """
        # In this mock implementation, we return a sample message if the code is valid.
        # In a real-world application, this method would involve actual data transfer mechanisms.
        if code in cls.active_codes:
            return "Hello, Client!"
        return None

# class ConnectionHandler:
#     """
#     ConnectionHandler manages client connections and generates codes for clients to connect.

#     Attributes:
#     - is_connected (bool): Indicates if a client is currently connected.
#     - connection_codes (list): List of valid connection codes.
#     """

    @classmethod
    def connect(cls, connection_code: str) -> bool:
        """
        Attempts to establish a connection using a given connection code.

        Parameters:
        - connection_code (str): The code to use for establishing the connection.

        Returns:
        - bool: True if the connection is successful, False otherwise.
        """
        if connection_code in cls.active_codes:
            cls.is_connected = True
            return True
        return False

#     @classmethod
#     def sendData(cls, data: str):
#         """
#         Sends data to a connected client.

#         Parameters:
#         - data (str): Data to be sent.
#         """
#         if cls.is_connected:
#             # Here, logic to send data would be implemented. For now, we'll just pass.
#             pass

    @classmethod
    def reset(cls):
        """
        Resets the connection.
        """
        cls.is_connected = False
