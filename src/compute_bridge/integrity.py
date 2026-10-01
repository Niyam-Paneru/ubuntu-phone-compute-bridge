from __future__ import annotations

import hashlib


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_artifact(data: bytes, expected_sha256: str) -> bool:
    return sha256_bytes(data) == expected_sha256.lower()
