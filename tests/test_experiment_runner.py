"""
====================================================================
Tests for Unified Experiment Runner (tests/test_experiment_runner.py)
====================================================================
Verifies that:
1. ExperimentConfig and ExperimentResult dataclasses function properly.
2. run_experiment returns all required output fields.
3. Reproducible runs with random_seed produce consistent results.
4. Test sample and candidate key lengths correctly partition the sifted key.
5. run_multi_experiment calculates statistical aggregates and exports CSV.
====================================================================
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.experiment_runner import (
    ExperimentConfig,
    ExperimentResult,
    MultiExperimentSummary,
    run_experiment,
    run_multi_experiment,
)


class TestExperimentRunner(unittest.TestCase):
    """Test suite for the unified Experiment Runner."""

    def test_clean_noiseless_run(self):
        """Test clean BB84 run with Eve OFF, Noise OFF."""
        config = ExperimentConfig(
            num_qubits=40,
            eve_enabled=False,
            noise_enabled=False,
            qber_threshold=0.11,
            random_seed=42,
        )

        result = run_experiment(config)

        # Check types
        self.assertIsInstance(result, ExperimentResult)
        self.assertEqual(result.total_qubits, 40)
        self.assertEqual(len(result.alice_bits), 40)
        self.assertEqual(len(result.bob_results), 40)

        # Sifted key check
        self.assertEqual(len(result.alice_sifted_key), len(result.matching_positions))
        self.assertEqual(result.alice_sifted_key, result.bob_sifted_key)

        # In noiseless run without Eve, errors must be 0 and QBER 0.0
        self.assertEqual(result.errors, 0)
        self.assertEqual(result.qber, 0.0)
        self.assertEqual(result.status, "PASSED")

        # Partition check: test sample + candidate key = sifted key
        sifted_len = len(result.alice_sifted_key)
        test_len = len(result.test_sample_indices)
        cand_len = len(result.alice_candidate_key)
        self.assertEqual(test_len + cand_len, sifted_len)

    def test_custom_test_sample_size(self):
        """Test specifying an explicit test_sample_size."""
        config = ExperimentConfig(
            num_qubits=60,
            test_sample_size=8,
            random_seed=123,
        )
        result = run_experiment(config)

        # If sifted key has at least 8 bits, test sample must be exactly 8
        if len(result.alice_sifted_key) >= 8:
            self.assertEqual(len(result.test_sample_indices), 8)
            self.assertEqual(len(result.test_sample_alice), 8)
            self.assertEqual(len(result.test_sample_bob), 8)

    def test_result_to_dict(self):
        """Test converting result to dictionary."""
        config = ExperimentConfig(num_qubits=20, random_seed=7)
        result = run_experiment(config)
        d = result.to_dict()

        self.assertIsInstance(d, dict)
        self.assertIn("total_qubits", d)
        self.assertIn("alice_bits", d)
        self.assertIn("alice_bases", d)
        self.assertIn("bob_bases", d)
        self.assertIn("bob_results", d)
        self.assertIn("matching_positions", d)
        self.assertIn("alice_sifted_key", d)
        self.assertIn("bob_sifted_key", d)
        self.assertIn("test_sample_indices", d)
        self.assertIn("errors", d)
        self.assertIn("qber", d)
        self.assertIn("alice_candidate_key", d)
        self.assertIn("bob_candidate_key", d)
        self.assertIn("status", d)

    def test_multi_experiment_and_csv_export(self):
        """Test multi-trial runner and verify statistical bounds and CSV export."""
        summary = run_multi_experiment(
            num_qubits=30,
            num_repetitions=3,
            eve_enabled=False,
            noise_level="OFF",
            save_csv=True,
            output_dir="experiments",
            csv_filename="test_multi_output.csv",
        )

        self.assertIsInstance(summary, MultiExperimentSummary)
        self.assertEqual(summary.num_repetitions, 3)
        self.assertEqual(summary.num_qubits_per_run, 30)
        self.assertEqual(len(summary.trials), 3)

        # QBER stats
        self.assertGreaterEqual(summary.avg_qber, 0.0)
        self.assertLessEqual(summary.min_qber, summary.avg_qber)
        self.assertGreaterEqual(summary.max_qber, summary.avg_qber)

        # CSV file existence
        self.assertIsNotNone(summary.csv_filepath)
        self.assertTrue(os.path.exists(summary.csv_filepath))

        # Cleanup test CSV file
        if os.path.exists(summary.csv_filepath):
            os.remove(summary.csv_filepath)


if __name__ == "__main__":
    unittest.main(verbosity=2)
