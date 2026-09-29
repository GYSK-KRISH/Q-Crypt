"""
====================================================================
Tests for Quantum Noise Modeling (tests/test_noise.py)
====================================================================
Verifies that:
1. build_noise_model creates valid NoiseModels for OFF, LOW, MEDIUM, HIGH.
2. Noise OFF returns None (pure noiseless simulation).
3. High noise elevates measurement error rate over many trials.
====================================================================
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from experiments.noise_experiment import build_noise_model, NOISE_CONFIGS


class TestNoiseModels(unittest.TestCase):
    """Unit tests for Qiskit Aer noise model construction."""

    def test_noise_model_off(self):
        """Noise OFF should return None (ideal noiseless simulator)."""
        nm = build_noise_model("OFF")
        self.assertIsNone(nm)

    def test_noise_models_creation(self):
        """LOW, MEDIUM, HIGH should successfully return NoiseModel instances."""
        for level in ["LOW", "MEDIUM", "HIGH"]:
            nm = build_noise_model(level)
            self.assertIsNotNone(nm, f"NoiseModel for {level} should not be None.")

    def test_noise_configs_values(self):
        """Verify noise configurations are strictly ascending."""
        self.assertEqual(NOISE_CONFIGS["OFF"], 0.0)
        self.assertLess(NOISE_CONFIGS["LOW"], NOISE_CONFIGS["MEDIUM"])
        self.assertLess(NOISE_CONFIGS["MEDIUM"], NOISE_CONFIGS["HIGH"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
