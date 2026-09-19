# REQ-006 — Explicit Run Provenance

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #12

## Purpose

Strengthen the laboratory's reproducibility foundation by making the provenance recorded on each run explicit and inspectable.

The run artifact now records the runtime adapter's qualified class name and Python module. This identifies the runtime implementation used without expanding the runtime interface.

## Scope

- explicit runtime adapter provenance
- preserve the existing run/configuration boundaries
- human-readable filesystem persistence
- backward-compatible loading of existing run artifacts
- regression coverage
- documentation of the provenance contract

## Deliberate non-goals

- remote telemetry
- automatic environment fingerprinting
- hardware inventory
- dependency lockfile generation
- model registry
- configuration registry
- database
- UI
- orchestration
- training/fine-tuning
- new communication protocol

## Acceptance Criteria

1. A run records explicit, inspectable provenance sufficient to identify the runtime adapter used.
2. Existing runtime behavior remains unchanged.
3. Provenance survives save/load as part of the run artifact.
4. Existing run artifacts without the new explicit provenance fields remain loadable.
5. Automated regression tests cover the new behavior.
6. REQ-001 through REQ-005 remain intact.
7. No new service, database, UI, orchestration layer, or communication mechanism is introduced.

## Engineering Constraints

- Python-first
- local-first
- artifact-based
- reproducible
- backward-compatible with existing human-readable artifacts
- smallest justified vertical slice
- contracts before complexity

## Verification

Owner-machine verification is required before merge using the established `uv` workflow.

## Completion

REQ-006 is complete when run artifacts contain a small explicit runtime provenance record that is preserved and reloadable without expanding the runtime architecture.
