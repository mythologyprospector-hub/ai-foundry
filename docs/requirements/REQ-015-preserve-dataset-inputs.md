# REQ-015 — Preserve Dataset-Driven Inputs

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Issue:** #32

## Purpose

Close a reproducibility gap in dataset-driven execution: `Lab.run_dataset()` executes each TestCase but must also preserve the Dataset artifact through the existing ArtifactStore.

## Scope

- preserve the supplied Dataset through the existing ArtifactStore before dataset-driven execution
- keep dataset-driven execution order and Run/Result behavior unchanged
- add regression coverage proving the Dataset survives the operation
- preserve existing dataset integrity protections
- no new persistence mechanism

## Non-goals

- changing Dataset or TestCase schemas
- changing Run or Result schemas
- dataset versioning beyond existing identifiers
- automatic dataset generation
- scheduling, concurrency, orchestration, UI, database, services, or training
- new communication protocols

## Acceptance Criteria

1. `run_dataset()` preserves the supplied Dataset before execution.
2. The preserved Dataset can be loaded through the existing ArtifactStore.
3. Dataset order and existing Run/Result behavior remain unchanged.
4. A conflicting Dataset definition cannot silently replace an existing artifact.
5. Tests cover preservation and existing behavior remains green.
6. No new subsystem or architectural mechanism is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
