# REQ-009 — Direct Run Retrieval

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #19

## Purpose

Complete the durable run-history retrieval surface.

The artifact store already preserves runs and can enumerate them, but it lacks a direct `load_run(run_id)` operation.

## Scope

- explicit `load_run(run_id)`
- preserve existing `list_runs()` behavior and experiment filtering
- regression coverage for direct loading
- requirement documentation

## Deliberate non-goals

New run schema, provenance expansion, database storage, UI, orchestration, remote services, batch execution, dataset-driven execution, training/fine-tuning, and new communication protocols.

## Acceptance Criteria

1. A preserved run can be loaded directly by run ID.
2. Loaded run content matches the preserved artifact.
3. Existing run enumeration/filtering remains intact.
4. Missing runs retain normal filesystem error behavior.
5. Automated regression coverage is added.
6. REQ-001 through REQ-008 remain intact.
7. No new architectural subsystem is introduced.

## Engineering Constraints

Python-first, local-first, artifact-based, reproducible, smallest justified vertical slice.

## Verification

Owner-machine verification is required before merge.
