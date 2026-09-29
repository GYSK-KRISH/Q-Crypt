"""
====================================================================
Experiment 4: Multi-Trial Statistical BB84 Experiment
====================================================================
Educational Objective (Class 12 Physics / CS Project Data Collection):
Runs repeated independent simulations of the BB84 protocol to gather
large-sample statistical evidence on:
- Average, Minimum, and Maximum QBER.
- Average Sifted Key Length and Candidate Key Yield.
- Protocol Acceptance vs. Abort rates under various physical conditions.

All trial data is saved as a clean CSV in the 'experiments/' directory
for easy plotting, graphing, and inclusion in project reports.
====================================================================
"""

import sys
import os

# Ensure the project root and 'src' directory are in Python's search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.experiment_runner import (
    run_multi_experiment,
    display_multi_experiment_summary,
    NOISE_PROBABILITIES,
)


def main():
    print("=" * 80)
    print("      Q-Crypt: Multi-Trial Statistical Experiment & CSV Logger")
    print("=" * 80)

    # 1. Number of qubits per trial
    n_input = input("1. Number of qubits per trial (e.g. 50, 100; default 100): ").strip()
    num_qubits = int(n_input) if n_input.isdigit() and int(n_input) > 0 else 100

    # 2. Number of repetitions (trials)
    rep_input = input("2. Number of repetitions/trials (e.g. 10, 20, 50; default 10): ").strip()
    num_repetitions = int(rep_input) if rep_input.isdigit() and int(rep_input) > 0 else 10

    # 3. Eve toggle
    eve_input = input("3. Enable Eve Intercept-Resend? (ON / OFF; default OFF): ").strip().upper()
    eve_enabled = eve_input in ["ON", "Y", "YES", "TRUE", "1"]

    # 4. Noise level
    print("4. Select Quantum Noise Level: OFF, LOW, MEDIUM, HIGH")
    noise_input = input("   Enter Noise Level (default OFF): ").strip().upper()
    noise_level = noise_input if noise_input in NOISE_PROBABILITIES else "OFF"

    # 5. Threshold
    thresh_input = input("5. Educational Acceptance Threshold (default 0.11 for 11%): ").strip()
    try:
        threshold = float(thresh_input) if thresh_input else 0.11
    except ValueError:
        threshold = 0.11

    # Execute Multi-Trial Simulation
    print(f"\n[Running {num_repetitions} trials of {num_qubits} qubits each. Please wait...]")
    summary = run_multi_experiment(
        num_qubits=num_qubits,
        num_repetitions=num_repetitions,
        eve_enabled=eve_enabled,
        noise_level=noise_level,
        qber_threshold=threshold,
        save_csv=True,
        output_dir="experiments",
    )

    # Display Report
    display_multi_experiment_summary(summary)


if __name__ == "__main__":
    main()
