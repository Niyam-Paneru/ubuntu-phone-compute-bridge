# Ubuntu Phone Compute Bridge

My Windows laptop and heavy computation have a complicated relationship. So I experimented with using a phone-hosted Ubuntu environment as a remote worker.

The rule was simple: **the laptop is not allowed to do the work locally and then put “phone” on the receipt.** That would make a very impressive benchmark of the wrong device.

This repo contains a bounded Windows-to-phone **controller and result contract**, not a publicly running compute service.

## The trip to the phone

The [PowerShell controller](windows/Invoke-SafeUbuntuJob.ps1) accepts reviewed job names and explicit SSH settings (host, user, port, key, and host-key checks). It requests a named remote job and returns stdout; the caller validates the result separately.

| Check | Why it matters |
| --- | --- |
| Job name is on the reviewed list | No surprise arbitrary commands |
| SSH and host-key verification succeed | We contacted the intended remote endpoint |
| Stdout is valid JSON and within the size limit | A gigantic stack trace isn't a result |
| Response names the expected job | Nobody swaps the homework halfway through |
| Execution location says phone-ubuntu and success is true | The laptop doesn't steal the phone's medal |
| Provided artifact digest matches SHA-256 | The bytes are the bytes we expected |

**SSH failure stays failure.** There is no secret Windows fallback, and returned stdout is not automatically trusted as a success certificate.

Read the [job registry](src/compute_bridge/jobs.py), [result parser](src/compute_bridge/results.py), [integrity check](src/compute_bridge/integrity.py), [job contract](docs/job-contract.md), and [verification cases](docs/verification.md).

## The phone is not in the box

There are **no live worker credentials, keys, IP addresses, reachable phone, or proof of a currently online device** here. This is the controller, validation logic, and tests. The SSH transport alone doesn't authenticate a claimed job result beyond the configured checks; a real deployment still needs to protect its execution environment.

I wanted extra compute, not an elaborate way for my laptop to lie on its résumé. [Security boundary](SECURITY.md).
