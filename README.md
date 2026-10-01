# Ubuntu Phone Compute Bridge

A public proof of a bounded Windows → Android/Termux → Ubuntu compute contract. The Windows controller selects one reviewed job, invokes it through a constrained SSH example, and returns structured remote output; the Python package separately validates job identity, execution location, success state, result size, and optional artifact digests.

![Protocol boundary diagram](docs/workflow.svg)

## What is actually implemented

- [`windows/Invoke-SafeUbuntuJob.ps1`](windows/Invoke-SafeUbuntuJob.ps1) is the concrete Windows controller example. It exposes only `health`, `python-smoke`, `benchmark`, and `setup`; requires an explicit IPv4 target, user, and identity file; enables strict host-key checking and bounded connection settings; and throws when SSH fails.
- [`src/compute_bridge/jobs.py`](src/compute_bridge/jobs.py) defines the same small public job registry plus descriptive `max_seconds` metadata.
- [`src/compute_bridge/results.py`](src/compute_bridge/results.py) rejects results that are too large, are not JSON objects, identify the wrong job or execution location, or do not report `ok: true`.
- [`src/compute_bridge/integrity.py`](src/compute_bridge/integrity.py) provides SHA-256 artifact verification when returned bytes have an expected digest.

One boundary is intentionally visible rather than hidden: the PowerShell example emits the remote stdout as-is. It does **not** call the Python validator itself. A caller that wants verified success must pass that payload through `parse_result(...)` before trusting it.

## Protocol contract

A request is a reviewed job selection, not an arbitrary shell string. For example:

```text
-Job health
```

A synthetic valid remote result is:

```json
{"job":"health","execution_location":"phone-ubuntu","ok":true}
```

The Python verifier accepts that result only when the expected job is allowlisted, the UTF-8 payload is within the 64 KiB bound, `job` matches the request, `execution_location` is exactly `phone-ubuntu`, and `ok` is exactly `true`.

Artifact verification is a separate check: `verify_artifact(bytes, expected_sha256)` compares the returned bytes with the expected SHA-256 digest. The PowerShell example does not currently return an artifact or wire this digest check automatically.

## Failure behavior

| Failure | Result |
|---|---|
| unknown job name | rejected by the allowlist |
| missing identity file | controller throws before SSH |
| host identity mismatch | strict host-key checking stops the SSH connection |
| non-zero SSH exit | controller throws; no local fallback |
| wrong job or execution location | `parse_result` rejects |
| `ok` is false | `parse_result` rejects |
| result exceeds the configured byte bound | rejected before JSON parsing |
| artifact digest mismatch | `verify_artifact` returns false |

Remote failure is not converted into a plausible local Windows success path anywhere in this public controller.

## Verify the public slice

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests -v
```

The behavior suite covers the four-job allowlist, result identity/location checks, explicit remote failure rejection, the result-size limit, deterministic SHA-256 hashing, and tamper detection.

## Scope and provenance

This repository contains no SSH private key, password, device address, host fingerprint, router configuration, or live remote-access endpoint. The private lab contains the actual device setup and recovery details. This public slice demonstrates the controller/protocol boundaries; it does not publish a persistent worker service or claim that the example exposes live phone access.

For the narrower contracts, see [invariants](docs/invariants.md), [failure modes](docs/failure-modes.md), [job contract](docs/job-contract.md), [walkthrough](docs/walkthrough.md), [security boundary](SECURITY.md), and [provenance](PROVENANCE.md).
