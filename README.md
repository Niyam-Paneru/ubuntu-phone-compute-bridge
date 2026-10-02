# Ubuntu Phone Compute Bridge

A bounded remote-compute protocol intended for a Windows controller and a phone-hosted Ubuntu environment. The repository demonstrates the controller, named-job contract, structured-result validation, and integrity checks; it does **not** prove or expose a live phone deployment.

![Protocol boundary diagram](docs/workflow.svg)

## What is implemented

- [`windows/Invoke-SafeUbuntuJob.ps1`](windows/Invoke-SafeUbuntuJob.ps1) accepts only four named jobs, requires explicit connection inputs, uses strict host-key checking, and throws on SSH failure.
- [`src/compute_bridge/jobs.py`](src/compute_bridge/jobs.py) defines the matching public job registry.
- [`src/compute_bridge/results.py`](src/compute_bridge/results.py) validates payload size, job identity, execution location, and `ok: true`.
- [`src/compute_bridge/integrity.py`](src/compute_bridge/integrity.py) verifies optional SHA-256 artifact digests.

The PowerShell example returns remote stdout as-is. It does **not** automatically call the Python validator, so verified success requires the caller to pass that payload through `parse_result(...)`.

## Protocol example

Request:

```text
-Job health
```

Synthetic valid result:

```json
{"job":"health","execution_location":"phone-ubuntu","ok":true}
```

`parse_result(...)` accepts it only when the requested job is allowlisted, the payload is within 64 KiB, the job matches, the claimed execution location is exactly `phone-ubuntu`, and `ok` is exactly `true`.

## Failure behavior

| Failure | Result |
|---|---|
| unknown job | allowlist rejection |
| missing identity file | stop before SSH |
| host-key mismatch | SSH refuses the connection |
| non-zero SSH exit | controller throws; no local fallback |
| wrong job/location, false `ok`, oversized result | `parse_result` rejects |
| artifact digest mismatch | `verify_artifact` returns false |

Remote failure is never converted into a local Windows success path by this controller.

## Verify

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests -v
```

The tests cover the four-job allowlist, result identity/location checks, remote-failure rejection, the size bound, SHA-256 hashing, and tamper detection.

## Scope

No SSH key, password, device address, host fingerprint, router configuration, live endpoint, persistent worker service, or live phone-access claim is included.

See [job contract](docs/job-contract.md), [invariants](docs/invariants.md), [failure modes](docs/failure-modes.md), [security boundary](SECURITY.md), and [provenance](PROVENANCE.md).
