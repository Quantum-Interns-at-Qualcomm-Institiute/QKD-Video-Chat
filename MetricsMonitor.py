class MetricsMonitor:
    """
    MetricsMonitor class manages and tracks metrics related to data exchange and key exchanges.

    Attributes:
    - data_volume (int): Total volume of data exchanged (in bytes).
    - key_exchanges (int): Count of key exchanges that have occurred.
    """
    
    def __init__(self):
        self.data_volume = 0
        self.key_exchanges = 0 # Temp in place of actual key rate

    def addDataVolume(self, volume: int):
        """
        Increment the data volume by a specified amount.

        Parameters:
        - volume (int): Amount of data (in bytes) to add to the total volume.
        """
        self.data_volume += volume

    def getDataVolume(self) -> int:
        """
        Retrieve the current total volume of data exchanged.

        Returns:
        - int: Total volume of data exchanged.
        """
        return self.data_volume

    def incrementKeyExchanges(self):
        """
        Increment the count of key exchanges by one. Temporary for now
        """
        self.key_exchanges += 1

    def getKeyExchangeRate(self) -> int:
        """
        Retrieve the speed with which keys are being exchanged

        Returns:
        - int: Count for MB/s 
        """
        return self.key_exchanges # Temp just returns how MANY exchanges