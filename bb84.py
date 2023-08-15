from abc import ABC, abstractmethod
import sys
import unittest
from qiskit import QuantumCircuit, Aer, execute
import random


class QuantumBitGenerator:
    """
    A utility class for generating quantum bits.
    """
    @staticmethod
    def generate() -> int:
        """
        Generates a quantum bit.

        Returns:
            int: A quantum bit (0 or 1).
        """
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        return int(QuantumMeasurer.measure(qc))


class QuantumMeasurer:
    """
    A utility class for measuring quantum circuits.
    """

    @staticmethod
    def measure(qc: QuantumCircuit, shots: int = 1) -> int:
        """
        Measures a quantum circuit.

        Args:
            qc (QuantumCircuit): The quantum circuit to measure.
            shots (int, optional): The number of measurement shots. Defaults to 1.

        Returns:
            int: The measurement result (0 or 1).
        """
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend=backend, shots=shots)
        result = job.result()
        counts = result.get_counts()
        return 0 if counts.get('0', 0) > counts.get('1', 0) else 1

# Party


class AbstractParty(ABC):
    """
    An abstract base class for quantum parties.
    """

    @abstractmethod
    def send_bit(self, receiver, bit: int, basis: int):
        """
        Sends a quantum bit to a receiver.

        Args:
            receiver: The receiving party.
            bit (int): The bit of information to send.
            basis (int): The basis to use. (0: rect, 1: diag)
        """
        pass

    @abstractmethod
    def receive(self, sender, qc: QuantumCircuit):
        """
        Receives a quantum bit from a sender.

        Args:
            sender: The sending party.
            qc (QuantumCircuit): The quantum circuit representing the bit.
        """
        pass


class Party(AbstractParty):
    """
    Represents a quantum party.
    """
    def __init__(self):
        self.bits = {}
        self.keys = {}
        self.amplified_keys = {}

    def _ensure_party_initialized(self, other_party):
        """
        Assures parties have been properly initialized with each other

        Args:
            other_party: The party to initialize/check for initialization
        """
        if other_party not in self.bits:
            self.bits[other_party] = []
        if other_party not in self.keys:
            self.keys[other_party] = []
        if other_party not in self.amplified_keys:
            self.amplified_keys[other_party] = []

    def send_bit(self, receiver, bit: int = None, basis: int = None):
        """
        Sends a quantum bit to a receiver.

        Args:
            receiver: The receiving party.
            bit (int, optional): The quantum bit to send. Defaults to a random bit.
            basis (int, optional): The basis to use. Defaults to a random basis.
        """
        self._ensure_party_initialized(receiver)

        if bit is None:
            bit = QuantumBitGenerator.generate()
        if basis is None:
            basis = QuantumBitGenerator.generate()

        self.bits[receiver].append((bit, basis))

        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == 1:
            qc.h(0)

        receiver.receive(self, qc)

    def receive(self, sender, qc: QuantumCircuit):
        """
        Receives a quantum bit from a sender.

        Args:
            sender: The sending party.
            qc (QuantumCircuit): The quantum circuit representing the bit.
        """
        self._ensure_party_initialized(sender)

        basis = QuantumBitGenerator.generate()
        if basis == 1:
            qc.h(0)
        qc.measure(0, 0)
        bit = int(QuantumMeasurer.measure(qc))

        self.bits[sender].append((bit, basis))

    def get_bases(self, other, indices: list[int]):
        return [self.bits[other][i][1] for i in indices]

    def get_bits(self, other, indices: list[int]):
        valid_indices = [i for i in indices if i >= -
                         len(self.bits[other]) and i < len(self.bits[other])]
        return [self.bits[other][i][0] for i in valid_indices]

    def add_key(self, expected_other, actual_other, indices: list[int]):
        self._ensure_party_initialized(expected_other)
        self._ensure_party_initialized(actual_other)
        valid_indices = [i for i in indices if i < len(self.bits[actual_other])]
        self.keys[expected_other].append(self.get_bits(actual_other, valid_indices))
        self.amplified_keys[expected_other].append(self.privacy_amplification(expected_other))

    def add_party(self, other):
        self.bits[other] = []
        self.keys[other] = []
        self.amplified_keys[other] = []

    def privacy_amplification(self, other, num_reduced_by_half: int = 2):
        partial_key = self.keys[other][-1]

        for i in range(num_reduced_by_half):
            reduced_key = []
            for j in list(range(len(partial_key)-1))[::2]:
                reduced_key.append(partial_key[j] ^ partial_key[j+1])
            if len(reduced_key) == 1:
                break
            partial_key = reduced_key

        return partial_key

# BB84


class AbstractQuantumProtocol(ABC):
    @abstractmethod
    def run(self):
        pass


class BB84(AbstractQuantumProtocol):
    def __init__(self, sender, receiver, eve=None, bits: int | list[int] = 100,
                 verify_len: int = 0, error_rate=0.05):

        """
        Initializes a new BB84 protocol instance.

        Args:
            sender: The sending party.
            receiver: The receiving party.
            eve (optional): The eavesdropper. Defaults to None.
            bits (int | list[int], optional): The number of bits or a list of bits. Defaults to 100.
            verify_len (int, optional): The length of the verification sequence. Defaults to 0.
            error_rate (float, optional): The acceptable error rate. Defaults to 0.05.
        """
        self.sender = sender
        self.receiver = receiver
        self.eve = eve
        self.verify_len = verify_len
        self.bits = bits
        if isinstance(self.bits, int):
            self.bits = [None] * self.bits
        self.error_rate = error_rate
        if self.eve is None:
            for bit in self.bits:
                self.sender.send_bit(self.receiver, bit=bit)
        else:
            for bit in self.bits:
                self.sender.send_bit(self.eve, bit=bit)
                # Eve measures the intercepted quantum bit
                eve_bit = self.eve.get_bits(self.sender, [-1])[0]
                self.eve.send_bit(self.receiver, bit=eve_bit)

    def detect_intrusion(self, actual_error):
        return actual_error > self.error_rate

    def run(self):
        if isinstance(self.bits, int):
            self.bits = [None] * self.bits

        sent_to = self.receiver if self.eve is None else self.eve
        received_from = self.sender if self.eve is None else self.eve

        if self.eve is None:
            for bit in self.bits:
                self.sender.send_bit(self.receiver, bit=bit)
        else:
            for bit in self.bits:
                self.sender.send_bit(self.eve, bit=bit)
                self.eve.send_bit(
                    self.receiver, bit=self.eve.get_bits(self.sender, [-1]))

        sent_bases = self.sender.get_bases(sent_to, range(-len(self.bits), 0))
        received_bases = self.receiver.get_bases(
            received_from, range(-len(self.bits), 0))

        matches = [i-len(self.bits) for i in range(len(self.bits))
                   if sent_bases[i] == received_bases[i]]
        verify_idx = random.sample(matches, self.verify_len)
        verify_self = self.sender.get_bits(sent_to, verify_idx)
        verify_receiver = self.receiver.get_bits(received_from, verify_idx)
        for i in verify_idx:
            matches.remove(i)
        verify_matches = len(
            [i for i in range(self.verify_len) if verify_self[i] == verify_receiver[i]])
        actual_error = 1 - verify_matches/self.verify_len

        self.sender.add_key(self.receiver, sent_to, matches)
        self.receiver.add_key(self.sender, received_from, matches)

        transmission1 = (self.sender.get_bits(sent_to, range(-len(self.bits), 0)), self.sender.get_bases(sent_to, range(-len(self.bits), 0)),
                         sent_to.get_bases(self.sender, range(-len(self.bits), 0)), sent_to.get_bits(self.sender, range(-len(self.bits), 0)))
        transmission2 = None if self.eve is None else (
            self.eve.get_bits(self.receiver, range(-len(self.bits), 0)
                              ), self.eve.get_bases(self.receiver, range(-len(self.bits), 0)),
            self.receiver.get_bases(received_from, range(-len(self.bits), 0)), self.receiver.get_bits(received_from, range(-len(self.bits), 0)))
        return self.detect_intrusion(actual_error), transmission1, transmission2


# Tests


# QuantumUtils


class TestQuantumUtilities(unittest.TestCase):
    def test_bit_generation(self):
        bit = QuantumBitGenerator.generate()
        self.assertIn(bit, [0, 1], "Generated bit should be 0 or 1")

    def test_bit_generation_probability(self):
        n = 1000
        ones = sum([QuantumBitGenerator.generate() for _ in range(n)])
        self.assertAlmostEqual(ones, n/2, delta=0.1*n, msg="Generated bits should be approximately 50 percent 1s")

    def test_quantum_measurement(self):
        qc = QuantumCircuit(1, 1)
        qc.h(0)
        qc.measure(0, 0)
        measurement = QuantumMeasurer.measure(qc)
        self.assertIn(measurement, [0, 1], "Measurement should be 0 or 1")

# Party


class TestParty(unittest.TestCase):
    def setUp(self):
        self.alice = Party()
        self.bob = Party()

    def test_send_receive(self):
        self.alice.send_bit(self.bob, 1, 0)
        bit, basis = self.bob.bits[self.alice][-1]
        self.assertIn(bit, [0, 1], "Received bit should be 0 or 1")
        self.assertIn(basis, [0, 1], "Receiving basis should be 0 or 1")

    def test_send_receive_random(self):
        for i in range(1, 100):
            self.alice.send_bit(self.bob)
            bit, basis = self.bob.bits[self.alice][-1]
            self.assertIn(bit, [0, 1], "Received bit should be 0 or 1")
            self.assertIn(basis, [0, 1], "Receiving basis should be 0 or 1")
            self.assertEqual(len(self.alice.bits[self.bob]), i,
                              "Alice should have {} bits sent to Bob".format(i))
            self.assertEqual(len(self.bob.bits[self.alice]), i,
                              "Bob should have {} bits received from Alice".format(i))

    def test_privacy_amplification(self):
        self.alice.keys[self.bob] = [[0, 1, 1, 0]]
        amplified_key = self.alice.privacy_amplification(self.bob)
        self.assertEqual(amplified_key, [1, 1],
                         "Amplified key should be [1, 1]")
        
    def test_privacy_amplification2(self):
        self.alice.keys[self.bob] = [[0, 1, 1, 0, 1, 1]]
        amplified_key = self.alice.privacy_amplification(self.bob)
        self.assertEqual(amplified_key, [1, 1, 0],
                         "Amplified key should be [1, 1, 0")
        
    def test_privacy_amplification2(self):
        self.alice.keys[self.bob] = [[0, 0, 1, 0, 1, 1, 0]]
        amplified_key = self.alice.privacy_amplification(self.bob)
        self.assertEqual(amplified_key, [0, 1, 0],
                         "Amplified key should be [1, 1, 0")
        
    def test_privacy_amplification_random(self):
        self.alice._ensure_party_initialized(self.bob)
        for i in range(10):
            key = [QuantumBitGenerator.generate() for _ in range(random.randint(2, 100))]
            self.alice.keys[self.bob].append(key)

            times = random.randint(1, 10)
            amplified_key = self.alice.privacy_amplification(self.bob, times)

            while (len(key)>>times <= 1):
                times -= 1
            expected_len = len(key)>>times
            def xor_reduce(arr):
                xor = 0
                for i in arr:
                    xor ^= i
                return xor
            expected_key = [xor_reduce(key[i<<times:(i+1)<<times]) for i in range(expected_len)]
            self.assertEqual(len(amplified_key), expected_len,
                            "Amplified key should have length {}".format(expected_len))
            self.assertEqual(amplified_key, expected_key,
                            "Amplified key should be {}".format(expected_key))

    def test_add_party(self):
        self.alice.add_party(self.bob)
        self.assertIn(self.bob, self.alice.bits,
                      "Bob should be added to Alice's parties")
        
    def test_get_bits_bases(self):
        n = 10
        pairs = [(QuantumBitGenerator.generate(), QuantumBitGenerator.generate()) for _ in range(n)]
        for bit, basis in pairs:
            self.alice.send_bit(self.bob, bit, basis)

        self.assertEqual(self.alice.get_bits(self.bob, range(-n, 0)), [bit for bit, _ in pairs])
        self.assertEqual(self.alice.get_bases(self.bob, range(-n, 0)), [basis for _, basis in pairs])

# BB84


class TestBB84(unittest.TestCase):
    def setUp(self):
        self.alice = Party()
        self.bob = Party()
        self.eve = Party()

        # Initialize parties
        self.alice._ensure_party_initialized(self.bob)
        self.bob._ensure_party_initialized(self.alice)

    def test_bb84_without_eve(self):
        protocol = BB84(self.alice, self.bob, bits=20, verify_len=5)
        intrusion, _, _ = protocol.run()
        self.assertFalse(
            intrusion, "Intrusion should not be detected without Eve")
        self.assertEqual(self.alice.keys[self.bob][-1], self.bob.keys[self.alice][-1], 
                         "Alice and Bob should have the same key")

    def test_bb84_with_eve(self):
        protocol = BB84(self.alice, self.bob, eve=self.eve,
                        bits=60, verify_len=10)
        intrusion, _, _ = protocol.run()
        self.assertTrue(intrusion, "Intrusion should be detected with Eve")
        self.assertNotEqual(self.alice.keys[self.bob][-1], self.bob.keys[self.alice][-1], 
                            "Alice and Bob should not have the same key")

    def test_bb84_with_random_eve(self):
        for i in range(1, 10):
            if random.randint(0, 1):
                self.test_bb84_with_eve()
            else:
                self.test_bb84_without_eve()
            self.assertEqual(len(self.alice.keys[self.bob]), i, "Number of keys should be {}".format(i))

# Run


def run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)


run_tests()



# # Graphics possibly
# # from p5 import *
# # run(renderer="vispy")
