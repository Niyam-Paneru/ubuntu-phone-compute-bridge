# Walkthrough: prove the phone did the work

The controller requests the named job `health`.

A valid worker result says, in effect:

- job: health
- execution location: phone-ubuntu
- success: true

That proves the result matches the requested job contract.

Now imagine the connection fails and a local helper quietly runs an equivalent check on Windows.

The output may look useful. It is still invalid for the question “did the phone worker run?”

Likewise, a response labeled `benchmark` cannot satisfy a `health` request, even if both succeeded.

The bridge treats execution identity as part of correctness because otherwise remote verification becomes theatre.
