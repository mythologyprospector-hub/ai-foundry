# REQ-016 — Artifact Reference Integrity

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Issue:** #34

## Purpose

Close a provenance/reproducibility gap in persisted artifacts: durable records must not point at Run or Evaluation artifacts that do not exist in the same ArtifactStore.

## Scope

- require every persisted Evaluation to reference an existing Run
- require every persisted Comparison to reference existing Runs
- require every persisted Regression to reference existing Evaluation records when the corresponding ID is present
- preserve existing immutable/idempotent persistence behavior
- add regression coverage for invalid references and valid linked artifacts
- use the existing ArtifactStore only

## Non-goals

- changing artifact schemas or IDs
- adding a graph, database, index, or new persistence mechanism
- changing comparison or regression semantics
- rejecting legitimate missing-side Regression records
- changing existing Run or Result behavior

## Acceptance Criteria

1. `save_evaluation()` rejects an Evaluation whose `run_id` is not present in the store.
2. `save_comparison()` rejects a Comparison when any referenced `run_id` is absent.
3. `save_regression()` rejects only non-`None` baseline/candidate evaluation IDs that are absent.
4. Identical resaves of existing immutable artifacts remain idempotent.
5. Existing valid linked artifacts remain loadable and preservable.
6. Tests cover each invalid-reference case and valid linkage.
7. No new subsystem or persistence mechanism is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
