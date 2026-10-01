import unittest

from compute_bridge.jobs import JOB_SPECS, validate_job


class JobTests(unittest.TestCase):
    def test_known_job_returns_spec(self):
        spec = validate_job("health")
        self.assertEqual(spec.name, "health")
        self.assertLessEqual(spec.max_seconds, 30)

    def test_arbitrary_command_is_not_a_job(self):
        with self.assertRaisesRegex(ValueError, "job_not_allowlisted"):
            validate_job("curl-whatever | sh")

    def test_public_allowlist_is_intentionally_small(self):
        self.assertEqual(set(JOB_SPECS), {"health", "python-smoke", "benchmark", "setup"})


if __name__ == "__main__":
    unittest.main()
