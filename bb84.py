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
        self.error_rates = {}
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

    def add_key(self, other, indices: list[int]):
        self._ensure_party_initialized(other)
        valid_indices = [i for i in indices if i < len(self.bits[other])]
        self.keys[other].append(self.get_bits(other, valid_indices))
        self.amplified_keys[other].append(self.privacy_amplification(other))

    def add_party(self, other):
        self.bits[other] = []
        self.keys[other] = []
        self.amplified_keys[other] = []

    def privacy_amplification(self, other, num_reduced_by_half: int = 2):
        partial_key = self.keys[other][-1]

        if len(partial_key) % 2 == 1:
            partial_key = partial_key[:-1]

        for i in range(num_reduced_by_half):
            reduced_key = []
            for j in list(range(len(partial_key)))[::2]:
                reduced_key.append(partial_key[j] ^ partial_key[j+1])
            if len(reduced_key) == 1:
                break
            partial_key = reduced_key if len(
                reduced_key) % 2 == 0 else reduced_key[:-1]

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

        # Ensure the indices are valid for the self.bits[other] list
        valid_indices = [i for i in matches if i <
                         len(self.sender.bits[self.receiver])]

        self.sender.add_key(self.receiver, valid_indices)
        self.receiver.add_key(self.sender, valid_indices)

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

    def test_privacy_amplification(self):
        self.alice.keys[self.bob] = [[0, 1, 1, 0]]
        amplified_key = self.alice.privacy_amplification(self.bob)
        self.assertEqual(amplified_key, [1, 1],
                         "Amplified key should be [1, 1]")

    def test_add_party(self):
        self.alice.add_party(self.bob)
        self.assertIn(self.bob, self.alice.bits,
                      "Bob should be added to Alice's parties")

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

    def test_bb84_with_eve(self):
        protocol = BB84(self.alice, self.bob, eve=self.eve,
                        bits=20, verify_len=5)
        intrusion, _, _ = protocol.run()
        self.assertTrue(intrusion, "Intrusion should be detected with Eve")

# Run


def run_tests():
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=2).run(suite)


run_tests()



# # Graphics possibly
# # from p5 import *
# # run(renderer="vispy")
