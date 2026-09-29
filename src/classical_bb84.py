"""
====================================================================
Q-Crypt: Classical BB84 Protocol Simulator
====================================================================
Educational Objective (Class 12 CS / Physics Viva):
Understand the core mathematical and logical flow of the BB84 Quantum
Key Distribution (QKD) protocol using pure Python (standard library only).

In this simulator, we model the quantum behavior classically:
- When Bob's basis MATCHES Alice's basis -> Bob gets Alice's exact bit (100%).
- When Bob's basis DIFFERS from Alice's -> Quantum collapse makes Bob's
  measured outcome 50% random (0 or 1).

Protocol Steps (Sifting Phase):
1. Alice generates random bits (0 or 1).
2. Alice chooses random bases (Z or X) to encode each bit.
3. Bob chooses random bases (Z or X) to measure each incoming qubit.
4. Bob measures qubits based on quantum probability rules.
5. Sifting Phase: Alice and Bob publicly announce their BASES (never their bits).
6. They keep only bits where their bases matched -> This forms the SIFTED KEY!
====================================================================
"""

import random
import sys

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def generate_random_bits(n: int) -> list:
    """
    Step 1: Alice generates a sequence of random classical bits (0 or 1).
    Example: [1, 0, 1, 1, 0]
    """
    return [random.choice([0, 1]) for _ in range(n)]


def generate_random_bases(n: int) -> list:
    """
    Step 2 & 3: Generate a random sequence of bases ('Z' or 'X').
    'Z' represents the Rectilinear basis (+).
    'X' represents the Diagonal basis (×).
    """
    return [random.choice(["Z", "X"]) for _ in range(n)]


def simulate_bob_measurement(alice_bits: list, alice_bases: list, bob_bases: list) -> list:
    """
    Step 4: Simulate Bob measuring Alice's photons.
    
    Quantum Rule:
    - If Bob's basis == Alice's basis: Deterministic result (Bob gets Alice's exact bit).
    - If Bob's basis != Alice's basis: Probabilistic collapse (Bob gets random 0 or 1).
    """
    bob_results = []
    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            # Bases match: Bob measures the exact bit Alice sent
            bob_results.append(alice_bits[i])
        else:
            # Bases mismatch: Quantum state collapses randomly (50% chance of 0 or 1)
            bob_results.append(random.choice([0, 1]))
    return bob_results


def sift_keys(alice_bits: list, bob_results: list, alice_bases: list, bob_bases: list):
    """
    Step 5, 6 & 7: Sifting Phase.
    Alice and Bob compare bases over a public channel.
    - If bases matched: Keep the bit in the sifted key.
    - If bases differed: Discard the bit.
    
    Returns:
        alice_sifted_key (list), bob_sifted_key (list), matching_indices (list)
    """
    alice_sifted = []
    bob_sifted = []
    matching_indices = []

    for i in range(len(alice_bits)):
        if alice_bases[i] == bob_bases[i]:
            alice_sifted.append(alice_bits[i])
            bob_sifted.append(bob_results[i])
            matching_indices.append(i)

    return alice_sifted, bob_sifted, matching_indices


def display_simulation_table(n: int, alice_bits: list, alice_bases: list,
                             bob_bases: list, bob_results: list, matching_indices: list):
    """Prints a neat step-by-step table comparing Alice and Bob's transmission."""
    print("\n" + "=" * 75)
    print(f"{'Index':^7}|{'Alice Bit':^11}|{'Alice Basis':^13}|{'Bob Basis':^11}|{'Bob Measured':^14}|{'Match?':^8}|{'Key Bit':^9}")
    print("=" * 75)

    matching_set = set(matching_indices)
    for i in range(n):
        matched = "YES" if i in matching_set else "NO"
        key_bit = str(alice_bits[i]) if i in matching_set else "-"
        print(f"{i:^7}|{alice_bits[i]:^11}|{alice_bases[i]:^13}|{bob_bases[i]:^11}|{bob_results[i]:^14}|{matched:^8}|{key_bit:^9}")
    print("=" * 75)


def run_classical_bb84():
    """Main function to run the interactive classical BB84 simulation."""
    print("=" * 70)
    print("         Q-Crypt: Classical BB84 Protocol Simulator")
    print("=" * 70)

    # 1. Ask user for number of qubits to send
    user_input = input("Enter number of qubits to simulate (press Enter for default 20): ").strip()
    if user_input.isdigit() and int(user_input) > 0:
        n = int(user_input)
    else:
        n = 20
        print(f"[Using default value: {n} qubits]")

    # 2. Alice generates random bits and random preparation bases
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)

    # 3. Bob independently selects random measurement bases
    bob_bases = generate_random_bases(n)

    # 4. Simulate Bob's quantum measurements
    bob_results = simulate_bob_measurement(alice_bits, alice_bases, bob_bases)

    # 5. Perform the sifting process (keep matching bases)
    alice_key, bob_key, matching_indices = sift_keys(alice_bits, bob_results, alice_bases, bob_bases)

    # 6. Display step-by-step breakdown table (up to 30 qubits for clean terminal view)
    if n <= 30:
        display_simulation_table(n, alice_bits, alice_bases, bob_bases, bob_results, matching_indices)
    else:
        print(f"\n[Note: Table skipped because {n} is large. Showing summary directly.]")

    # 7. Display Final Results
    print("\n" + "=" * 70)
    print("                     FINAL RESULTS")
    print("=" * 70)
    print(f"Total Qubits Transmitted     : {n}")
    print(f"Matching Bases (Kept Bits)   : {len(matching_indices)}")
    print(f"Discarded Bits (Mismatched)  : {n - len(matching_indices)}")
    print(f"Sifted Key Length            : {len(alice_key)} bits")

    efficiency = (len(alice_key) / n) * 100 if n > 0 else 0
    print(f"Protocol Sifting Efficiency  : {efficiency:.2f}% (Theoretical average: ~50%)")

    # Convert list of ints to string format for display
    alice_key_str = "".join(map(str, alice_key))
    bob_key_str = "".join(map(str, bob_key))

    print(f"\nAlice's Sifted Key           : {alice_key_str}")
    print(f"Bob's Sifted Key             : {bob_key_str}")

    # Check key agreement
    if alice_key == bob_key:
        print("\n[SUCCESS] Alice and Bob have generated identical secret keys! 100% agreement.")
    else:
        print("\n[ERROR] Key mismatch detected.")

    print("=" * 70)


if __name__ == "__main__":
    run_classical_bb84()
