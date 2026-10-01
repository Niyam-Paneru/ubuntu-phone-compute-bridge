# Security boundary

This public repo ships no SSH private key, password, device address, host fingerprint, router configuration, or live remote-access secret.

Keep host identity verification strict. Keep the job registry small. Do not replace named jobs with arbitrary command passthrough.

If the remote worker cannot prove the expected job and execution location, treat the result as untrusted.
