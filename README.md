# Ubuntu Phone Compute Bridge

My laptop doesn't have unlimited patience (or memory). My phone has a processor and spends a suspicious amount of its day showing me videos. Could it do a little actual work?

This Windows-to-phone controller runs a bounded Ubuntu job over SSH and checks the result contract. If the laptop does the computation and puts the phone's name on the report, that isn't remote compute. That's group homework.

This is a controller and result contract, not a publicly running compute service.

## The phone gets the credit only if it did the work

The [PowerShell controller](windows/Invoke-SafeUbuntuJob.ps1) accepts reviewed job names and explicit SSH settings (host, user, port, key, and host-key checks). It requests a named remote job and returns stdout; the caller validates the result separately.

| Check | Why it matters |
| --- | --- |
| Job name is on the reviewed list | No surprise arbitrary commands |
| SSH and host-key verification succeed | We contacted the intended remote endpoint |
| Stdout is valid JSON and within the size limit | A 900-page stack trace does not count as a compute result |
| Response names the expected job | A response for some other task isn't evidence this job ran |
| Execution location says phone-ubuntu and success is true | Local work cannot masquerade as remote success |
| Provided artifact digest matches SHA-256 | The bytes are the bytes we expected |

**SSH failure stays failure.** There is no secret Windows fallback, and returned stdout is not automatically trusted as a success certificate.

Read the [job registry](src/compute_bridge/jobs.py), [result parser](src/compute_bridge/results.py), [integrity check](src/compute_bridge/integrity.py), [job contract](docs/job-contract.md), and [verification cases](docs/verification.md).

## What I didn't put in this repo

There are **no live worker credentials, keys, IP addresses, reachable phone, or proof of a currently online device** here. This is the controller, validation logic, and tests. The SSH transport alone doesn't authenticate a claimed job result beyond the configured checks; a real deployment still needs to protect its execution environment.

If the phone did nothing, it doesn't deserve a performance review. [Security boundary](SECURITY.md).
