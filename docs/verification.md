# Verification

Exact maintainer-facing checks live here rather than in the reviewer-facing README.

## Local checks

```bash
python -m compileall -q src
PYTHONPATH=src python -m unittest discover -s tests -v
```

Expected evidence:

- source compilation exits successfully;
- the unittest suite passes the allowlist, structured-result identity/location, remote-failure, result-size, SHA-256, and tamper-detection checks.

## CI

CircleCI repeats source compilation and unittest discovery, then checks that the public proof/supporting files are present.

These checks validate the public protocol implementation. They do not establish that a live phone endpoint exists or is currently reachable.
