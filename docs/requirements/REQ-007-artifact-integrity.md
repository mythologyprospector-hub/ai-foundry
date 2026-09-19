# REQ-007 — Artifact Integrity Protection

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #14

## Purpose

Harden the artifact store's preservation guarantee so run and result artifacts obey the same no-silent-overwrite rule already established for experiments, datasets, evaluations, and comparisons.

## Scope

- protect run artifacts from silent replacement
- protect result artifacts from silent replacement
- allow idempotent re-save of identical artifacts
- preserve existing loading and enumeration
- regression coverage
- document the integrity rule

## Deliberate non-goals

- database transactions
- locking/concurrency framework
- content-addressed storage
- checksums or signing
- schema migration framework
- UI
- orchestration
- new communication protocol

## Acceptance Criteria

1. Saving a run cannot silently replace a different run with the same ID.
2. Saving a result cannot silently replace a different result with the same run ID.
3. Re-saving an identical run/result remains idempotent.
4. Existing loading and enumeration remain intact.
5. Automated regression tests cover the behavior.
6. REQ-001 through REQ-006 remain intact.
7. No new architectural subsystem is introduced.

## Verification

Owner-machine verification is required before merge using the established `uv` workflow.

## Completion

REQ-007 is complete when run and result preservation obeys the same no-silent-overwrite rule as the other durable artifact types.
