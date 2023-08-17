import unittest
from MetricsMonitor import MetricsMonitor


class TestMetricsMonitor(unittest.TestCase):

    def setUp(self):
        MetricsMonitor.data_volume = 0
        MetricsMonitor.key_exchanges = 0

    def test_addDataVolume(self):
        MetricsMonitor.addDataVolume(500)
        self.assertEqual(MetricsMonitor.getDataVolume(), 500)
        MetricsMonitor.addDataVolume(300)
        self.assertEqual(MetricsMonitor.getDataVolume(), 800)

    def test_incrementKeyExchanges(self):
        MetricsMonitor.incrementKeyExchanges()
        self.assertEqual(MetricsMonitor.getKeyExchangeRate(), 1)
        MetricsMonitor.incrementKeyExchanges()
        self.assertEqual(MetricsMonitor.getKeyExchangeRate(), 2)


if __name__ == "__main__":
    unittest.main()
