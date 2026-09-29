"""
====================================================================
Tests for Classical BB84 Protocol Simulator (tests/test_classical_bb84.py)
====================================================================
Educational Objective:
Demonstrate how unit tests verify the logical rules of BB84:
1. Valid bit values (0 or 1).
2. Valid basis selections ('Z' or 'X').
3. Deterministic outcome when bases match.
4. Valid measurement outcome when bases mismatch.
5. Correct sifting (discarding mismatches and preserving matching bits).
6. Perfect key agreement between Alice and Bob.
====================================================================
"""

import unittest
import sys
import os

# Ensure the project root and 'src' directory are in Python's search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.classical_bb84 import (
    generate_random_bits,
    generate_random_bases,
    simulate_bob_measurement,
    sift_keys,
)


class TestClassicalBB84(unittest.TestCase):
    """Test suite for the classical BB84 functions."""

    def test_random_bits_validity(self):
        """Test 1: Generated bits should only contain 0 or 1, and match requested length."""
        n = 50
        bits = generate_random_bits(n)

        # Check list length
        self.assertEqual(len(bits), n, "Bit list length should match requested count.")

        # Check every element is either 0 or 1
        for bit in bits:
            self.assertIn(bit, [0, 1], f"Bit value {bit} is invalid; expected 0 or 1.")

    def test_random_bases_validity(self):
        """Test 2: Generated bases should only be 'Z' or 'X', and match requested length."""
        n = 50
        bases = generate_random_bases(n)

        # Check list length
        self.assertEqual(len(bases), n, "Bases list length should match requested count.")

        # Check every element is either 'Z' or 'X'
        for b in bases:
            self.assertIn(b, ["Z", "X"], f"Basis {b} is invalid; expected 'Z' or 'X'.")

    def test_matching_bases_preserve_alice_bits(self):
        """
        Test 3: When Bob's basis matches Alice's basis, Bob must ALWAYS
        measure the exact bit Alice sent (100% deterministic).
        """
        # Controlled scenario: Alice and Bob choose identical bases
        alice_bits = [0, 1, 0, 1, 1, 0, 0, 1]
        alice_bases = ["Z", "Z", "X", "X", "Z", "X", "Z", "X"]
        bob_bases = ["Z", "Z", "X", "X", "Z", "X", "Z", "X"]  # Identical to Alice

        bob_results = simulate_bob_measurement(alice_bits, alice_bases, bob_bases)

        # When bases match, Bob's measurements must equal Alice's bits exactly
        self.assertEqual(
            bob_results,
            alice_bits,
            "Bob's measurements should exactly match Alice's bits when all bases match.",
        )

    def test_mismatched_bases_produce_valid_bits(self):
        """
        Test 4: When bases differ, Bob's measurement collapses to a valid bit (0 or 1).
        """
        # Controlled scenario: All bases intentionally mismatched
        alice_bits = [0, 1, 0, 1]
        alice_bases = ["Z", "Z", "X", "X"]
        bob_bases = ["X", "X", "Z", "Z"]  # Opposite of Alice

        bob_results = simulate_bob_measurement(alice_bits, alice_bases, bob_bases)

        self.assertEqual(len(bob_results), len(alice_bits))
        for res in bob_results:
            self.assertIn(res, [0, 1], f"Measurement {res} is invalid; expected 0 or 1.")

    def test_sifting_removes_mismatches(self):
        """
        Test 5: Sifting must discard all positions where bases differ.
        """
        alice_bits = [1, 0, 1, 0]
        bob_results = [1, 1, 1, 0]  # Measurement results
        alice_bases = ["Z", "Z", "X", "X"]
        bob_bases = ["Z", "X", "X", "Z"]  # Matches at index 0 and 2; mismatches at 1 and 3

        alice_key, bob_key, matching_indices = sift_keys(
            alice_bits, bob_results, alice_bases, bob_bases
        )

        # Only index 0 and 2 should be kept
        self.assertEqual(matching_indices, [0, 2], "Matching indices should be [0, 2].")
        self.assertEqual(len(alice_key), 2, "Sifted key length should be 2.")
        self.assertEqual(len(bob_key), 2, "Bob's sifted key length should be 2.")

    def test_sifted_key_contains_matching_basis_positions(self):
        """
        Test 6: Sifted keys from Alice and Bob must be identical and correspond
        only to matching basis positions.
        """
        alice_bits = [0, 1, 1, 0, 1]
        alice_bases = ["Z", "X", "Z", "X", "Z"]
        bob_bases = ["Z", "Z", "Z", "X", "X"]
        # Matches at index: 0 ('Z'=='Z'), 2 ('Z'=='Z'), 3 ('X'=='X')
        # Expected Alice kept bits: [alice_bits[0], alice_bits[2], alice_bits[3]] -> [0, 1, 0]

        bob_results = simulate_bob_measurement(alice_bits, alice_bases, bob_bases)
        alice_key, bob_key, matching_indices = sift_keys(
            alice_bits, bob_results, alice_bases, bob_bases
        )

        # 1. Matching indices should strictly be [0, 2, 3]
        self.assertEqual(matching_indices, [0, 2, 3])

        # 2. Alice's sifted key should match expected bits from those indices
        expected_key = [0, 1, 0]
        self.assertEqual(alice_key, expected_key)

        # 3. In the absence of noise/Eve, Alice's key and Bob's key must match 100%
        self.assertEqual(
            alice_key, bob_key, "Alice and Bob's sifted keys must be identical."
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
