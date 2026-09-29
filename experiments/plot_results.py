"""
====================================================================
Q-Crypt: Automated Experiment Data Visualization Engine
====================================================================
Educational Objective (Class 12 Science Project Visuals):
Generates 4 publication-quality, scientific graphs based on REAL
Qiskit quantum simulation data for project submission and reports:

1. Graph 1: QBER vs. Quantum Noise Level
2. Graph 2: QBER Distribution (Eve OFF vs. Eve ON)
3. Graph 3: Sifted Key Length vs. Number of Qubits Transmitted
4. Graph 4: Basis Matching Percentage Distribution

All figures are automatically saved in high resolution (300 DPI)
inside the 'screenshots/' directory.
====================================================================
"""

import os
import sys

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Use non-interactive backend for reliable headless image saving
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.experiment_runner import (
    ExperimentConfig,
    run_experiment,
    run_multi_experiment,
    NOISE_PROBABILITIES,
)

OUTPUT_DIR = "screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styling configuration for clean educational graphs
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
})


def plot_qber_vs_noise(num_qubits: int = 100, num_trials_per_level: int = 15):
    """
    Graph 1: QBER vs. Noise Level.
    Runs real simulations for OFF, LOW, MEDIUM, and HIGH noise levels and plots
    the observed average QBER with min-max error bars and acceptance threshold.
    """
    print("Generating Graph 1: QBER vs. Quantum Noise Level...")
    noise_levels = ["OFF", "LOW", "MEDIUM", "HIGH"]
    nominal_rates = [NOISE_PROBABILITIES[l] * 100 for l in noise_levels]

    avg_qbers = []
    min_qbers = []
    max_qbers = []

    for level in noise_levels:
        summary = run_multi_experiment(
            num_qubits=num_qubits,
            num_repetitions=num_trials_per_level,
            eve_enabled=False,
            noise_level=level,
            save_csv=False,
        )
        avg_qbers.append(summary.avg_qber * 100)
        min_qbers.append(summary.min_qber * 100)
        max_qbers.append(summary.max_qber * 100)

    # Calculate error bar ranges
    yerr_lower = [avg - mn for avg, mn in zip(avg_qbers, min_qbers)]
    yerr_upper = [mx - avg for avg, mx in zip(avg_qbers, max_qbers)]

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    bars = ax.bar(
        noise_levels,
        avg_qbers,
        yerr=[yerr_lower, yerr_upper],
        capsize=6,
        color=["#2ecc71", "#3498db", "#f39c12", "#e74c3c"],
        edgecolor="#2c3e50",
        linewidth=1.2,
        alpha=0.85,
        label="Observed Average QBER",
    )

    # Acceptance Threshold Line
    threshold_pct = 11.0
    ax.axhline(
        threshold_pct,
        color="#c0392b",
        linestyle="--",
        linewidth=2,
        label=f"Acceptance Threshold ({threshold_pct}%)",
    )

    # Annotations on top of bars
    for bar, avg in zip(bars, avg_qbers):
        height = bar.get_height()
        ax.annotate(
            f"{avg:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    ax.set_title("Graph 1: Measured QBER vs. Quantum Noise Level (Eve OFF)")
    ax.set_xlabel("Configured Noise Level (Channel Depolarizing Noise)")
    ax.set_ylabel("Quantum Bit Error Rate (QBER %)")
    ax.set_ylim(0, max(max_qbers + [threshold_pct]) + 8)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "1_qber_vs_noise.png")
    plt.savefig(filepath)
    plt.close()
    print(f" -> Saved: {filepath}")
    return filepath


def plot_eve_comparison(num_qubits: int = 100, num_trials: int = 25):
    """
    Graph 2: QBER with Eve OFF vs. Eve ON.
    Runs multiple real trials and visualizes the statistical QBER distribution
    under secure vs. intercepted quantum transmissions.
    """
    print("Generating Graph 2: QBER with Eve OFF vs. Eve ON...")

    # Run trials with Eve OFF
    summary_off = run_multi_experiment(
        num_qubits=num_qubits,
        num_repetitions=num_trials,
        eve_enabled=False,
        noise_level="OFF",
        save_csv=False,
    )
    qber_off = [t.qber * 100 for t in summary_off.trials]

    # Run trials with Eve ON
    summary_on = run_multi_experiment(
        num_qubits=num_qubits,
        num_repetitions=num_trials,
        eve_enabled=True,
        noise_level="OFF",
        save_csv=False,
    )
    qber_on = [t.qber * 100 for t in summary_on.trials]

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    # Boxplot / Scatter representation
    positions = [1, 2]
    bp = ax.boxplot(
        [qber_off, qber_on],
        positions=positions,
        patch_artist=True,
        widths=0.45,
        boxprops=dict(facecolor="#ecf0f1", color="#2c3e50", linewidth=1.5),
        medianprops=dict(color="#2980b9", linewidth=2),
        whiskerprops=dict(color="#2c3e50", linewidth=1.2),
        capprops=dict(color="#2c3e50", linewidth=1.2),
    )

    # Colorize boxes
    bp["boxes"][0].set_facecolor("#2ecc71")
    bp["boxes"][1].set_facecolor("#e74c3c")

    # Overlay jittered scatter data points
    np.random.seed(42)
    jitter_off = np.random.normal(1, 0.04, size=len(qber_off))
    jitter_on = np.random.normal(2, 0.04, size=len(qber_on))
    ax.scatter(jitter_off, qber_off, color="#27ae60", alpha=0.7, edgecolors="none", s=35, label="Eve OFF Trials")
    ax.scatter(jitter_on, qber_on, color="#c0392b", alpha=0.7, edgecolors="none", s=35, label="Eve ON Trials")

    # Threshold & Theoretical Line
    ax.axhline(11.0, color="#f39c12", linestyle="--", linewidth=1.8, label="Acceptance Threshold (11%)")
    ax.axhline(25.0, color="#8e44ad", linestyle=":", linewidth=2, label="Theoretical Average with Eve (25%)")

    ax.set_xticks(positions)
    ax.set_xticklabels([f"Eve OFF\n(Mean: {np.mean(qber_off):.1f}%)", f"Eve ON\n(Mean: {np.mean(qber_on):.1f}%)"])
    ax.set_title("Graph 2: QBER Comparison - Eve OFF vs. Eve ON (Intercept-Resend)")
    ax.set_ylabel("Quantum Bit Error Rate (QBER %)")
    ax.set_ylim(-2, max(qber_on + [30]) + 8)
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "2_qber_eve_off_vs_on.png")
    plt.savefig(filepath)
    plt.close()
    print(f" -> Saved: {filepath}")
    return filepath


def plot_sifted_key_vs_qubits():
    """
    Graph 3: Sifted Key Length vs. Number of Transmitted Qubits.
    Runs simulations across varying qubit counts and compares observed
    sifted key length with the theoretical 50% line.
    """
    print("Generating Graph 3: Sifted Key Length vs. Number of Qubits...")
    qubit_counts = [20, 40, 60, 80, 100, 150, 200]
    trials_per_count = 10

    avg_sifted_lengths = []
    avg_candidate_lengths = []

    for n in qubit_counts:
        summary = run_multi_experiment(
            num_qubits=n,
            num_repetitions=trials_per_count,
            eve_enabled=False,
            noise_level="OFF",
            save_csv=False,
        )
        avg_sifted_lengths.append(summary.avg_sifted_key_len)
        avg_candidate_lengths.append(summary.avg_candidate_key_len)

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    # Theoretical line (50% sifting rate)
    theoretical_sifted = [0.5 * n for n in qubit_counts]
    ax.plot(
        qubit_counts,
        theoretical_sifted,
        color="#7f8c8d",
        linestyle="--",
        linewidth=2,
        label="Theoretical Expectation ($y = 0.5x$, 50% Sifting)",
    )

    # Actual observed sifted key lengths
    ax.plot(
        qubit_counts,
        avg_sifted_lengths,
        marker="o",
        markersize=7,
        color="#2980b9",
        linewidth=2.5,
        label="Observed Sifted Key Length",
    )

    # Actual observed candidate key lengths (after 33% parameter test)
    ax.plot(
        qubit_counts,
        avg_candidate_lengths,
        marker="s",
        markersize=6,
        color="#27ae60",
        linewidth=2,
        linestyle="-.",
        label="Observed Candidate Secret Key (Post-Test)",
    )

    ax.set_title("Graph 3: Sifted Key Yield vs. Total Qubits Transmitted")
    ax.set_xlabel("Total Qubits Sent by Alice (Photons)")
    ax.set_ylabel("Generated Key Length (Bits)")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left")

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "3_sifted_key_vs_qubits.png")
    plt.savefig(filepath)
    plt.close()
    print(f" -> Saved: {filepath}")
    return filepath


def plot_basis_matching_distribution(num_trials: int = 100, num_qubits: int = 100):
    """
    Graph 4: Basis Matching Percentage Distribution.
    Simulates 100 independent transmissions and plots the distribution
    of basis matching ratios around the theoretical 50% mean.
    """
    print("Generating Graph 4: Basis Matching Percentage Distribution...")

    matching_percentages = []
    for _ in range(num_trials):
        config = ExperimentConfig(num_qubits=num_qubits, random_seed=None)
        res = run_experiment(config)
        pct = (len(res.matching_positions) / num_qubits) * 100
        matching_percentages.append(pct)

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)

    # Histogram
    counts, bins, patches = ax.hist(
        matching_percentages,
        bins=15,
        color="#3498db",
        edgecolor="#1b4f72",
        alpha=0.8,
        density=False,
        label="Observed Trials ($N=100$)",
    )

    # Mean line and Theoretical line
    mean_match = np.mean(matching_percentages)
    ax.axvline(
        50.0,
        color="#e74c3c",
        linestyle="--",
        linewidth=2.5,
        label="Theoretical Mean (50.0%)",
    )
    ax.axvline(
        mean_match,
        color="#27ae60",
        linestyle=":",
        linewidth=2,
        label=f"Observed Sample Mean ({mean_match:.2f}%)",
    )

    ax.set_title(f"Graph 4: Distribution of Basis Matching Rates ({num_trials} Trials of {num_qubits} Qubits)")
    ax.set_xlabel("Basis Matching Rate (%) [Alice Basis == Bob Basis]")
    ax.set_ylabel("Frequency (Number of Trials)")
    ax.grid(axis="y", linestyle=":", alpha=0.6)
    ax.legend(loc="upper right")

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "4_basis_matching_percentage.png")
    plt.savefig(filepath)
    plt.close()
    print(f" -> Saved: {filepath}")
    return filepath


def generate_all_graphs():
    """Runs all 4 simulation visualizers and prints a complete summary."""
    print("=" * 75)
    print("      Q-Crypt: Generating Scientific Experiment Visualizations")
    print("=" * 75)

    g1 = plot_qber_vs_noise()
    g2 = plot_eve_comparison()
    g3 = plot_sifted_key_vs_qubits()
    g4 = plot_basis_matching_distribution()

    print("\n" + "=" * 75)
    print(" All 4 graphs successfully generated and saved to 'screenshots/':")
    print(f"  1. {g1}")
    print(f"  2. {g2}")
    print(f"  3. {g3}")
    print(f"  4. {g4}")
    print("=" * 75)


if __name__ == "__main__":
    generate_all_graphs()
