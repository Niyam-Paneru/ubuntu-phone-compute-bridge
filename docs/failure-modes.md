# Failure modes

## Unknown job name
A caller asks for work outside the reviewed registry. Response: reject before transport.

## Phone is unreachable
The remote worker cannot be contacted. Response: fail visibly; do not silently execute on Windows.

## Wrong execution location
A result claims it ran somewhere other than the expected phone Ubuntu environment. Response: reject the result.

## Job/result mismatch
The caller asked for one job and received output labeled as another. Response: reject.

## Artifact bytes changed
Returned bytes do not match the expected digest. Response: mark integrity verification failed.

## Host identity changed
The transport no longer matches the reviewed host identity. Response: stop and investigate rather than auto-accepting.
