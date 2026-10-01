from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JobSpec:
    name: str
    description: str
    max_seconds: int


JOB_SPECS = {
    "health": JobSpec("health", "basic remote health proof", 10),
    "python-smoke": JobSpec("python-smoke", "prove Python executes on the phone Ubuntu environment", 20),
    "benchmark": JobSpec("benchmark", "small bounded CPU benchmark", 30),
    "setup": JobSpec("setup", "check required local tooling", 20),
}

ALLOWED_JOBS = frozenset(JOB_SPECS)


def validate_job(job: str) -> JobSpec:
    try:
        return JOB_SPECS[job]
    except KeyError as error:
        raise ValueError("job_not_allowlisted") from error
