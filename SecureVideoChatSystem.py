from EavesdropperDetector import EavesdropperDetector

class EavesdroppingChecker:
    def __init__(self, eavesdropper_detector):
        self.eavesdropper_detector = eavesdropper_detector

    def check_for_eavesdropping(self):
        return self.eavesdropper_detector.detectEavesdropping()

class SecureVideoChatSystem:
    """
    SecureVideoChatSystem class integrates the functionalities of the IntegratedServer 
    and IntegratedClient modules to facilitate secure video chat through quantum key 
    distribution and eavesdropping detection.

    Attributes:
    - server (IntegratedServer): Instance of the integrated server module.
    - client (IntegratedClient): Instance of the integrated client module.
    """

    def __init__(self, server, client, eavesdropping_checker):
        self.server = server
        self.client = client
        self.eavesdropping_checker = eavesdropping_checker

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
        eavesdropping_detected = self.eavesdropping_checker.check_for_eavesdropping()
        if eavesdropping_detected:
            print("Eavesdropping detected!")

    def clientDisconnect(self):
        """
        Allows the client to disconnect from the server, stopping the video stream.
        """
        self.client.disconnect()
