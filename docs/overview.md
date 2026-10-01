# Design overview

The private lab uses an Android phone as a small attended compute target:

**Windows → SSH → Termux → Ubuntu userspace → bounded job → JSON result**

The interesting part is not SSH. SSH already knows how to execute arbitrary commands.

The interesting part is refusing to turn an automation bridge into “remote shell, but with extra branding.”

This public slice therefore has three contracts:

- the caller chooses from a tiny job registry;
- the result must explicitly prove which job ran and where;
- returned artifacts can be checked by digest before they are trusted.

The PowerShell entry point is intentionally boring: strict host-key checking, batch authentication, bounded connection settings, and hard failure when the remote side fails.
