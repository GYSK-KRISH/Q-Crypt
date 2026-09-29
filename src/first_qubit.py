"""
====================================================================
Experiment 1: My First Qubit & Superposition
====================================================================
Educational Objective (Class 12 Physics / CS):
Understand how a single quantum bit (qubit) behaves when placed
into quantum superposition using a Hadamard gate, and observe the
probabilistic nature of quantum measurement.

Key Terms Explained:
- Qubit: A Quantum Bit. Unlike a classical bit (which can only be
  0 or 1), a qubit can exist in a linear combination (superposition)
  of both states simultaneously.
- |0> State: The default ground state of a qubit. In Dirac bra-ket
  notation, |0> represents the classical bit 0.
- Hadamard Gate (H): A quantum logic gate that transforms a definite
  basis state (|0> or |1>) into an equal superposition state:
      H|0> = (|0> + |1>) / sqrt(2)
- Measurement: In quantum mechanics, observing/measuring a qubit
  causes its superposition state to "collapse" into a definite
  classical state (0 or 1) with specific probabilities.
- Shots: The number of times the quantum circuit is repeatedly
  executed and measured to collect statistical data.
====================================================================
"""

import sys

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Import the core quantum circuit builder from Qiskit
from qiskit import QuantumCircuit

# Import the AerSimulator backend from Qiskit Aer (Modern Qiskit API)
from qiskit_aer import AerSimulator


def run_first_qubit_experiment(shots: int = 1000):
    """
    Builds, simulates, and measures a 1-qubit superposition circuit.
    
    Args:
        shots (int): Total number of simulation runs (default: 1000).
    """
    print("=" * 60)
    print("   Q-Crypt: Experiment 1 - First Qubit Superposition")
    print("=" * 60)

    # Step 1: Create a quantum circuit with 1 quantum bit and 1 classical bit.
    # The classical bit is needed to store the measurement result.
    # By default in Qiskit, all qubits start in the |0> state.
    circuit = QuantumCircuit(1, 1)
    print("\n[Step 1] Created 1 qubit initialized in state |0>.")

    # Step 2: Apply a Hadamard gate (H) to qubit 0.
    # This places the qubit into an equal superposition: (|0> + |1>) / sqrt(2).
    circuit.h(0)
    print("[Step 2] Applied Hadamard Gate (H) -> Qubit is now in Superposition.")

    # Step 3: Measure qubit 0 and store the outcome into classical bit 0.
    # Measurement forces the quantum state to collapse into either 0 or 1.
    circuit.measure(0, 0)
    print("[Step 3] Added measurement -> Collapses state to classical bit.")

    # Display the visual representation of our quantum circuit
    print("\nQuantum Circuit Diagram:")
    try:
        print(circuit.draw(output="text"))
    except Exception:
        print(circuit)

    # Step 4: Set up the Qiskit Aer quantum simulator.
    simulator = AerSimulator()
    print(f"\n[Step 4] Running circuit on AerSimulator for {shots} shots...")

    # Step 5: Execute the circuit and retrieve the measurement counts.
    job = simulator.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Step 6: Display the measurement counts and percentages.
    print("\n" + "=" * 60)
    print("   Simulation Results")
    print("=" * 60)

    count_0 = counts.get("0", 0)
    count_1 = counts.get("1", 0)
    pct_0 = (count_0 / shots) * 100
    pct_1 = (count_1 / shots) * 100

    print(f"State '0' measured: {count_0:4d} times ({pct_0:5.1f}%)")
    print(f"State '1' measured: {count_1:4d} times ({pct_1:5.1f}%)")
    print("=" * 60)


if __name__ == "__main__":
    # Run the experiment with 1000 shots
    run_first_qubit_experiment(shots=1000)
