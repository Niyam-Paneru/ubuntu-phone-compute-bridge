# Ubuntu Phone Compute Bridge

A bounded remote-compute protocol intended for a Windows controller and a phone-hosted Ubuntu environment. It exposes a reviewed named-job contract, structured result validation, and optional artifact integrity checks; it does **not** prove or expose a live phone deployment.

The phone is allowed to fail. The controller is not allowed to improvise a Windows victory and call it remote compute.

```mermaid
sequenceDiagram
    participant C as Caller
    participant W as Windows controller
    participant S as SSH boundary
    participant P as phone-Ubuntu named job
    participant V as caller-side Python

    C->>W: Request named job
    alt job is not allowlisted
        W-->>C: Reject before SSH
    else allowlisted job
        W->>S: ssh.exe + explicit connection inputs
        S->>P: Run mapped named job
        alt SSH or remote execution fails
            S-->>W: Non-zero exit
            W-->>C: Throw; no local fallback
        else remote stdout returns
            P-->>S: Structured stdout
            S-->>W: stdout
            W-->>C: Return remote stdout unchanged
            C->>V: parse_result(stdout, expected_job)
            alt wrong job, wrong location, or ok != true
                V-->>C: Reject result
            else valid structured result
                V-->>C: Parsed result
                opt artifact digest supplied
                    C->>V: verify_artifact(bytes, expected_sha256)
                    alt digest mismatch
                        V-->>C: false
                    else digest matches
                        V-->>C: true
                    end
                end
            end
        end
    end
```

## Protocol at a glance

| Stage | Example / contract | Where it happens |
|---|---|---|
| Request | named job `health` | Windows controller accepts only the reviewed job set |
| Transport | explicit host, user, port, identity file + strict host-key checking | PowerShell crosses the SSH boundary |
| Remote result | `{"job":"health","execution_location":"phone-ubuntu","ok":true}` | named phone-Ubuntu job writes structured stdout |
| Handoff | remote stdout is returned unchanged | PowerShell does **not** automatically validate the JSON |
| Verification | `parse_result(..., expected_job="health")` | separate caller-side Python checks size, job, location, and `ok` |
| Artifact integrity | SHA-256 comparison when an expected digest exists | caller-side `verify_artifact(...)` |

## Failure behavior

| Failure | Result |
|---|---|
| unknown job | rejected before transport |
| missing identity file | controller stops before SSH |
| host-key mismatch | SSH refuses the connection |
| SSH / remote non-zero exit | controller throws; there is no local fallback |
| wrong job, wrong execution location, false `ok`, or oversized result | `parse_result(...)` rejects |
| artifact digest mismatch | `verify_artifact(...)` returns false |

## What to inspect

| File | Role |
|---|---|
| `windows/Invoke-SafeUbuntuJob.ps1` | allowlisted Windows controller and explicit SSH boundary |
| `src/compute_bridge/jobs.py` | public named-job registry |
| `src/compute_bridge/results.py` | caller-side structured stdout validation |
| `src/compute_bridge/integrity.py` | optional SHA-256 artifact verification |
| `tests/` | allowlist, result identity/location, failure, size-bound, and digest checks |

## Scope

No SSH key, password, device address, host fingerprint, router configuration, live endpoint, persistent worker service, or claim of a currently reachable phone is included.

Verification commands and expected checks: [docs/verification.md](docs/verification.md)

See [job contract](docs/job-contract.md), [invariants](docs/invariants.md), [failure modes](docs/failure-modes.md), [security boundary](SECURITY.md), and [provenance](PROVENANCE.md).
