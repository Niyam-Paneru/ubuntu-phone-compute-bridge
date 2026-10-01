import unittest

from compute_bridge.results import parse_result


class ResultTests(unittest.TestCase):
    def test_result_must_prove_remote_location(self):
        with self.assertRaisesRegex(ValueError, "unexpected_execution_location"):
            parse_result(
                '{"job":"health","execution_location":"windows","ok":true}',
                expected_job="health",
            )

    def test_wrong_job_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unexpected_job"):
            parse_result(
                '{"job":"benchmark","execution_location":"phone-ubuntu","ok":true}',
                expected_job="health",
            )

    def test_failed_remote_result_is_not_success(self):
        with self.assertRaisesRegex(ValueError, "remote_job_not_ok"):
            parse_result(
                '{"job":"health","execution_location":"phone-ubuntu","ok":false}',
                expected_job="health",
            )

    def test_valid_result_round_trips(self):
        result = parse_result(
            '{"job":"health","execution_location":"phone-ubuntu","ok":true}',
            expected_job="health",
        )
        self.assertTrue(result["ok"])

    def test_oversized_result_is_rejected_before_parsing(self):
        payload = '{"job":"health","execution_location":"phone-ubuntu","ok":true,"pad":"' + ("x" * 200) + '"}'
        with self.assertRaisesRegex(ValueError, "result_too_large"):
            parse_result(payload, expected_job="health", max_bytes=64)

    def test_invalid_result_size_limit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "invalid_result_size_limit"):
            parse_result("{}", expected_job="health", max_bytes=0)


if __name__ == "__main__":
    unittest.main()
