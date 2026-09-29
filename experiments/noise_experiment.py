"""
====================================================================
Experiment 3: BB84 Quantum Noise Simulation (Qiskit Aer Noise)
====================================================================
Educational Objective (Class 12 Physics / CS):
Investigate how environmental noise and hardware imperfections in the
quantum channel (depolarizing noise) induce errors in the transmitted
qubits, elevating the Quantum Bit Error Rate (QBER) even without an eavesdropper.

--------------------------------------------------------------------
Noise Levels Defined:
--------------------------------------------------------------------
1. OFF    (Error Rate:  0.0%) - Ideal, perfect noiseless channel.
2. LOW    (Error Rate:  3.0%) - High-grade optical fiber transmission.
3. MEDIUM (Error Rate:  8.0%) - Typical real-world fiber attenuation & detector dark counts.
4. HIGH   (Error Rate: 20.0%) - Severe atmospheric turbulence / noisy quantum channel.

--------------------------------------------------------------------
Key Scientific Insights:
--------------------------------------------------------------------
- Depolarizing noise randomly distorts the quantum state of a photon during
  transmission or gate operations.
- As noise increases, the probability of bit flips and phase flips rises,
  leading to higher measured QBER on the matching basis bits.
- Because simulations use a finite number of qubits (e.g., 100 qubits),
  the observed QBER will statistically fluctuate around the expected error level.
====================================================================
"""

import random
import sys

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
    Constructs a Qiskit Aer NoiseModel based on the chosen level.
    Uses depolarizing error on single-qubit gates ('x', 'h') and readout error.
    """
    prob = NOISE_CONFIGS.get(noise_level.upper(), 0.0)
    if prob <= 0.0:
        return None

    noise_model = NoiseModel()

    # 1. Depolarizing quantum error for single-qubit gates
    gate_error = depolarizing_error(prob, 1)
    noise_model.add_all_qubit_quantum_error(gate_error, ["x", "h"])

    # 2. Readout (measurement detector) error
    readout_error = ReadoutError([[1.0 - prob, prob], [prob, 1.0 - prob]])
    noise_model.add_all_qubit_readout_error(readout_error)

    return noise_model


def prepare_qubit(bit: int, basis: str) -> QuantumCircuit:
    """Constructs a 1-qubit quantum circuit for Alice's state."""
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == "X":
        qc.h(0)
    qc.barrier()
    return qc


def measure_qubit(qc: QuantumCircuit, basis: str, simulator: AerSimulator) -> int:
    """Applies Bob's basis transformation and measures the qubit."""
    if basis == "X":
        qc.h(0)
    qc.measure(0, 0)

    job = simulator.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()

    return int(list(counts.keys())[0])


def run_single_noise_simulation(
    num_qubits: int = 100,
    noise_level: str = "OFF",
    test_sample_fraction: float = 0.33,
    educational_threshold: float = 0.11,
):
    """
    Runs a single BB84 transmission with Eve OFF at the specified noise level.
    Returns a dictionary of statistical results.
    """
    noise_model = build_noise_model(noise_level)
    simulator = AerSimulator(noise_model=noise_model) if noise_model else AerSimulator()

    alice_bits = []
    alice_bases = []
    bob_bases = []
    bob_results = []
    matching_indices = []
    alice_sifted_key = []
    bob_sifted_key = []

    # 1. Quantum Transmission
    for i in range(num_qubits):
        a_bit = random.choice([0, 1])
        a_basis = random.choice(["Z", "X"])
        alice_bits.append(a_bit)
        alice_bases.append(a_basis)

        qc = prepare_qubit(a_bit, a_basis)

        b_basis = random.choice(["Z", "X"])
        bob_bases.append(b_basis)

        b_measured = measure_qubit(qc, b_basis, simulator)
        bob_results.append(b_measured)

    # 2. Basis Sifting
    for i in range(num_qubits):
        if alice_bases[i] == bob_bases[i]:
            matching_indices.append(i)
            alice_sifted_key.append(alice_bits[i])
            bob_sifted_key.append(bob_results[i])

    sifted_len = len(alice_sifted_key)
    if sifted_len == 0:
        return {
            "noise_level": noise_level,
            "total_qubits": num_qubits,
            "matching_bases": 0,
            "sifted_key_len": 0,
            "test_bits": 0,
            "errors": 0,
            "qber": 0.0,
            "candidate_key_len": 0,
            "passed": False,
        }

    # 3. Parameter Estimation (Test Bits Sampling)
    num_test_bits = max(1, int(sifted_len * test_sample_fraction))
    if num_test_bits >= sifted_len and sifted_len > 1:
        num_test_bits = sifted_len // 2

    test_indices = sorted(random.sample(range(sifted_len), num_test_bits))
    test_set = set(test_indices)

    errors = sum(1 for idx in test_indices if alice_sifted_key[idx] != bob_sifted_key[idx])
    qber = errors / num_test_bits if num_test_bits > 0 else 0.0
    candidate_len = sifted_len - num_test_bits
    passed = qber <= educational_threshold

    return {
        "noise_level": noise_level,
        "total_qubits": num_qubits,
        "matching_bases": len(matching_indices),
        "sifted_key_len": sifted_len,
        "test_bits": num_test_bits,
        "errors": errors,
        "qber": qber,
        "candidate_key_len": candidate_len,
        "passed": passed,
    }


def run_comparative_noise_experiment(num_qubits: int = 100, threshold: float = 0.11):
    """
    Executes BB84 across all four noise levels (OFF, LOW, MEDIUM, HIGH)
    and displays a comparative summary table.
    """
    print("\n" + "=" * 85)
    print(f"      Q-Crypt: Comparative Quantum Noise Experiment ({num_qubits} Qubits Per Level)")
    print(f"      Eve: OFF | Educational Acceptance Threshold: {threshold * 100:.1f}%")
    print("=" * 85)

    levels = ["OFF", "LOW", "MEDIUM", "HIGH"]
    results = []

    for level in levels:
        res = run_single_noise_simulation(
            num_qubits=num_qubits,
            noise_level=level,
            educational_threshold=threshold,
        )
        results.append(res)

    # Print Comparative Table
    print("\n" + "=" * 85)
    print(f"{'Noise Level':^13}|{'Noise Prob':^12}|{'Sifted Key':^12}|{'Test Bits':^11}|{'Errors':^8}|{'Observed QBER':^15}|{'Status':^10}")
    print("=" * 85)

    for r in results:
        level_str = r["noise_level"]
        prob_str = f"{NOISE_CONFIGS[level_str] * 100:.1f}%"
        sifted_str = f"{r['sifted_key_len']} bits"
        test_str = f"{r['test_bits']} bits"
        err_str = str(r["errors"])
        qber_str = f"{r['qber'] * 100:.2f}%"
        status_str = "ACCEPTED" if r["passed"] else "ABORTED"
        print(f"{level_str:^13}|{prob_str:^12}|{sifted_str:^12}|{test_str:^11}|{err_str:^8}|{qber_str:^15}|{status_str:^10}")
    print("=" * 85)

    # Scientific Observations
    print("\n" + "=" * 85)
    print("                        EDUCATIONAL OBSERVATIONS")
    print("=" * 85)
    print("1. Noise OFF    : In a noiseless environment, matching bases yield QBER = 0.00%.")
    print("2. Noise LOW    : Slight channel disturbance introduces small errors (often <= 11% threshold).")
    print("3. Noise MEDIUM : Moderate noise pushes error rates closer to or slightly above threshold.")
    print("4. Noise HIGH   : Severe noise creates frequent bit flips, consistently aborting key generation.")
    print("\n*Statistical Note*: Because each run uses a finite random sample, observed QBER values")
    print("will naturally fluctuate around the physical channel noise rate between separate runs.")
    print("=" * 85)


def main():
    print("=" * 80)
    print("           Q-Crypt: Quantum Noise Simulator (Qiskit Aer)")
    print("=" * 80)

    print("\nSelect Mode:")
    print("  [1] Run Comparative Experiment across ALL noise levels (OFF, LOW, MEDIUM, HIGH)")
    print("  [2] Run a Single Simulation with a chosen noise level")

    choice = input("\nEnter choice (1 or 2; default 1): ").strip()

    num_qubits_input = input("Enter number of qubits per run (e.g. 100; default 100): ").strip()
    num_qubits = int(num_qubits_input) if num_qubits_input.isdigit() and int(num_qubits_input) > 0 else 100

    threshold_input = input("Enter educational acceptance threshold (default 0.11 for 11%): ").strip()
    try:
        threshold = float(threshold_input) if threshold_input else 0.11
    except ValueError:
        threshold = 0.11

    if choice == "2":
        print("\nAvailable Noise Levels: OFF, LOW, MEDIUM, HIGH")
        level_input = input("Choose noise level (default MEDIUM): ").strip().upper()
        noise_level = level_input if level_input in NOISE_CONFIGS else "MEDIUM"

        res = run_single_noise_simulation(
            num_qubits=num_qubits,
            noise_level=noise_level,
            educational_threshold=threshold,
        )

        print("\n" + "=" * 70)
        print(f"            Single Simulation Result [Noise: {res['noise_level']}]")
        print("=" * 70)
        print(f"Total Qubits Sent              : {res['total_qubits']}")
        print(f"Matching Bases (Sifted Key)    : {res['sifted_key_len']} bits")
        print(f"Test Bits Sampled              : {res['test_bits']} bits")
        print(f"Errors Detected in Test Sample : {res['errors']}")
        print(f"Observed QBER                  : {res['qber']:.4f} ({res['qber'] * 100:.2f}%)")
        print(f"Remaining Candidate Key Length : {res['candidate_key_len']} bits")
        print(f"Verdict                        : {'ACCEPTED' if res['passed'] else 'ABORTED (Excessive Noise)'}")
        print("=" * 70)
    else:
        run_comparative_noise_experiment(num_qubits=num_qubits, threshold=threshold)


if __name__ == "__main__":
    main()
