# Decisions

## Named jobs instead of free-form work

The public bridge accepts a tiny registry of reviewed job names. The point is to make the behavior inspectable, not to recreate a general remote terminal.

## Result location is part of correctness

A valid result must identify the expected execution environment. Silent fallback to the controller would make benchmarking and verification misleading.

## Integrity is checked separately

Returned bytes can be compared with an expected digest. This proves byte identity, not semantic correctness.

## Machine-specific details stay private

Device addresses, keys, host fingerprints, and personal setup notes do not belong in this public proof.

> Small device. Small API. Normal-sized skepticism.
