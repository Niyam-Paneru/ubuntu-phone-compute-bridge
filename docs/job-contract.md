# Job contract

A remote job is accepted only when the controller and worker agree on the same small contract.

## Request

- reviewed job name;
- no arbitrary command text;
- caller knows the expected worker location.

## Result

- `job` matches the requested name;
- `execution_location` matches the phone Ubuntu environment;
- `ok` is explicitly true;
- artifacts, when present, can be checked by digest.

## Failure rule

Connection failure, wrong job identity, wrong execution location, or failed integrity verification stays a failure.

There is intentionally no “helpful” fallback that runs the work somewhere else and returns a plausible-looking answer.
