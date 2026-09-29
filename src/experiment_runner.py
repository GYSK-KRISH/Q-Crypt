"""
====================================================================
Q-Crypt: Unified Experiment Runner & Multi-Trial Statistical Engine
====================================================================
Educational Objective (Class 12 Physics / CS):
Provides a clean, modular, and configurable engine to simulate:
1. Single BB84 runs (with customizable Eve and Noise).
2. Multi-trial statistical experiments (Monte Carlo simulations) that:
   - Repeat the BB84 protocol across N iterations.
   - Calculate Average, Minimum, and Maximum QBER.
   - Calculate Average Sifted Key Length.
   - Save all trial data to a CSV file inside the 'experiments/' folder.
====================================================================
"""

from dataclasses import dataclass, asdict
import csv
from datetime import datetime
import os
import random
import sys
from typing import List, Optional

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

# Predefined noise probability mapping
NOISE_PROBABILITIES = {
    "OFF": 0.00,
    "LOW": 0.03,
    "MEDIUM": 0.08,
    "HIGH": 0.20,
}


@dataclass
class ExperimentConfig:
    """
    Configuration parameters for a Q-Crypt BB84 experiment.
    """
    num_qubits: int = 100
    eve_enabled: bool = False
    noise_enabled: bool = False
    noise_level: str = "OFF"                  # 'OFF', 'LOW', 'MEDIUM', 'HIGH'
    test_sample_size: Optional[int] = None    # Exact number of test bits (optional)
    test_sample_fraction: float = 0.33        # Fraction of sifted key to test
    qber_threshold: float = 0.11              # Acceptance threshold (e.g. 11%)
    random_seed: Optional[int] = None         # Seed for reproducible simulations


@dataclass
class ExperimentResult:
    """
    Structured results returned from an executed single BB84 trial.
    """
    total_qubits: int
    alice_bits: List[int]
    alice_bases: List[str]
    bob_bases: List[str]
    bob_results: List[int]
    matching_positions: List[int]
    alice_sifted_key: List[int]
    bob_sifted_key: List[int]
    test_sample_indices: List[int]
    test_sample_alice: List[int]
    test_sample_bob: List[int]
    errors: int
    qber: float
    alice_candidate_key: List[int]
    bob_candidate_key: List[int]
    status: str                               # 'PASSED' or 'ABORTED'

    def to_dict(self) -> dict:
        """Converts the dataclass result into a standard Python dictionary."""
        return asdict(self)


@dataclass
class MultiExperimentSummary:
    """
    Aggregated statistical summary from repeated BB84 trials.
    """
    num_repetitions: int
    num_qubits_per_run: int
    eve_enabled: bool
    noise_level: str
    avg_qber: float
    min_qber: float
    max_qber: float
    avg_sifted_key_len: float
    avg_candidate_key_len: float
    passed_runs: int
    aborted_runs: int
    trials: List[ExperimentResult]
    csv_filepath: Optional[str] = None


def build_noise_model(noise_level: str) -> Optional[NoiseModel]:
    """Builds a Qiskit Aer NoiseModel for the specified level."""
    prob = NOISE_PROBABILITIES.get(noise_level.upper(), 0.0)
    if prob <= 0.0:
        return None

    noise_model = NoiseModel()
    gate_err = depolarizing_error(prob, 1)
    noise_model.add_all_qubit_quantum_error(gate_err, ["x", "h"])

    readout_err = ReadoutError([[1.0 - prob, prob], [prob, 1.0 - prob]])
    noise_model.add_all_qubit_readout_error(readout_err)
    return noise_model


def prepare_qubit(bit: int, basis: str) -> QuantumCircuit:
    """Creates a 1-qubit circuit in the appropriate BB84 state."""
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == "X":
        qc.h(0)
    qc.barrier()
    return qc


def measure_qubit(
    qc: QuantumCircuit,
    basis: str,
    simulator: AerSimulator,
    seed: Optional[int] = None,
) -> int:
    """Measures a qubit in the specified basis (Z or X) for 1 shot."""
    if basis == "X":
        qc.h(0)
    qc.measure(0, 0)

    run_kwargs = {"shots": 1}
    if seed is not None:
        run_kwargs["seed_simulator"] = seed

    job = simulator.run(qc, **run_kwargs)
    result = job.result()
    counts = result.get_counts()
    return int(list(counts.keys())[0])


def run_experiment(config: ExperimentConfig) -> ExperimentResult:
    """
    Executes a single BB84 simulation based on the provided configuration.
    When config.random_seed is supplied, the entire simulation (classical bit/basis
    selection, quantum noise, and measurement collapse) is 100% reproducible.
    """
    if config.random_seed is not None:
        random.seed(config.random_seed)
        try:
            import numpy as np
            np.random.seed(config.random_seed)
        except ImportError:
            pass

    effective_noise = config.noise_level if config.noise_enabled else "OFF"
    noise_model = build_noise_model(effective_noise)
    simulator = AerSimulator(noise_model=noise_model) if noise_model else AerSimulator()

    alice_bits = []
    alice_bases = []
    bob_bases = []
    bob_results = []
    matching_positions = []
    alice_sifted_key = []
    bob_sifted_key = []

    # Transmission Phase
    for i in range(config.num_qubits):
        a_bit = random.choice([0, 1])
        a_basis = random.choice(["Z", "X"])
        alice_bits.append(a_bit)
        alice_bases.append(a_basis)

        qc_alice = prepare_qubit(a_bit, a_basis)

        # Deterministic sub-seeds derived from base seed if configured
        eve_seed = (config.random_seed * 10000 + i * 2) if config.random_seed is not None else None
        bob_seed = (config.random_seed * 10000 + i * 2 + 1) if config.random_seed is not None else None

        # Eve Interception (if enabled)
        if config.eve_enabled:
            e_basis = random.choice(["Z", "X"])
            e_measured = measure_qubit(qc_alice, e_basis, simulator, seed=eve_seed)
            qc_transmitted = prepare_qubit(e_measured, e_basis)
        else:
            qc_transmitted = qc_alice

        # Bob Measurement
        b_basis = random.choice(["Z", "X"])
        bob_bases.append(b_basis)

        b_measured = measure_qubit(qc_transmitted, b_basis, simulator, seed=bob_seed)
        bob_results.append(b_measured)

    # Basis Sifting Phase
    for i in range(config.num_qubits):
        if alice_bases[i] == bob_bases[i]:
            matching_positions.append(i)
            alice_sifted_key.append(alice_bits[i])
            bob_sifted_key.append(bob_results[i])

    sifted_len = len(alice_sifted_key)

    if sifted_len == 0:
        return ExperimentResult(
            total_qubits=config.num_qubits,
            alice_bits=alice_bits,
            alice_bases=alice_bases,
            bob_bases=bob_bases,
            bob_results=bob_results,
            matching_positions=[],
            alice_sifted_key=[],
            bob_sifted_key=[],
            test_sample_indices=[],
            test_sample_alice=[],
            test_sample_bob=[],
            errors=0,
            qber=0.0,
            alice_candidate_key=[],
            bob_candidate_key=[],
            status="ABORTED",
        )

    # Parameter Estimation (Test Sample Sampling)
    if config.test_sample_size is not None:
        num_test_bits = min(config.test_sample_size, sifted_len)
    else:
        num_test_bits = max(1, int(sifted_len * config.test_sample_fraction))
        if num_test_bits >= sifted_len and sifted_len > 1:
            num_test_bits = sifted_len // 2

    test_indices = sorted(random.sample(range(sifted_len), num_test_bits))
    test_set = set(test_indices)

    test_sample_alice = [alice_sifted_key[i] for i in test_indices]
    test_sample_bob = [bob_sifted_key[i] for i in test_indices]

    errors = sum(1 for a, b in zip(test_sample_alice, test_sample_bob) if a != b)
    qber = errors / num_test_bits if num_test_bits > 0 else 0.0

    # Extract Candidate Key
    alice_candidate_key = [
        alice_sifted_key[i] for i in range(sifted_len) if i not in test_set
    ]
    bob_candidate_key = [
        bob_sifted_key[i] for i in range(sifted_len) if i not in test_set
    ]

    status = "PASSED" if qber <= config.qber_threshold else "ABORTED"

    return ExperimentResult(
        total_qubits=config.num_qubits,
        alice_bits=alice_bits,
        alice_bases=alice_bases,
        bob_bases=bob_bases,
        bob_results=bob_results,
        matching_positions=matching_positions,
        alice_sifted_key=alice_sifted_key,
        bob_sifted_key=bob_sifted_key,
        test_sample_indices=test_indices,
        test_sample_alice=test_sample_alice,
        test_sample_bob=test_sample_bob,
        errors=errors,
        qber=qber,
        alice_candidate_key=alice_candidate_key,
        bob_candidate_key=bob_candidate_key,
        status=status,
    )


def save_trials_to_csv(
    trials: List[ExperimentResult],
    num_qubits: int,
    eve_enabled: bool,
    noise_level: str,
    output_dir: str = "experiments",
    filename: Optional[str] = None,
) -> str:
    """
    Saves trial results to a CSV file with detailed metrics per run.
    """
    os.makedirs(output_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        eve_tag = "eve_ON" if eve_enabled else "eve_OFF"
        noise_tag = f"noise_{noise_level.upper()}"
        filename = f"bb84_multi_{eve_tag}_{noise_tag}_{timestamp}.csv"

    filepath = os.path.join(output_dir, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "Trial",
            "Total_Qubits",
            "Eve_Status",
            "Noise_Level",
            "Matching_Bases",
            "Sifted_Key_Len",
            "Test_Bits",
            "Errors",
            "QBER",
            "QBER_Percentage",
            "Candidate_Key_Len",
            "Status",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, t in enumerate(trials, start=1):
            writer.writerow({
                "Trial": idx,
                "Total_Qubits": t.total_qubits,
                "Eve_Status": "ON" if eve_enabled else "OFF",
                "Noise_Level": noise_level.upper(),
                "Matching_Bases": len(t.matching_positions),
                "Sifted_Key_Len": len(t.alice_sifted_key),
                "Test_Bits": len(t.test_sample_indices),
                "Errors": t.errors,
                "QBER": f"{t.qber:.4f}",
                "QBER_Percentage": f"{t.qber * 100:.2f}%",
                "Candidate_Key_Len": len(t.alice_candidate_key),
                "Status": t.status,
            })

    return filepath


def run_multi_experiment(
    num_qubits: int = 100,
    num_repetitions: int = 10,
    eve_enabled: bool = False,
    noise_level: str = "OFF",
    test_sample_size: Optional[int] = None,
    test_sample_fraction: float = 0.33,
    qber_threshold: float = 0.11,
    save_csv: bool = True,
    csv_filename: Optional[str] = None,
    output_dir: str = "experiments",
) -> MultiExperimentSummary:
    """
    Executes the BB84 protocol repeatedly across multiple independent runs,
    calculates statistical aggregates (Avg/Min/Max QBER, Sifted Length),
    and saves the raw trial data as a CSV file.
    """
    noise_enabled = (noise_level.upper() != "OFF")
    trials: List[ExperimentResult] = []

    for _ in range(num_repetitions):
        config = ExperimentConfig(
            num_qubits=num_qubits,
            eve_enabled=eve_enabled,
            noise_enabled=noise_enabled,
            noise_level=noise_level,
            test_sample_size=test_sample_size,
            test_sample_fraction=test_sample_fraction,
            qber_threshold=qber_threshold,
            random_seed=None,  # Each repetition is an independent random experiment
        )
        res = run_experiment(config)
        trials.append(res)

    # Compute Statistical Aggregates
    qber_list = [t.qber for t in trials]
    sifted_lens = [len(t.alice_sifted_key) for t in trials]
    candidate_lens = [len(t.alice_candidate_key) for t in trials]

    avg_qber = sum(qber_list) / len(qber_list) if qber_list else 0.0
    min_qber = min(qber_list) if qber_list else 0.0
    max_qber = max(qber_list) if qber_list else 0.0
    avg_sifted_key_len = sum(sifted_lens) / len(sifted_lens) if sifted_lens else 0.0
    avg_candidate_key_len = sum(candidate_lens) / len(candidate_lens) if candidate_lens else 0.0

    passed_runs = sum(1 for t in trials if t.status == "PASSED")
    aborted_runs = sum(1 for t in trials if t.status == "ABORTED")

    # Save to CSV
    csv_filepath = None
    if save_csv:
        csv_filepath = save_trials_to_csv(
            trials=trials,
            num_qubits=num_qubits,
            eve_enabled=eve_enabled,
            noise_level=noise_level,
            output_dir=output_dir,
            filename=csv_filename,
        )

    return MultiExperimentSummary(
        num_repetitions=num_repetitions,
        num_qubits_per_run=num_qubits,
        eve_enabled=eve_enabled,
        noise_level=noise_level,
        avg_qber=avg_qber,
        min_qber=min_qber,
        max_qber=max_qber,
        avg_sifted_key_len=avg_sifted_key_len,
        avg_candidate_key_len=avg_candidate_key_len,
        passed_runs=passed_runs,
        aborted_runs=aborted_runs,
        trials=trials,
        csv_filepath=csv_filepath,
    )


def display_multi_experiment_summary(summary: MultiExperimentSummary):
    """Prints a neat statistical report of repeated BB84 trials."""
    eve_status = "ON (Intercept-Resend Active)" if summary.eve_enabled else "OFF (Secure)"
    print("\n" + "=" * 80)
    print("               Q-CRYPT MULTI-TRIAL EXPERIMENT REPORT")
    print("=" * 80)
    print(f"Total Repetitions (Trials)     : {summary.num_repetitions}")
    print(f"Qubits Transmitted Per Trial   : {summary.num_qubits_per_run}")
    print(f"Eve Status                     : {eve_status}")
    print(f"Quantum Noise Level            : {summary.noise_level.upper()} ({NOISE_PROBABILITIES.get(summary.noise_level.upper(), 0.0)*100:.1f}%)")
    print("-" * 80)
    print(f"Average Sifted Key Length      : {summary.avg_sifted_key_len:.1f} bits (Efficiency: ~{(summary.avg_sifted_key_len/summary.num_qubits_per_run)*100:.1f}%)")
    print(f"Average Candidate Key Length   : {summary.avg_candidate_key_len:.1f} bits")
    print("-" * 80)
    print(f"Average QBER                   : {summary.avg_qber:.4f} ({summary.avg_qber * 100:.2f}%)")
    print(f"Minimum QBER                   : {summary.min_qber:.4f} ({summary.min_qber * 100:.2f}%)")
    print(f"Maximum QBER                   : {summary.max_qber:.4f} ({summary.max_qber * 100:.2f}%)")
    print("-" * 80)
    print(f"Trials Passed (Key Accepted)   : {summary.passed_runs} / {summary.num_repetitions} ({summary.passed_runs/summary.num_repetitions*100:.1f}%)")
    print(f"Trials Aborted (Key Discarded) : {summary.aborted_runs} / {summary.num_repetitions} ({summary.aborted_runs/summary.num_repetitions*100:.1f}%)")

    if summary.csv_filepath:
        print("-" * 80)
        print(f"CSV Results Saved To          : {summary.csv_filepath}")
    print("=" * 80)


def display_experiment_result(result: ExperimentResult, max_display_rows: int = 20):
    """Prints a structured, formatted display of a single experiment result."""
    print("\n" + "=" * 80)
    print("                     Q-CRYPT EXPERIMENT RESULTS")
    print("=" * 80)

    display_rows = min(result.total_qubits, max_display_rows)
    print(f"\n--- Transmission Log (First {display_rows} of {result.total_qubits} Qubits) ---")
    print(f"{'Idx':^5}|{'Alice Bit':^10}|{'Alice Bas':^10}|{'Bob Bas':^10}|{'Bob Res':^10}|{'Match?':^8}")
    print("-" * 60)
    matching_set = set(result.matching_positions)
    for i in range(display_rows):
        matched = "YES" if i in matching_set else "NO"
        print(f"{i:^5}|{result.alice_bits[i]:^10}|{result.alice_bases[i]:^10}|{result.bob_bases[i]:^10}|{result.bob_results[i]:^10}|{matched:^8}")
    print("-" * 60)

    print("\n--- Summary Metrics ---")
    print(f"Total Qubits Sent              : {result.total_qubits}")
    print(f"Matching Bases (Sifted Bits)   : {len(result.matching_positions)}")
    print(f"Sifted Key Length              : {len(result.alice_sifted_key)} bits")
    print(f"Test Sample Size               : {len(result.test_sample_indices)} bits")
    print(f"Errors Found in Test Sample    : {result.errors}")
    print(f"Measured QBER                  : {result.qber:.4f} ({result.qber * 100:.2f}%)")
    print(f"Remaining Candidate Key Length : {len(result.alice_candidate_key)} bits")
    print(f"Final Protocol Status          : {result.status}")

    def key_str(k):
        s = "".join(map(str, k))
        return s if len(s) <= 35 else s[:35] + f"... ({len(s)} bits)"

    print("\n--- Generated Keys ---")
    print(f"Alice Sifted Key   : {key_str(result.alice_sifted_key)}")
    print(f"Bob Sifted Key     : {key_str(result.bob_sifted_key)}")
    print(f"Alice Candidate Key: {key_str(result.alice_candidate_key)}")
    print(f"Bob Candidate Key  : {key_str(result.bob_candidate_key)}")
    print("=" * 80)


def main():
    print("=" * 75)
    print("         Q-Crypt: Interactive BB84 Experiment Runner")
    print("=" * 75)

    print("\nSelect Experiment Mode:")
    print("  [1] Single BB84 Transmission Simulation")
    print("  [2] Multi-Trial Statistical Experiment (with CSV export)")

    mode_choice = input("\nEnter choice (1 or 2; default 1): ").strip()

    # 1. Number of qubits
    n_input = input("\n1. Number of qubits per run (e.g. 50, 100; default 100): ").strip()
    num_qubits = int(n_input) if n_input.isdigit() and int(n_input) > 0 else 100

    # 2. Eve toggle
    eve_input = input("2. Enable Eve Intercept-Resend? (ON/OFF; default OFF): ").strip().upper()
    eve_enabled = eve_input in ["ON", "Y", "YES", "TRUE", "1"]

    # 3. Noise level
    print("3. Select Quantum Channel Noise Level: OFF, LOW, MEDIUM, HIGH")
    noise_input = input("   Enter Noise Level (default OFF): ").strip().upper()
    noise_level = noise_input if noise_input in NOISE_PROBABILITIES else "OFF"

    # 4. Threshold
    thresh_input = input("4. QBER Acceptance Threshold (default 0.11 for 11%): ").strip()
    try:
        threshold = float(thresh_input) if thresh_input else 0.11
    except ValueError:
        threshold = 0.11

    if mode_choice == "2":
        # Repetitions
        rep_input = input("5. Number of repetitions/trials (e.g. 10, 20, 50; default 10): ").strip()
        num_reps = int(rep_input) if rep_input.isdigit() and int(rep_input) > 0 else 10

        summary = run_multi_experiment(
            num_qubits=num_qubits,
            num_repetitions=num_reps,
            eve_enabled=eve_enabled,
            noise_level=noise_level,
            qber_threshold=threshold,
            save_csv=True,
        )
        display_multi_experiment_summary(summary)
    else:
        sample_input = input("5. Test Sample Size in bits (or press Enter for default 33%): ").strip()
        test_sample_size = int(sample_input) if sample_input.isdigit() and int(sample_input) > 0 else None

        seed_input = input("6. Random Seed for Reproducibility (optional, press Enter to skip): ").strip()
        random_seed = int(seed_input) if seed_input.isdigit() else None

        config = ExperimentConfig(
            num_qubits=num_qubits,
            eve_enabled=eve_enabled,
            noise_enabled=(noise_level != "OFF"),
            noise_level=noise_level,
            test_sample_size=test_sample_size,
            qber_threshold=threshold,
            random_seed=random_seed,
        )
        result = run_experiment(config)
        display_experiment_result(result)


if __name__ == "__main__":
    main()
