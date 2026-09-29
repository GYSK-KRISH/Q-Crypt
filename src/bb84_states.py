"""
====================================================================
Experiment 2: The Four BB84 Quantum States & Basis Measurements
====================================================================
Educational Objective (Class 12 Physics / CS):
Understand how classical bits (0 and 1) are encoded into quantum states
using two complementary bases (Z basis and X basis), and understand how
matching vs. mismatched measurement bases affect the outcome.

--------------------------------------------------------------------
Core Concepts:
--------------------------------------------------------------------
1. Bit Value:
   The classical information we want to send: either 0 or 1.

2. Bases in BB84:
   - Z Basis (Rectilinear / Standard Computational Basis):
     * Bit 0 -> State |0> (Ground state)
     * Bit 1 -> State |1> (Excited state, prepared by X gate)
   - X Basis (Diagonal / Superposition Basis):
     * Bit 0 -> State |+> = (|0> + |1>) / sqrt(2) (prepared by H gate)
     * Bit 1 -> State |-> = (|0> - |1>) / sqrt(2) (prepared by X then H gate)

3. Measurement:
   - Quantum physical detectors naturally measure in the Z basis (|0> vs |1>).
   - To measure in the X basis (|+> vs |->), we apply a Hadamard (H) gate
     before measuring. This rotates the X-basis states back into Z-basis states:
         H|+> = |0>  (measured as 0)
         H|-> = |1>  (measured as 1)

4. Key Takeaway for BB84:
   - MATCHING basis (Prep == Meas): 100% deterministic, correct bit.
   - MISMATCHED basis (Prep != Meas): 50% / 50% random probabilistic outcome.
====================================================================
"""

import sys

# Ensure UTF-8 output encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def get_state_symbol(bit: int, basis: str) -> str:
    """Returns the Dirac ket notation symbol for the BB84 state."""
    if basis == "Z":
        return "|0>" if bit == 0 else "|1>"
    else:  # basis == "X"
        return "|+>" if bit == 0 else "|->"


def create_bb84_circuit(bit: int, prep_basis: str, meas_basis: str) -> QuantumCircuit:
    """
    Constructs a 1-qubit quantum circuit for state preparation and measurement.
    
    Args:
        bit (int): Classical bit value to encode (0 or 1).
        prep_basis (str): Basis used for preparation ('Z' or 'X').
        meas_basis (str): Basis used for measurement ('Z' or 'X').
        
    Returns:
        QuantumCircuit: The ready-to-run Qiskit quantum circuit.
    """
    # 1 quantum bit, 1 classical bit for measurement output
    qc = QuantumCircuit(1, 1)

    # -------------------------------------------------------------
    # Step 1: State Preparation (Encoding the bit into quantum state)
    # -------------------------------------------------------------
    # All qubits in Qiskit start in |0>.
    # If bit is 1, flip state from |0> to |1> using Pauli-X (NOT) gate.
    if bit == 1:
        qc.x(0)

    # If preparation basis is X (diagonal), apply Hadamard (H) gate.
    # - If initial state was |0>, H transforms it to |+>
    # - If initial state was |1>, H transforms it to |->
    if prep_basis == "X":
        qc.h(0)

    # Visual separator in the circuit between preparation and measurement
    qc.barrier()

    # -------------------------------------------------------------
    # Step 2: Basis Measurement
    # -------------------------------------------------------------
    # Physical detectors measure along the Z basis (|0> vs |1>).
    # To measure in the X basis (|+> vs |->), apply H gate before measurement.
    if meas_basis == "X":
        qc.h(0)

    # Measure qubit 0 into classical bit 0
    qc.measure(0, 0)

    return qc


def simulate_circuit(circuit: QuantumCircuit, shots: int = 1000) -> dict:
    """Runs the quantum circuit on Qiskit Aer simulator and returns counts."""
    simulator = AerSimulator()
    job = simulator.run(circuit, shots=shots)
    result = job.result()
    return result.get_counts()


def run_experiment_case(bit: int, prep_basis: str, meas_basis: str, shots: int = 1000):
    """Executes and formats a single BB84 state preparation and measurement scenario."""
    state_sym = get_state_symbol(bit, prep_basis)
    is_match = (prep_basis == meas_basis)
    match_status = "MATCH (Deterministic)" if is_match else "MISMATCH (Probabilistic)"

    print(f"\n--- Scenario: Bit={bit} | Prep Basis={prep_basis} ({state_sym}) | Meas Basis={meas_basis} ---")
    print(f"Basis Relationship: {match_status}")

    # Build and simulate circuit
    circuit = create_bb84_circuit(bit, prep_basis, meas_basis)
    counts = simulate_circuit(circuit, shots=shots)

    # Display circuit diagram
    print("Circuit:")
    try:
        print(circuit.draw(output="text"))
    except Exception:
        print(circuit)

    # Calculate statistics
    count_0 = counts.get("0", 0)
    count_1 = counts.get("1", 0)
    pct_0 = (count_0 / shots) * 100
    pct_1 = (count_1 / shots) * 100

    print(f"Results ({shots} shots):")
    print(f"  Outcome '0': {count_0:4d} times ({pct_0:5.1f}%)")
    print(f"  Outcome '1': {count_1:4d} times ({pct_1:5.1f}%)")

    if is_match:
        expected_bit = str(bit)
        actual_count = counts.get(expected_bit, 0)
        print(f"  [Verdict] 100% agreement! Measured bit '{expected_bit}' exactly as sent.")
    else:
        print("  [Verdict] 50/50 Random split! Measuring in wrong basis lost the original bit.")


def main():
    shots = 1000

    print("=" * 70)
    print("      Q-Crypt: Experiment 2 - The Four BB84 States & Bases")
    print("=" * 70)

    # -------------------------------------------------------------
    # PART 1: The Four BB84 States Measured in MATCHING Bases
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART 1: MATCHING BASES (Prep Basis == Meas Basis)")
    print(" Rule: If measurement basis matches, result is 100% deterministic.")
    print("=" * 70)

    # State 1: Bit 0, Z basis -> |0>
    run_experiment_case(bit=0, prep_basis="Z", meas_basis="Z", shots=shots)

    # State 2: Bit 1, Z basis -> |1>
    run_experiment_case(bit=1, prep_basis="Z", meas_basis="Z", shots=shots)

    # State 3: Bit 0, X basis -> |+>
    run_experiment_case(bit=0, prep_basis="X", meas_basis="X", shots=shots)

    # State 4: Bit 1, X basis -> |->
    run_experiment_case(bit=1, prep_basis="X", meas_basis="X", shots=shots)

    # -------------------------------------------------------------
    # PART 2: What Happens When Measurement Basis is MISMATCHED?
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print(" PART 2: MISMATCHED BASES (Prep Basis != Meas Basis)")
    print(" Rule: If measurement basis is different, result is 50/50 random.")
    print("=" * 70)

    # Case A: Prepared |0> (Z basis), measured in X basis
    run_experiment_case(bit=0, prep_basis="Z", meas_basis="X", shots=shots)

    # Case B: Prepared |1> (Z basis), measured in X basis
    run_experiment_case(bit=1, prep_basis="Z", meas_basis="X", shots=shots)

    # Case C: Prepared |+> (X basis), measured in Z basis
    run_experiment_case(bit=0, prep_basis="X", meas_basis="Z", shots=shots)

    # Case D: Prepared |-> (X basis), measured in Z basis
    run_experiment_case(bit=1, prep_basis="X", meas_basis="Z", shots=shots)

    print("\n" + "=" * 70)
    print(" Experiment Complete: All 4 BB84 states and basis combinations tested.")
    print("=" * 70)


if __name__ == "__main__":
    main()
