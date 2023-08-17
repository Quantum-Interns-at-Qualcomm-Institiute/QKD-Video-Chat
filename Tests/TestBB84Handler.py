import unittest
from BB84Handler import BB84Handler

# # Mock implementation of BB84Handler for demonstration purposes
# class BB84Handler:

#     key_sequence = []

#     @classmethod
#     def runBB84Protocol(cls):
#         # This is a mock implementation; in reality, this would involve quantum mechanics
#         # For simplicity, we generate a random binary sequence as the key
#         import random
#         cls.key_sequence = [random.choice([0, 1]) for _ in range(8)]

#     @classmethod
#     def getQuantumKey(cls):
#         return cls.key_sequence

#     @classmethod
#     def detectEavesdropping(cls):
#         # Mock implementation: let's say if we have more than 2 '1's in sequence, it's eavesdropped
#         return cls.key_sequence.count(1) > 2


class TestBB84Handler(unittest.TestCase):

    def test_runBB84Protocol_and_getQuantumKey(self):
        BB84Handler.runBB84Protocol()
        key = BB84Handler.getQuantumKey()
        self.assertEqual(len(key), 8)

    def test_detectEavesdropping(self):
        BB84Handler.key_sequence = [0, 0, 0, 0, 0, 0, 0, 0]
        self.assertFalse(BB84Handler.detectEavesdropping())

        BB84Handler.key_sequence = [1, 1, 1, 0, 0, 0, 0, 0]
        self.assertTrue(BB84Handler.detectEavesdropping())


if __name__ == "__main__":
    unittest.main()
