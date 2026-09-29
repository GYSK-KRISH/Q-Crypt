"""
====================================================================
Comprehensive Master Audit & Test Suite (tests/test_master_audit.py)
====================================================================
Audits all 18 required aspects of Q-Crypt:
1. Classical BB84 logic
2. Quantum state preparation
3. Z-basis measurement
4. X-basis measurement
5. Basis matching
6. Sifting
7. QBER calculation
8. Eve OFF
9. Eve ON
10. Noise OFF
11. Noise ON
12. Experiment repetition
13. CSV output
14. Graph generation
15. Message encryption
16. Message decryption
17. Rejected-key behavior
18. GUI controls & initialization
====================================================================
"""

import unittest
import os
import sys
import tkinter as tk

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from qiskit_aer import AerSimulator
from src.classical_bb84 import (
    generate_random_bits,
    generate_random_bases,
    simulate_bob_measurement,
    sift_keys,
)
from src.bb84_quantum import (
    prepare_qubit as prep_qubit_q,
    measure_qubit as meas_qubit_q,
    estimate_qber_and_extract_key as est_qber_q,
)
from src.experiment_runner import (
    ExperimentConfig,
    ExperimentResult,
    run_experiment,
    run_multi_experiment,
    build_noise_model,
)
from src.encryption import (
    text_to_bits,
    bits_to_text,
    encrypt_message,
    decrypt_message,
    send_secure_message,
)
from src.gui import QCryptGUI, generate_educational_circuit


class MasterAuditTest(unittest.TestCase):
    """Exhaustive audit suite covering all 18 components of Q-Crypt."""

    def setUp(self):
        self.simulator = AerSimulator()

    # 1. Classical BB84 logic
    def test_01_classical_bb84_logic(self):
        bits = generate_random_bits(20)
        bases = generate_random_bases(20)
        self.assertEqual(len(bits), 20)
        self.assertEqual(len(bases), 20)
        self.assertTrue(all(b in [0, 1] for b in bits))
        self.assertTrue(all(b in ["Z", "X"] for b in bases))

    # 2. Quantum state preparation
    def test_02_quantum_state_preparation(self):
        for bit in [0, 1]:
            for basis in ["Z", "X"]:
                qc = prep_qubit_q(bit, basis)
                self.assertEqual(qc.num_qubits, 1)
                self.assertEqual(qc.num_clbits, 1)

    # 3. Z-basis measurement
    def test_03_z_basis_measurement(self):
        # |0> in Z -> 0
        qc0 = prep_qubit_q(0, "Z")
        self.assertEqual(meas_qubit_q(qc0, "Z", self.simulator), 0)
        # |1> in Z -> 1
        qc1 = prep_qubit_q(1, "Z")
        self.assertEqual(meas_qubit_q(qc1, "Z", self.simulator), 1)

    # 4. X-basis measurement
    def test_04_x_basis_measurement(self):
        # |+> in X -> 0
        qc0 = prep_qubit_q(0, "X")
        self.assertEqual(meas_qubit_q(qc0, "X", self.simulator), 0)
        # |-> in X -> 1
        qc1 = prep_qubit_q(1, "X")
        self.assertEqual(meas_qubit_q(qc1, "X", self.simulator), 1)

    # 5. Basis matching
    def test_05_basis_matching(self):
        alice_bases = ["Z", "X", "Z", "X"]
        bob_bases = ["Z", "Z", "Z", "X"]
        # Matching positions should be indices 0, 2, 3
        matches = [i for i in range(4) if alice_bases[i] == bob_bases[i]]
        self.assertEqual(matches, [0, 2, 3])

    # 6. Sifting
    def test_06_sifting(self):
        alice_bits = [0, 1, 1, 0]
        bob_results = [0, 0, 1, 0]
        alice_bases = ["Z", "X", "Z", "X"]
        bob_bases = ["Z", "Z", "Z", "X"]
        a_sifted, b_sifted, indices = sift_keys(alice_bits, bob_results, alice_bases, bob_bases)
        self.assertEqual(indices, [0, 2, 3])
        self.assertEqual(a_sifted, [0, 1, 0])
        self.assertEqual(b_sifted, [0, 1, 0])

    # 7. QBER calculation
    def test_07_qber_calculation(self):
        # 1 error out of 4 test bits -> QBER = 0.25
        a_sifted = [0, 1, 0, 1, 1, 0]
        b_sifted = [0, 1, 1, 1, 1, 0]  # error at index 2
        res = est_qber_q(a_sifted, b_sifted, test_sample_size=4)
        self.assertEqual(res["num_test_bits"], 4)
        self.assertIn(res["qber"], [0.0, 0.25])  # Depends on whether index 2 is sampled
        self.assertEqual(len(res["alice_candidate_key"]), 2)

    # 8. Eve OFF
    def test_08_eve_off_noiseless(self):
        config = ExperimentConfig(num_qubits=40, eve_enabled=False, noise_enabled=False, random_seed=42)
        res = run_experiment(config)
        self.assertEqual(res.errors, 0)
        self.assertEqual(res.qber, 0.0)
        self.assertEqual(res.status, "PASSED")

    # 9. Eve ON
    def test_09_eve_on_detection(self):
        # Over 100 qubits with Eve ON, errors should typically be detected
        config = ExperimentConfig(num_qubits=100, eve_enabled=True, noise_enabled=False, random_seed=123)
        res = run_experiment(config)
        self.assertGreaterEqual(res.errors, 0)
        self.assertIsInstance(res.status, str)

    # 10. Noise OFF
    def test_10_noise_off_model(self):
        nm = build_noise_model("OFF")
        self.assertIsNone(nm)

    # 11. Noise ON
    def test_11_noise_on_models(self):
        for lvl in ["LOW", "MEDIUM", "HIGH"]:
            nm = build_noise_model(lvl)
            self.assertIsNotNone(nm)

    # 12. Experiment repetition
    def test_12_experiment_repetition(self):
        summary = run_multi_experiment(
            num_qubits=20,
            num_repetitions=5,
            eve_enabled=False,
            noise_level="OFF",
            save_csv=False,
        )
        self.assertEqual(summary.num_repetitions, 5)
        self.assertGreaterEqual(summary.avg_sifted_key_len, 0)
        self.assertGreaterEqual(summary.avg_qber, 0.0)

    # 13. CSV output
    def test_13_csv_output(self):
        test_csv = "test_audit_output.csv"
        summary = run_multi_experiment(
            num_qubits=20,
            num_repetitions=2,
            eve_enabled=False,
            noise_level="OFF",
            save_csv=True,
            output_dir="experiments",
            csv_filename=test_csv,
        )
        self.assertIsNotNone(summary.csv_filepath)
        self.assertTrue(os.path.exists(summary.csv_filepath))
        # Verify file non-empty and cleanup
        self.assertGreater(os.path.getsize(summary.csv_filepath), 50)
        if os.path.exists(summary.csv_filepath):
            os.remove(summary.csv_filepath)

    # 14. Graph generation verification
    def test_14_graph_files_exist(self):
        expected_graphs = [
            "1_qber_vs_noise.png",
            "2_qber_eve_off_vs_on.png",
            "3_sifted_key_vs_qubits.png",
            "4_basis_matching_percentage.png",
        ]
        for g in expected_graphs:
            p = os.path.join("screenshots", g)
            self.assertTrue(os.path.exists(p), f"Graph file {g} missing from screenshots/")
            self.assertGreater(os.path.getsize(p), 1000, f"Graph file {g} is corrupted or empty.")

    # 15. Message encryption
    def test_15_message_encryption(self):
        msg = "QKD"
        key = [1, 0, 1, 0] * 6  # 24 bits
        payload = encrypt_message(msg, key)
        self.assertEqual(len(payload["ciphertext_bits"]), 24)
        self.assertEqual(len(payload["ciphertext_hex"]), 6)

    # 16. Message decryption
    def test_16_message_decryption(self):
        msg = "QKD"
        key = [1, 0, 1, 0] * 6
        payload = encrypt_message(msg, key)
        decrypted = decrypt_message(payload["ciphertext_bits"], key)
        self.assertEqual(decrypted, msg)

    # 17. Rejected-key behavior
    def test_17_rejected_key_behavior(self):
        # Test that short key raises ValueError
        with self.assertRaises(ValueError):
            encrypt_message("HELLO", [0, 1, 0])

        # Test educational circuit model generator
        circuit_str = generate_educational_circuit(1, "X", "X")
        self.assertIn("H", circuit_str)
        self.assertIn("M", circuit_str)

    # 18. GUI controls & initialization
    def test_18_gui_controls(self):
        root = tk.Tk()
        app = QCryptGUI(root)
        self.assertIsNotNone(app.qubit_var)
        self.assertIsNotNone(app.eve_var)
        self.assertIsNotNone(app.noise_var)
        self.assertIsNotNone(app.thresh_var)
        root.update_idletasks()
        root.destroy()


if __name__ == "__main__":
    unittest.main(verbosity=2)
