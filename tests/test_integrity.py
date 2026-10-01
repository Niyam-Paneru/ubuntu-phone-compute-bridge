import unittest

from compute_bridge.integrity import sha256_bytes, verify_artifact


class IntegrityTests(unittest.TestCase):
    def test_known_sha(self):
        self.assertEqual(
            sha256_bytes(b"hello"),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )

    def test_tamper_is_visible(self):
        digest = sha256_bytes(b"artifact")
        self.assertTrue(verify_artifact(b"artifact", digest))
        self.assertFalse(verify_artifact(b"artifact!", digest))


if __name__ == "__main__":
    unittest.main()
