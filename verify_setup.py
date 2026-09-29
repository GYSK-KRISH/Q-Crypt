"""
====================================================================
Q-Crypt Environment Verification Script
====================================================================
This beginner-friendly script verifies that all required libraries
for the Q-Crypt BB84 project are installed and working properly.

Checked components:
1. Python Runtime
2. NumPy (numerical array handling)
3. Matplotlib (graphing and plotting)
4. Qiskit (quantum circuits and gates)
5. Qiskit Aer (quantum simulator backend)
====================================================================
"""

import sys

def test_python():
    """Check Python version (must be >= 3.8)."""
    version = sys.version.split()[0]
    print(f"[OK] Python is working! (Version: {version})")
    return True


def test_numpy():
    """Verify NumPy installation."""
    try:
        import numpy as np
        print(f"[OK] NumPy imported successfully! (Version: {np.__version__})")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import NumPy: {e}")
        return False


def test_matplotlib():
    """Verify Matplotlib installation."""
    try:
        import matplotlib
        print(f"[OK] Matplotlib imported successfully! (Version: {matplotlib.__version__})")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import Matplotlib: {e}")
        return False


def test_qiskit():
    """Verify Qiskit SDK installation."""
    try:
        import qiskit
        print(f"[OK] Qiskit imported successfully! (Version: {qiskit.__version__})")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import Qiskit: {e}")
        return False


def test_qiskit_aer():
    """Verify Qiskit Aer simulator installation and run a simple 1-qubit circuit."""
    try:
        import qiskit_aer
        from qiskit import QuantumCircuit
        from qiskit_aer import AerSimulator

        print(f"[OK] Qiskit Aer imported successfully! (Version: {qiskit_aer.__version__})")

        # Create a simple 1-qubit test circuit
        # Put qubit 0 into superposition using a Hadamard gate (H), then measure
        circuit = QuantumCircuit(1, 1)
        circuit.h(0)
        circuit.measure(0, 0)

        # Run on the modern AerSimulator (Qiskit 1.0+ standard API)
        simulator = AerSimulator()
        job = simulator.run(circuit, shots=50)
        counts = job.result().get_counts()

        print(f"     -> Quantum simulation sanity check passed! Measurement counts (50 shots): {counts}")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import Qiskit Aer: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Quantum circuit test error: {e}")
        return False


def main():
    print("=" * 60)
    print("   Q-Crypt: Environment Verification")
    print("=" * 60)

    checks = [
        ("Python", test_python),
        ("NumPy", test_numpy),
        ("Matplotlib", test_matplotlib),
        ("Qiskit", test_qiskit),
        ("Qiskit Aer", test_qiskit_aer),
    ]

    all_passed = True
    for name, check_func in checks:
        if not check_func():
            all_passed = False

    print("=" * 60)
    if all_passed:
        print("SUCCESS: All dependencies are ready for Q-Crypt!")
    else:
        print("ATTENTION: Some dependencies are missing. Run: pip install -r requirements.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()
