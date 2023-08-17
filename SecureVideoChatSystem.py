class SecureVideoChatSystem:
    """
    SecureVideoChatSystem class integrates the functionalities of the IntegratedServer 
    and IntegratedClient modules to facilitate secure video chat through quantum key 
    distribution and eavesdropping detection.

    Attributes:
    - server (IntegratedServer): Instance of the integrated server module.
    - client (IntegratedClient): Instance of the integrated client module.
    """

    def __init__(self):
        self.server = IntegratedServer
        self.client = IntegratedClient

    def clientConnect(self, connection_code: str) -> bool:
        """
        Allows the client to attempt a connection to the server.

        Parameters:
        - connection_code (str): The code used to establish the connection.

        Returns:
        - bool: True if the connection is successful, False otherwise.
        """
        return self.client.connect(connection_code)

    def executeBB84Protocol(self):
        """
        Executes the BB84 protocol on both the server and client sides for secure 
        key exchange. If eavesdropping is detected, the server resets the connection.
        """
        self.server.runBB84Protocol()
        self.client.runBB84Protocol()

        # Check for eavesdropping
        if EavesdropperDetector.detectEavesdropping():
            self.server.reset()

    def clientDisconnect(self):
        """
        Allows the client to disconnect from the server, stopping the video stream.
        """
        self.client.disconnect()
