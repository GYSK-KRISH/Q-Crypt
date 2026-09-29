"""
====================================================================
Tests for Classical Message Encryption & Decryption (tests/test_encryption.py)
====================================================================
Verifies that:
1. text_to_bits and bits_to_text perform lossless conversion.
2. One-Time Pad XOR encryption and decryption successfully recover plaintext.
3. Encryption raises ValueError when candidate key is shorter than message.
4. send_secure_message succeeds on clean channels and aborts when Eve is active.
====================================================================
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.encryption import (
    text_to_bits,
    bits_to_text,
    encrypt_message,
    decrypt_message,
    send_secure_message,
)


class TestEncryption(unittest.TestCase):
    """Test suite for the classical OTP encryption and decryption logic."""

    def test_text_to_bits_and_back(self):
        """Test binary encoding and decoding roundtrip."""
        original_text = "BB84 Quantum Key Distribution!"
        bits = text_to_bits(original_text)

        # 8 bits per character
        self.assertEqual(len(bits), len(original_text) * 8)

        # Convert back
        recovered_text = bits_to_text(bits)
        self.assertEqual(recovered_text, original_text)

    def test_otp_encryption_decryption(self):
        """Test that XOR encryption and decryption recover the exact plaintext."""
        message = "SECRET123"
        msg_bits = text_to_bits(message)

        # Candidate key of identical length
        candidate_key = [1, 0, 1, 1, 0, 1, 0, 0] * len(message)

        # Encrypt
        encrypted = encrypt_message(message, candidate_key)
        self.assertIn("ciphertext_bits", encrypted)
        self.assertIn("ciphertext_hex", encrypted)

        # Decrypt
        decrypted = decrypt_message(encrypted["ciphertext_bits"], candidate_key)
        self.assertEqual(decrypted, message)

    def test_insufficient_key_length_raises_error(self):
        """Test that attempting to encrypt with a short key raises ValueError."""
        message = "HELLO"  # Requires 40 bits
        short_key = [1, 0, 1, 0]  # Only 4 bits

        with self.assertRaises(ValueError):
            encrypt_message(message, short_key)

    def test_send_secure_message_success(self):
        """Test end-to-end secure messaging pipeline with Eve OFF, Noise OFF."""
        success = send_secure_message(
            message="OK",
            eve_enabled=False,
            noise_level="OFF",
            random_seed=42,
        )
        self.assertTrue(success)

    def test_send_secure_message_eve_aborted(self):
        """Test that send_secure_message aborts when Eve is active and triggers high QBER."""
        success = send_secure_message(
            message="OK",
            eve_enabled=True,
            noise_level="OFF",
            qber_threshold=0.10,
            random_seed=42,
        )
        # Eve introduces ~25% error, exceeding 10% threshold -> aborts
        self.assertFalse(success)


if __name__ == "__main__":
    unittest.main(verbosity=2)
