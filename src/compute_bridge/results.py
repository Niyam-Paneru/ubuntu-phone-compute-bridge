from __future__ import annotations

import json

from .jobs import validate_job


EXPECTED_LOCATION = "phone-ubuntu"


def parse_result(payload: str, *, expected_job: str) -> dict:
    validate_job(expected_job)
    data = json.loads(payload)

    if not isinstance(data, dict):
        raise ValueError("result_must_be_object")
    if data.get("job") != expected_job:
        raise ValueError("unexpected_job")
    if data.get("execution_location") != EXPECTED_LOCATION:
        raise ValueError("unexpected_execution_location")
    if data.get("ok") is not True:
        raise ValueError("remote_job_not_ok")

    return data
