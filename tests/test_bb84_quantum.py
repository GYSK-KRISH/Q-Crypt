"""
====================================================================
Tests for Quantum BB84 Simulator (tests/test_bb84_quantum.py)
====================================================================
Verifies that:
1. prepare_qubit constructs valid 1-qubit QuantumCircuits.
2. measure_qubit correctly simulates measurements on AerSimulator.
3. Deterministic basis matches produce identical bits in the quantum circuit.
4. estimate_qber_and_extract_key correctly calculates QBER and separates test bits.
====================================================================
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qiskit_aer import AerSimulator
from src.bb84_quantum import prepare_qubit, measure_qubit, estimate_qber_and_extract_key


class TestQuantumBB84(unittest.TestCase):
    """Unit tests for the Qiskit-based BB84 simulator functions."""

    def setUp(self):
        self.simulator = AerSimulator()

    def test_prepare_qubit_circuit_properties(self):
        """Test that prepare_qubit returns a circuit with 1 qubit and 1 classical bit."""
        qc = prepare_qubit(bit=1, basis="X")
        self.assertEqual(qc.num_qubits, 1)
        self.assertEqual(qc.num_clbits, 1)

    def test_quantum_deterministic_z_basis(self):
        """Test that Bit 0 and Bit 1 in Z basis measure deterministically."""
        qc0 = prepare_qubit(bit=0, basis="Z")
        res0 = measure_qubit(qc0, "Z", self.simulator)
        self.assertEqual(res0, 0)

        qc1 = prepare_qubit(bit=1, basis="Z")
        res1 = measure_qubit(qc1, "Z", self.simulator)
        self.assertEqual(res1, 1)

    def test_quantum_deterministic_x_basis(self):
        """Test that Bit 0 and Bit 1 in X basis measure deterministically when measured in X basis."""
        qc0 = prepare_qubit(bit=0, basis="X")
        res0 = measure_qubit(qc0, "X", self.simulator)
        self.assertEqual(res0, 0)

        qc1 = prepare_qubit(bit=1, basis="X")
        res1 = measure_qubit(qc1, "X", self.simulator)
        self.assertEqual(res1, 1)

    def test_qber_zero_error_calculation(self):
        """Test QBER calculation when Alice and Bob keys are identical (0% error)."""
        alice_sifted = [1, 0, 1, 1, 0, 1]
        bob_sifted = [1, 0, 1, 1, 0, 1]

        stats = estimate_qber_and_extract_key(alice_sifted, bob_sifted, test_sample_size=2)

        self.assertEqual(stats["num_test_bits"], 2)
        self.assertEqual(stats["num_errors"], 0)
        self.assertEqual(stats["qber"], 0.0)
        self.assertEqual(len(stats["alice_candidate_key"]), 4)
        self.assertEqual(stats["alice_candidate_key"], stats["bob_candidate_key"])

    def test_qber_non_zero_error_calculation(self):
        """Test QBER calculation with deliberate injected errors."""
        alice_sifted = [1, 1, 1, 1]
        bob_sifted = [0, 0, 0, 0]  # 100% error

        stats = estimate_qber_and_extract_key(alice_sifted, bob_sifted, test_sample_size=4)

        self.assertEqual(stats["num_test_bits"], 4)
        self.assertEqual(stats["num_errors"], 4)
        self.assertEqual(stats["qber"], 1.0)
        self.assertEqual(len(stats["alice_candidate_key"]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
