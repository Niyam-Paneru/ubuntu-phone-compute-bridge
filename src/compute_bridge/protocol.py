from __future__ import annotations

import hashlib
import json

ALLOWED_JOBS = frozenset({"health", "python-smoke", "benchmark", "setup"})


def validate_job(job: str) -> str:
    if job not in ALLOWED_JOBS:
        raise ValueError("job_not_allowlisted")
    return job


def parse_result(payload: str, *, expected_job: str) -> dict:
    validate_job(expected_job)
    data = json.loads(payload)
    if not isinstance(data, dict):
        raise ValueError("result_must_be_object")
    if data.get("job") != expected_job:
        raise ValueError("unexpected_job")
    if data.get("execution_location") != "phone-ubuntu":
        raise ValueError("unexpected_execution_location")
    if data.get("ok") is not True:
        raise ValueError("remote_job_not_ok")
    return data


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_artifact(data: bytes, expected_sha256: str) -> bool:
    return sha256_bytes(data) == expected_sha256.lower()
