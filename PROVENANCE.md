# Provenance

The code comes from private experiments using a phone-hosted Ubuntu environment as a bounded compute target.

The public repository keeps the pieces that are safe and independently reviewable: four named jobs, a Windows PowerShell controller example, structured result validation, execution-location checks, SHA-256 artifact verification, and explicit remote-failure handling.

Machine-specific material is excluded: SSH keys, addresses, host fingerprints, router configuration, device setup, recovery steps, and any live remote-access path.

This repository demonstrates the controller/protocol contract. It does not demonstrate that a phone is currently reachable or running a persistent worker service.
