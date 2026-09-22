# REQ-021 — Durable Regression Workflow

**Status:** Proposed  
**Phase:** 2 — Experimentation foundation  
**Issue:** #44

## Purpose

Close the workflow gap between the existing explicit regression check and durable regression records.

The repository can already compare two evaluation collections and can durably preserve individual Regression records, but the Lab has no single explicit operation connecting those existing capabilities.

## Scope

- one Lab-level operation that compares explicit baseline/candidate evaluations
- produce the existing Regression records through the existing Evaluator behavior
- durably preserve each produced Regression using the existing ArtifactStore
- return the produced Regression records
- require referenced evaluations to already exist
- preserve deterministic ordering and existing regression semantics

## Non-goals

- new persistence mechanisms
- new regression schema
- ranking, scoring, or winner selection
- changing regression semantics
- automatic discovery of baseline/candidate evaluations
- UI/services/orchestration
- new graph/index/database infrastructure

## Acceptance Criteria

1. Lab exposes one explicit durable regression workflow.
2. Baseline/candidate evaluation references are validated through existing ArtifactStore behavior.
3. Existing Evaluator regression semantics remain unchanged.
4. Produced Regression records are durably preserved.
5. Returned records equal the preserved records.
6. Regression identifiers are stable and explicit without inventing a new persistence model.
7. Existing missing-baseline/missing-candidate behavior remains representable.
8. Tests cover durable workflow and missing-reference behavior.
9. No new subsystem is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
