"""
====================================================================
Q-Crypt: Quantum BB84 Simulator with Eve Attack & Quantum Noise
====================================================================
Educational Objective (Class 12 Physics / CS):
Simulate the full BB84 Quantum Key Distribution protocol with:
1. Quantum state preparation and basis transformations on Qiskit Aer.
2. Optional Eavesdropping (Eve Intercept-Resend attack).
3. Optional Channel Noise (Noise Model: OFF, LOW, MEDIUM, HIGH).
4. Sifting, QBER parameter estimation, and Candidate Key extraction.

--------------------------------------------------------------------
Understanding Noise vs. Eavesdropping:
--------------------------------------------------------------------
- In quantum cryptography, noise and eavesdropping both manifest as errors
  (bit flips and phase flips) on the sifted key.
- Because Alice and Bob cannot distinguish environmental noise from Eve
  during parameter estimation, ANY error rate above the acceptance
  threshold (e.g. 11%) forces them to safely ABORT the protocol.
====================================================================
"""

import random
import sys
from typing import Optional, List, Dict, Any

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

# Noise level configurations (Error probabilities)
NOISE_CONFIGS = {
    "OFF": 0.00,
    "LOW": 0.03,
    "MEDIUM": 0.08,
    "HIGH": 0.20,
}


def build_noise_model(noise_level: str) -> NoiseModel:
    """
    Constructs a Qiskit Aer NoiseModel for the chosen noise level.
    Adds depolarizing gate errors on ('x', 'h') and detector readout error.
    """
    prob = NOISE_CONFIGS.get(noise_level.upper(), 0.0)
    if prob <= 0.0:
        return None

    noise_model = NoiseModel()
    gate_error = depolarizing_error(prob, 1)
    noise_model.add_all_qubit_quantum_error(gate_error, ["x", "h"])

    readout_error = ReadoutError([[1.0 - prob, prob], [prob, 1.0 - prob]])
    noise_model.add_all_qubit_readout_error(readout_error)

    return noise_model


def get_state_symbol(bit: int, basis: str) -> str:
    """Returns the Dirac ket notation symbol for the prepared quantum state."""
    if basis == "Z":
        return "|0>" if bit == 0 else "|1>"
    else:  # basis == "X"
        return "|+>" if bit == 0 else "|->"


def prepare_qubit(bit: int, basis: str) -> QuantumCircuit:
    """
    Alice (or Eve) prepares a 1-qubit quantum state based on a bit and basis.
    - Bit 0 in Z -> |0>
    - Bit 1 in Z -> |1> (via X gate)
    - Bit 0 in X -> |+> (via H gate)
    - Bit 1 in X -> |-> (via X then H gate)
    """
    qc = QuantumCircuit(1, 1)

    if bit == 1:
        qc.x(0)  # Bit flip

    if basis == "X":
        qc.h(0)  # Superposition

    qc.barrier()
    return qc


def measure_qubit(
    qc: QuantumCircuit,
    basis: str,
    simulator: AerSimulator,
    seed: Optional[int] = None,
) -> int:
    """
    Measures a qubit in the specified basis (Z or X) for 1 shot.
    - If measuring in X basis, applies H gate first before measurement.
    """
    if basis == "X":
        qc.h(0)  # Rotate X basis to Z basis for measurement

    qc.measure(0, 0)

    run_kwargs = {"shots": 1}
    if seed is not None:
        run_kwargs["seed_simulator"] = seed

    job = simulator.run(qc, **run_kwargs)
    result = job.result()
    counts = result.get_counts()

    measured_bit_str = list(counts.keys())[0]
    return int(measured_bit_str)


def estimate_qber_and_extract_key(
    alice_sifted_key: list,
    bob_sifted_key: list,
    test_sample_size: int = None,
    test_sample_fraction: float = 0.33,
):
    """
    Performs parameter estimation on the sifted key.
    
    1. Selects a random subset of test bits from the sifted key.
    2. Compares Alice's and Bob's values at those test indices to count errors.
    3. Calculates QBER = (errors) / (number of test bits).
    4. Separates the remaining unrevealed bits into the candidate key.
    """
    sifted_len = len(alice_sifted_key)

    if sifted_len == 0:
        return {
            "num_test_bits": 0,
            "test_indices": [],
            "num_errors": 0,
            "qber": 0.0,
            "alice_candidate_key": [],
            "bob_candidate_key": [],
        }

    if test_sample_size is not None:
        num_test_bits = min(test_sample_size, sifted_len)
    else:
        num_test_bits = max(1, int(sifted_len * test_sample_fraction))
        if num_test_bits >= sifted_len and sifted_len > 1:
            num_test_bits = sifted_len // 2

    test_indices = sorted(random.sample(range(sifted_len), num_test_bits))
    test_indices_set = set(test_indices)

    num_errors = 0
    for idx in test_indices:
        if alice_sifted_key[idx] != bob_sifted_key[idx]:
            num_errors += 1

    qber = (num_errors / num_test_bits) if num_test_bits > 0 else 0.0

    alice_candidate_key = [
        alice_sifted_key[i] for i in range(sifted_len) if i not in test_indices_set
    ]
    bob_candidate_key = [
        bob_sifted_key[i] for i in range(sifted_len) if i not in test_indices_set
    ]

    return {
        "num_test_bits": num_test_bits,
        "test_indices": test_indices,
        "num_errors": num_errors,
        "qber": qber,
        "alice_candidate_key": alice_candidate_key,
        "bob_candidate_key": bob_candidate_key,
    }


def run_bb84_quantum_simulation(
    num_qubits: int = 100,
    eve_enabled: bool = False,
    noise_level: str = "OFF",
    test_sample_fraction: float = 0.33,
    educational_acceptance_threshold: float = 0.11,
    random_seed: Optional[int] = None,
):
    """
    Runs the complete BB84 protocol simulation with optional Eve and Noise.
    When random_seed is provided, execution is 100% reproducible.
    """
    if random_seed is not None:
        random.seed(random_seed)

    eve_status = "ON (Intercept-Resend)" if eve_enabled else "OFF (Secure Channel)"
    noise_str = noise_level.upper() if noise_level.upper() in NOISE_CONFIGS else "OFF"
    noise_rate = NOISE_CONFIGS[noise_str]

    print("\n" + "=" * 85)
    print(f"      Q-Crypt: Quantum BB84 Simulator [Eve: {eve_status} | Noise: {noise_str} ({noise_rate*100:.1f}%)]")
    print(f"      Total Qubits: {num_qubits} | Acceptance Threshold: {educational_acceptance_threshold * 100:.1f}%")
    print("=" * 85)

    noise_model = build_noise_model(noise_str)
    simulator = AerSimulator(noise_model=noise_model) if noise_model else AerSimulator()

    alice_bits = []
    alice_bases = []
    states_prepared = []
    eve_bases = []
    eve_results = []
    bob_bases = []
    bob_results = []
    matching_indices = []
    alice_sifted_key = []
    bob_sifted_key = []

    # -------------------------------------------------------------
    # Stage 1: Quantum Transmission
    # -------------------------------------------------------------
    for i in range(num_qubits):
        a_bit = random.choice([0, 1])
        a_basis = random.choice(["Z", "X"])
        a_state = get_state_symbol(a_bit, a_basis)

        alice_bits.append(a_bit)
        alice_bases.append(a_basis)
        states_prepared.append(a_state)

        # Alice prepares quantum state
        qc_alice = prepare_qubit(a_bit, a_basis)

        eve_seed = (random_seed * 10000 + i * 2) if random_seed is not None else None
        bob_seed = (random_seed * 10000 + i * 2 + 1) if random_seed is not None else None

        # Eve interception (if active)
        if eve_enabled:
            e_basis = random.choice(["Z", "X"])
            e_measured = measure_qubit(qc_alice, e_basis, simulator, seed=eve_seed)
            eve_bases.append(e_basis)
            eve_results.append(e_measured)

            # Eve prepares replacement photon
            qc_transmitted = prepare_qubit(e_measured, e_basis)
        else:
            eve_bases.append("-")
            eve_results.append("-")
            qc_transmitted = qc_alice

        # Bob measures
        b_basis = random.choice(["Z", "X"])
        bob_bases.append(b_basis)

        b_measured = measure_qubit(qc_transmitted, b_basis, simulator, seed=bob_seed)
        bob_results.append(b_measured)

    # -------------------------------------------------------------
    # Stage 2: Basis Sifting
    # -------------------------------------------------------------
    for i in range(num_qubits):
        if alice_bases[i] == bob_bases[i]:
            matching_indices.append(i)
            alice_sifted_key.append(alice_bits[i])
            bob_sifted_key.append(bob_results[i])

    # -------------------------------------------------------------
    # Stage 3: QBER Parameter Estimation
    # -------------------------------------------------------------
    qber_stats = estimate_qber_and_extract_key(
        alice_sifted_key,
        bob_sifted_key,
        test_sample_fraction=test_sample_fraction,
    )

    num_test_bits = qber_stats["num_test_bits"]
    num_errors = qber_stats["num_errors"]
    qber = qber_stats["qber"]
    alice_candidate = qber_stats["alice_candidate_key"]
    bob_candidate = qber_stats["bob_candidate_key"]

    # -------------------------------------------------------------
    # Display Transmission Table (First 20 rows if num_qubits > 20)
    # -------------------------------------------------------------
    display_limit = min(num_qubits, 20)
    print("\n" + "=" * 90)
    if eve_enabled:
        print(f"{'Idx':^5}|{'Alice Bit':^10}|{'Alice Bas':^10}|{'Eve Bas':^8}|{'Eve Res':^8}|{'Bob Bas':^8}|{'Bob Res':^8}|{'Match?':^7}|{'Sifted':^7}")
        print("=" * 90)
        matching_set = set(matching_indices)
        for i in range(display_limit):
            matched = "YES" if i in matching_set else "NO"
            sifted = str(alice_bits[i]) if i in matching_set else "-"
            print(f"{i:^5}|{alice_bits[i]:^10}|{alice_bases[i]:^10}|{eve_bases[i]:^8}|{eve_results[i]:^8}|{bob_bases[i]:^8}|{bob_results[i]:^8}|{matched:^7}|{sifted:^7}")
    else:
        print(f"{'Idx':^5}|{'Alice Bit':^10}|{'Alice Bas':^10}|{'State':^8}|{'Bob Bas':^8}|{'Bob Res':^8}|{'Match?':^7}|{'Sifted':^7}")
        print("=" * 90)
        matching_set = set(matching_indices)
        for i in range(display_limit):
            matched = "YES" if i in matching_set else "NO"
            sifted = str(alice_bits[i]) if i in matching_set else "-"
            print(f"{i:^5}|{alice_bits[i]:^10}|{alice_bases[i]:^10}|{states_prepared[i]:^8}|{bob_bases[i]:^8}|{bob_results[i]:^8}|{matched:^7}|{sifted:^7}")
    print("=" * 90)

    if num_qubits > display_limit:
        print(f"[... table truncated for display; showing first {display_limit} of {num_qubits} qubits ...]")

    # -------------------------------------------------------------
    # Display Summary & Findings
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("                     BB84 PROTOCOL SUMMARY & QBER")
    print("=" * 80)
    print(f"Eve Status                        : {'ON (Intercept-Resend)' if eve_enabled else 'OFF'}")
    print(f"Noise Level                       : {noise_str} ({noise_rate * 100:.1f}% channel error probability)")
    print(f"Total qubits sent                 : {num_qubits}")
    print(f"Matching bases                    : {len(matching_indices)}")
    print(f"Sifted key length                 : {len(alice_sifted_key)} bits")
    print(f"Test bits sampled                 : {num_test_bits} bits")
    print(f"Errors detected in test bits      : {num_errors}")
    print(f"Observed QBER                     : {qber:.4f} ({qber * 100:.2f}%)")
    print(f"Educational Acceptance Threshold  : {educational_acceptance_threshold:.4f} ({educational_acceptance_threshold * 100:.1f}%)")
    print(f"Remaining candidate key length    : {len(alice_candidate)} bits")

    def format_key_preview(key_list, max_len=30):
        s = "".join(map(str, key_list))
        return s if len(s) <= max_len else s[:max_len] + f"... ({len(s)} bits total)"

    print("-" * 80)
    print(f"Alice's Sifted Key                : {format_key_preview(alice_sifted_key)}")
    print(f"Bob's Sifted Key                  : {format_key_preview(bob_sifted_key)}")
    print("-" * 80)
    print(f"Alice's Candidate Key             : {format_key_preview(alice_candidate)}")
    print(f"Bob's Candidate Key               : {format_key_preview(bob_candidate)}")
    print("-" * 80)

    # Cryptographic verdict
    if qber <= educational_acceptance_threshold:
        print(f"[PASSED] Observed QBER ({qber * 100:.2f}%) <= Acceptance Threshold ({educational_acceptance_threshold * 100:.1f}%).")
        print("          Channel disturbance within acceptable limits. Candidate key accepted!")
    else:
        print(f"[ABORTED] Observed QBER ({qber * 100:.2f}%) > Acceptance Threshold ({educational_acceptance_threshold * 100:.1f}%).")
        print("          Excessive errors (Noise or Eavesdropper) detected! Key discarded.")
    print("=" * 80)


def main():
    print("=" * 80)
    print("      Q-Crypt: Quantum BB84 Simulator with Eve & Noise")
    print("=" * 80)

    # 1. Ask for number of qubits
    user_qubits = input("Enter number of qubits to simulate (e.g. 20, 100; default 100): ").strip()
    if user_qubits.isdigit() and int(user_qubits) > 0:
        num_qubits = int(user_qubits)
    else:
        num_qubits = 100
        print(f"[Using default: {num_qubits} qubits]")

    # 2. Ask for Eve toggle
    eve_input = input("Enable Eve intercept-resend attack? (ON / OFF; default OFF): ").strip().upper()
    eve_enabled = eve_input in ["ON", "Y", "YES", "TRUE", "1"]

    # 3. Ask for Noise Level
    print("\nSelect Quantum Channel Noise Level:")
    print("  - OFF    (0.0%  error - ideal noiseless)")
    print("  - LOW    (3.0%  error - optical fiber)")
    print("  - MEDIUM (8.0%  error - realistic channel loss)")
    print("  - HIGH   (20.0% error - severe turbulence)")
    noise_input = input("Enter Noise Level (OFF / LOW / MEDIUM / HIGH; default OFF): ").strip().upper()
    noise_level = noise_input if noise_input in NOISE_CONFIGS else "OFF"

    # 4. Configurable threshold
    threshold_input = input("\nEnter educational acceptance threshold (default 0.11 for 11%): ").strip()
    try:
        threshold = float(threshold_input) if threshold_input else 0.11
    except ValueError:
        threshold = 0.11

    run_bb84_quantum_simulation(
        num_qubits=num_qubits,
        eve_enabled=eve_enabled,
        noise_level=noise_level,
        educational_acceptance_threshold=threshold,
    )


if __name__ == "__main__":
    main()
