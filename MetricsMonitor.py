class MetricsMonitor:
    """
    MetricsMonitor class manages and tracks metrics related to data exchange and key exchanges.

    Attributes:
    - data_volume (int): Total volume of data exchanged (in bytes).
    - key_exchanges (int): Count of key exchanges that have occurred.
    """

    data_volume = 0
    key_exchanges = 0

    @classmethod
    def addDataVolume(cls, volume: int):
        """
        Increment the data volume by a specified amount.

        Parameters:
        - volume (int): Amount of data (in bytes) to add to the total volume.
        """
        cls.data_volume += volume

    @classmethod
    def getDataVolume(cls) -> int:
        """
        Retrieve the current total volume of data exchanged.

        Returns:
        - int: Total volume of data exchanged.
        """
        return cls.data_volume

    @classmethod
    def incrementKeyExchanges(cls):
        """
        Increment the count of key exchanges by one.
        """
        cls.key_exchanges += 1

    @classmethod
    def getKeyExchangeRate(cls) -> int:
        """
        Retrieve the current count of key exchanges.

        Returns:
        - int: Count of key exchanges that have occurred.
        """
        return cls.key_exchanges
