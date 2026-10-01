import unittest

from compute_bridge.protocol import parse_result, sha256_bytes, validate_job, verify_artifact


class ComputeBridgeTests(unittest.TestCase):
    def test_allowlisted_job(self):
        self.assertEqual(validate_job("health"), "health")

    def test_unknown_job_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "job_not_allowlisted"):
            validate_job("please-run-whatever-i-type")

    def test_result_must_match_job(self):
        with self.assertRaisesRegex(ValueError, "unexpected_job"):
            parse_result(
                '{"job":"benchmark","execution_location":"phone-ubuntu","ok":true}',
                expected_job="health",
            )

    def test_result_must_prove_phone_execution(self):
        with self.assertRaisesRegex(ValueError, "unexpected_execution_location"):
            parse_result(
                '{"job":"health","execution_location":"windows","ok":true}',
                expected_job="health",
            )

    def test_failed_remote_result_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "remote_job_not_ok"):
            parse_result(
                '{"job":"health","execution_location":"phone-ubuntu","ok":false}',
                expected_job="health",
            )

    def test_valid_result(self):
        result = parse_result(
            '{"job":"health","execution_location":"phone-ubuntu","ok":true}',
            expected_job="health",
        )
        self.assertTrue(result["ok"])

    def test_sha256_is_deterministic(self):
        self.assertEqual(
            sha256_bytes(b"hello"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_artifact_verification(self):
        digest = sha256_bytes(b"artifact")
        self.assertTrue(verify_artifact(b"artifact", digest))
        self.assertFalse(verify_artifact(b"tampered", digest))


if __name__ == "__main__":
    unittest.main()
