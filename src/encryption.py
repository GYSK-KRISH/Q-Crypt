"""
====================================================================
Q-Crypt: Classical Message Encryption & Decryption Module (OTP/XOR)
====================================================================
Educational Architecture (Class 12 Physics / CS):
Demonstrates how a quantum-established secret key (from BB84) is used
by classical cryptography to securely send a text message.

--------------------------------------------------------------------
Key Architectural Principle:
--------------------------------------------------------------------
BB84 DOES NOT encrypt the message directly!
BB84 is strictly a Key Distribution Protocol.

The Complete Secure Pipeline:
1. Alice & Bob run BB84 over a Quantum Channel to establish a shared candidate key.
2. If QBER <= Threshold -> The Candidate Key is validated and accepted.
3. Alice uses the candidate key to classically encrypt her message (One-Time Pad XOR).
4. Alice sends the Ciphertext to Bob across a standard Public Channel (Internet).
5. Bob uses his identical candidate key to classically decrypt the Ciphertext back to text.

*Educational Disclaimer*:
This module is an educational simulator demonstrating the relationship between
quantum key distribution and classical symmetric encryption (One-Time Pad).
It is not intended as a production-grade cryptographic system.
====================================================================
"""

import os
import sys
from typing import List, Optional, Dict, Any

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.experiment_runner import ExperimentConfig, ExperimentResult, run_experiment


def text_to_bits(text: str) -> List[int]:
    """
    Converts a plain text string into a list of binary bits (8 bits per ASCII character).
    Example: 'Hi' -> [0,1,0,0,1,0,0,0, 0,1,1,0,1,0,0,1]
    """
    bits = []
    for char in text:
        bin_val = bin(ord(char))[2:].zfill(8)
        for b in bin_val:
            bits.append(int(b))
    return bits


def bits_to_text(bits: List[int]) -> str:
    """
    Converts a list of binary bits back into a plain text string (in 8-bit byte chunks).
    """
    chars = []
    for i in range(0, len(bits), 8):
        byte_chunk = bits[i : i + 8]
        if len(byte_chunk) == 8:
            byte_str = "".join(map(str, byte_chunk))
            chars.append(chr(int(byte_str, 2)))
    return "".join(chars)


def encrypt_message(plaintext: str, candidate_key: List[int]) -> dict:
    """
    Step 3 (Classical Encryption):
    Alice encrypts plaintext using the shared candidate key via One-Time Pad (XOR).
    
    Formula: Ciphertext_Bit = Plaintext_Bit XOR Key_Bit
    """
    message_bits = text_to_bits(plaintext)
    req_len = len(message_bits)

    if len(candidate_key) < req_len:
        raise ValueError(
            f"Candidate key length ({len(candidate_key)} bits) is too short for message "
            f"'{plaintext}' ({req_len} bits needed). Run BB84 with more qubits."
        )

    # Use exact number of key bits needed
    key_slice = candidate_key[:req_len]

    # Bitwise XOR encryption: c = m ^ k
    ciphertext_bits = [m ^ k for m, k in zip(message_bits, key_slice)]

    # Convert ciphertext bits to hexadecimal string for display
    hex_chars = []
    for i in range(0, len(ciphertext_bits), 8):
        byte_val = int("".join(map(str, ciphertext_bits[i : i + 8])), 2)
        hex_chars.append(f"{byte_val:02X}")
    ciphertext_hex = "".join(hex_chars)

    return {
        "plaintext": plaintext,
        "plaintext_bits": message_bits,
        "key_slice": key_slice,
        "ciphertext_bits": ciphertext_bits,
        "ciphertext_hex": ciphertext_hex,
    }


def decrypt_message(ciphertext_bits: List[int], candidate_key: List[int]) -> str:
    """
    Step 5 (Classical Decryption):
    Bob decrypts the ciphertext using his copy of the shared candidate key via XOR.
    
    Formula: Plaintext_Bit = Ciphertext_Bit XOR Key_Bit
    """
    req_len = len(ciphertext_bits)
    if len(candidate_key) < req_len:
        raise ValueError("Bob's candidate key is shorter than the received ciphertext.")

    key_slice = candidate_key[:req_len]

    # Bitwise XOR decryption: m = c ^ k
    decrypted_bits = [c ^ k for c, k in zip(ciphertext_bits, key_slice)]

    return bits_to_text(decrypted_bits)


def send_secure_message(
    message: str = "QUANTUM",
    eve_enabled: bool = False,
    noise_level: str = "OFF",
    qber_threshold: float = 0.11,
    random_seed: Optional[int] = None,
):
    """
    Executes the complete end-to-end pipeline:
    1. Calculates required quantum transmissions.
    2. Runs BB84 to establish candidate key.
    3. Validates key security (aborts if QBER > threshold).
    4. Alice classically encrypts message.
    5. Transmits ciphertext.
    6. Bob classically decrypts message.
    """
    print("=" * 80)
    print("            Q-CRYPT: END-TO-END SECURE MESSAGING DEMO")
    print("=" * 80)

    # 1. Message Bit Analysis
    message_bits = text_to_bits(message)
    num_message_bits = len(message_bits)

    # Allocate ~3.5x qubits to safely guarantee enough candidate key bits
    num_qubits = max(60, int(num_message_bits * 3.5))

    print(f"\n[Stage 1: Message Preparation]")
    print(f"  Plaintext Message         : '{message}'")
    print(f"  Message Bit Length        : {num_message_bits} bits ({len(message)} characters x 8 bits)")
    print(f"  Required Qubit Allocation : {num_qubits} qubits (to yield >= {num_message_bits} candidate key bits)")

    # 2. Quantum Key Distribution (BB84)
    print(f"\n[Stage 2: Quantum Key Distribution (BB84)]")
    print(f"  Transmitting {num_qubits} photons over Quantum Channel...")
    print(f"  Eve Status: {'ON (Intercept-Resend Active)' if eve_enabled else 'OFF (Secure Channel)'} | Noise Level: {noise_level}")

    config = ExperimentConfig(
        num_qubits=num_qubits,
        eve_enabled=eve_enabled,
        noise_enabled=(noise_level.upper() != "OFF"),
        noise_level=noise_level,
        qber_threshold=qber_threshold,
        random_seed=random_seed,
    )
    result = run_experiment(config)

    print(f"  Matching Bases Sifted     : {len(result.alice_sifted_key)} bits")
    print(f"  Test Bits Sampled         : {len(result.test_sample_indices)} bits")
    print(f"  Errors Detected           : {result.errors}")
    print(f"  Measured QBER             : {result.qber:.4f} ({result.qber * 100:.2f}%)")
    print(f"  Acceptance Threshold      : {qber_threshold:.4f} ({qber_threshold * 100:.1f}%)")
    print(f"  Candidate Key Yield       : {len(result.alice_candidate_key)} bits")

    # 3. Security Validation Check
    print(f"\n[Stage 3: Security Validation & Key Verification]")
    if result.status != "PASSED":
        print("  [X] KEY REJECTED / ABORTED!")
        print(f"  Measured QBER ({result.qber * 100:.2f}%) exceeded threshold ({qber_threshold * 100:.1f}%).")
        print("  [CRITICAL] Eavesdropper or severe noise detected. ENCRYPTION CANNOT PROCEED!")
        print("=" * 80)
        return False

    if len(result.alice_candidate_key) < num_message_bits:
        print("  [!] INSUFFICIENT KEY LENGTH!")
        print(f"  Candidate key has {len(result.alice_candidate_key)} bits; message requires {num_message_bits} bits.")
        print("  Please increase initial qubit count.")
        print("=" * 80)
        return False

    print("  [OK] KEY ACCEPTED! QBER is within safety threshold.")
    print("  Alice and Bob have successfully established a shared secret candidate key.")

    # 4. Classical Encryption by Alice
    print(f"\n[Stage 4: Classical Encryption by Alice (One-Time Pad)]")
    encryption_payload = encrypt_message(message, result.alice_candidate_key)

    key_slice_str = "".join(map(str, encryption_payload["key_slice"]))
    msg_bits_str = "".join(map(str, encryption_payload["plaintext_bits"]))
    cipher_bits_str = "".join(map(str, encryption_payload["ciphertext_bits"]))

    print(f"  Plaintext Bits (M)        : {msg_bits_str}")
    print(f"  Alice Candidate Key (K)   : {key_slice_str}")
    print(f"  XOR Ciphertext Bits (C)   : {cipher_bits_str}")
    print(f"  Ciphertext Hex Transmission: 0x{encryption_payload['ciphertext_hex']}")

    # 5. Public Classical Transmission
    print(f"\n[Stage 5: Public Channel Transmission]")
    print(f"  Alice sends Ciphertext (0x{encryption_payload['ciphertext_hex']}) over the Public Classical Channel.")
    print("  (An eavesdropper seeing the ciphertext learns ZERO information without the key).")

    # 6. Classical Decryption by Bob
    print(f"\n[Stage 6: Classical Decryption by Bob]")
    decrypted_text = decrypt_message(encryption_payload["ciphertext_bits"], result.bob_candidate_key)
    bob_key_slice_str = "".join(map(str, result.bob_candidate_key[:num_message_bits]))

    print(f"  Bob Candidate Key (K)     : {bob_key_slice_str}")
    print(f"  Decrypted Binary Result   : {msg_bits_str}")
    print(f"  Recovered Plaintext Text  : '{decrypted_text}'")

    # Final Verification
    print(f"\n[Stage 7: End-to-End Verification]")
    if decrypted_text == message:
        print("  [SUCCESS] Bob recovered Alice's exact message with 100% fidelity!")
    else:
        print("  [ERROR] Decrypted text does not match original message.")
    print("=" * 80)
    return True


def main():
    print("=" * 75)
    print("      Q-Crypt: Quantum Key Distribution & Classical Encryption")
    print("=" * 75)

    # 1. Message
    user_msg = input("Enter message to encrypt (e.g. 'HELLO', 'QUANTUM'; default 'Q-CRYPT'): ").strip()
    message = user_msg if user_msg else "Q-CRYPT"

    # 2. Eve toggle
    eve_input = input("Enable Eve Intercept-Resend attack? (ON / OFF; default OFF): ").strip().upper()
    eve_enabled = eve_input in ["ON", "Y", "YES", "TRUE", "1"]

    # 3. Noise level
    print("Select Quantum Noise Level: OFF, LOW, MEDIUM, HIGH")
    noise_input = input("Enter Noise Level (default OFF): ").strip().upper()
    noise_level = noise_input if noise_input in ["OFF", "LOW", "MEDIUM", "HIGH"] else "OFF"

    # 4. Run Demonstration
    send_secure_message(
        message=message,
        eve_enabled=eve_enabled,
        noise_level=noise_level,
        qber_threshold=0.11,
    )


if __name__ == "__main__":
    main()
