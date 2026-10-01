import unittest

from compute_bridge.jobs import JOB_SPECS, job_spec, validate_job


class JobTests(unittest.TestCase):
    def test_known_job_keeps_simple_validation_contract(self):
        self.assertEqual(validate_job("health"), "health")

    def test_job_spec_carries_bounds(self):
        spec = job_spec("health")
        self.assertEqual(spec.name, "health")
        self.assertLessEqual(spec.max_seconds, 30)

    def test_arbitrary_command_is_not_a_job(self):
        with self.assertRaisesRegex(ValueError, "job_not_allowlisted"):
            validate_job("please-run-whatever-i-type")

    def test_public_allowlist_is_intentionally_small(self):
        self.assertEqual(set(JOB_SPECS), {"health", "python-smoke", "benchmark", "setup"})


if __name__ == "__main__":
    unittest.main()
