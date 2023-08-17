import unittest
from EavesdropperDetector import EavesdropperDetector

# # Mock implementation of EavesdropperDetector for demonstration purposes
# class EavesdropperDetector:

#     key_sequence = []

#     @classmethod
#     def executeBB84(cls):
#         # This is a mock implementation; in reality, this would involve quantum mechanics
#         # For simplicity, we generate a random binary sequence
#         import random
#         cls.key_sequence = [random.choice([0, 1]) for _ in range(8)]

#     @classmethod
#     def detectEavesdropping(cls):
#         # Mock implementation: let's say if we have more than 2 '1's in sequence, it's eavesdropped
#         return cls.key_sequence.count(1) > 2

#     @classmethod
#     def alertUser(cls):
#         # In a real-world application, this would involve some GUI or notification mechanism
#         # For simplicity, we just print an alert
#         print("Eavesdropping detected!")


class TestEavesdropperDetector(unittest.TestCase):

    def test_executeBB84(self):
        EavesdropperDetector.runBB84Protocol()
        self.assertEqual(len(EavesdropperDetector.key_sequence), 8)

    def test_detectEavesdropping(self):
        EavesdropperDetector.key_sequence = [0, 0, 0, 0, 0, 0, 0, 0]
        self.assertFalse(EavesdropperDetector.detectEavesdropping())

        EavesdropperDetector.key_sequence = [1, 1, 1, 0, 0, 0, 0, 0]
        self.assertTrue(EavesdropperDetector.detectEavesdropping())


if __name__ == "__main__":
    unittest.main()
