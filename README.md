# Ubuntu Phone Compute Bridge

A bounded remote-compute protocol for a Windows controller and a phone-hosted Ubuntu environment: reviewed named jobs, structured results, and optional artifact integrity checks.

**The phone may fail. A victory quietly computed on Windows does not count.**

This public sample comes from my private remote-compute experiments. It exposes the controller and result contract for review. I can build and adapt the surrounding job workflows, device setup, and application integrations; this repo makes no claim that a phone is currently reachable.

## Transport: remote failure stays a failure

```mermaid
sequenceDiagram
    participant C as Caller
    participant W as Windows controller
    participant P as Phone Ubuntu

    C->>W: <b>Request named job</b>
    alt Invalid job or connection inputs
        W-->>C: <b>Reject before SSH</b>
    else Valid controller inputs
        W->>P: SSH, run mapped job
        alt SSH or remote execution fails
            P-->>W: Non-zero exit
            W-->>C: <b>Throw, no local fallback</b>
        else Remote stdout returns
            P-->>W: Structured stdout
            W-->>C: <b>Return stdout unchanged</b>
        end
    end
```

## Caller validation: check the result before using it

PowerShell returns stdout. The caller invokes Python validation separately, then verifies artifact bytes when it has an expected digest.

```mermaid
flowchart LR
    R["<b>Remote stdout</b>"] --> V{"parse_result valid?"}
    V -- No --> X["<b>Reject result</b>"]
    V -- Yes --> P["<b>Parsed result</b>"]
    classDef input fill:#e8e6df,stroke:#55534a,color:#20201d,stroke-width:2px;
    classDef pass fill:#d2e5d8,stroke:#38734d,color:#183923,stroke-width:2px;
    classDef stop fill:#f4dadd,stroke:#b14253,color:#611c29,stroke-width:2px;
    class R,V input;
    class P pass;
    class X stop;
```

`parse_result()` checks the byte limit, JSON object, expected job, phone execution location, and `ok == true`. Optional artifact verification returns a boolean:

```mermaid
flowchart LR
    A["<b>Bytes + expected SHA-256</b>"] --> H{"Digest matches?"}
    H -- No --> F["<b>false</b>"]
    H -- Yes --> T["<b>true</b>"]
    classDef input fill:#e8e6df,stroke:#55534a,color:#20201d,stroke-width:2px;
    classDef pass fill:#d2e5d8,stroke:#38734d,color:#183923,stroke-width:2px;
    classDef stop fill:#f4dadd,stroke:#b14253,color:#611c29,stroke-width:2px;
    class A,H input;
    class T pass;
    class F stop;
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
