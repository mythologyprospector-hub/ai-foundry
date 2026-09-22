# REQ-019 — Durable Comparison Workflow

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Issue:** #40

## Purpose

Close the workflow gap between preserved Runs, the existing Comparison contract, and ArtifactStore persistence.

The existing laboratory can execute and preserve Runs. ArtifactStore can preserve Comparison records and enforce Run references. This requirement provides one explicit Lab-level operation connecting those existing pieces.

## Scope

- add one explicit Lab-level comparison operation for existing Runs
- use the existing Comparison contract and ArtifactStore
- preserve the resulting Comparison through the existing store
- return the Comparison to the caller
- require referenced Runs to already exist
- keep Comparison semantics unchanged

## Non-goals

- new persistence mechanisms
- graph/database/index infrastructure
- changing Comparison schema
- automatic comparison after runs
- ranking, scoring, or winner selection
- UI/services/orchestration
- changing Run or Result semantics

## Acceptance Criteria

1. A Lab can create and durably preserve a Comparison from existing Run IDs.
2. The returned Comparison is identical to the persisted Comparison.
3. Existing ArtifactStore reference integrity remains authoritative.
4. Missing Run references are rejected.
5. Existing direct ArtifactStore comparison behavior remains unchanged.
6. Tests cover successful durable comparison and missing Run rejection.
7. No new persistence mechanism or subsystem is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
