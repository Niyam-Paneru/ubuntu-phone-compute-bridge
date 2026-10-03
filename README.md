# Ubuntu Phone Compute Bridge

A bounded remote-compute protocol for a Windows controller and a phone-hosted Ubuntu environment: reviewed named jobs, structured results, and optional artifact integrity checks.

**The phone may fail. A victory quietly computed on Windows does not count.**

This public sample comes from my private remote-compute experiments. It exposes the controller and result contract for review. I can build and adapt the surrounding job workflows, device setup, and application integrations; this repo makes no claim that a phone is currently reachable.

## Transport: remote failure stays a failure

```mermaid
---
config:
  sequence:
    actorMargin: 50
    messageMargin: 28
    mirrorActors: false
    wrap: false
---
sequenceDiagram
    accTitle: Transport: remote failure stays a failure
    accDescr: Sequence for transport: remote failure stays a failure.
    participant C as Caller
    participant W as Windows controller
    participant P as Phone Ubuntu

    C->>W: Request named job
    alt Invalid job or connection inputs
        W-->>C: Reject before SSH
    else Valid controller inputs
        W->>P: SSH, run mapped job
        alt SSH or remote execution fails
            P-->>W: Non-zero exit
            W-->>C: Throw, no local fallback
        else Remote stdout returns
            P-->>W: Structured stdout
            W-->>C: Return stdout unchanged
        end
    end
```

## Caller validation: check the result before using it

PowerShell returns stdout. The caller invokes Python validation separately, then verifies artifact bytes when it has an expected digest.

```mermaid
---
config:
  flowchart:
    curve: linear
    nodeSpacing: 28
    rankSpacing: 42
---
flowchart LR
    accTitle: Caller validation: check the result before using it
    accDescr: Decision flow for caller validation: check the result before using it.
    R["Remote stdout"] --> V{"parse_result valid?"}
    V -- No --> X["Reject result"]
    V -- Yes --> P["Parsed result"]
    classDef input stroke-width:1.5px;
    classDef pass stroke-width:2.5px;
    classDef stop stroke-width:2px,stroke-dasharray:5 3;
    class R,V input;
    class P pass;
    class X stop;
```

`parse_result()` checks the byte limit, JSON object, expected job, phone execution location, and `ok == true`. Optional artifact verification returns a boolean:

```mermaid
---
config:
  flowchart:
    curve: linear
    nodeSpacing: 28
    rankSpacing: 42
---
flowchart LR
    accTitle: Caller validation: check the result before using it
    accDescr: Decision flow for caller validation: check the result before using it.
    A["Bytes + expected SHA-256"] --> H{"Digest matches?"}
    H -- No --> F["false"]
    H -- Yes --> T["true"]
    classDef input stroke-width:1.5px;
    classDef pass stroke-width:2.5px;
    classDef stop stroke-width:2px,stroke-dasharray:5 3;
    class A,H input;
    class T pass;
    class F stop;
```

The controller accepts only reviewed named jobs, such as `health`, and uses an explicit SSH host, user, port, identity file, and strict host-key checking. A result can be `{"job":"health","execution_location":"phone-ubuntu","ok":true}`; returning that stdout does not automatically validate it.

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
