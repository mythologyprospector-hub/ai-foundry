# REQ-017 — Durable Evaluation Workflow

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Issue:** #36

## Purpose

Close the workflow gap between a preserved Run/Result and a durable Evaluation.

The existing laboratory can execute and preserve Runs and Results. The existing Evaluator can construct explicit Evaluation records, and ArtifactStore can preserve them. This requirement provides one explicit Lab-level operation connecting those existing pieces.

## Scope

- add one explicit Lab-level evaluation operation for a Result
- use the existing Evaluator contract and ArtifactStore
- preserve the resulting Evaluation through the existing store
- return the Evaluation to the caller
- keep the existing Evaluator.check API intact

## Non-goals

- evaluation suites
- automatic evaluation after every run
- changing evaluation semantics
- new evaluator registries/plugins
- databases, services, UI, or orchestration
- automatic ranking or scoring
- changing Run/Result contracts

## Acceptance Criteria

1. A Lab can evaluate a supplied Result using the existing explicit test contract.
2. The resulting Evaluation is durably preserved.
3. REQ-016 reference integrity is enforced through the existing ArtifactStore.
4. The Evaluation returned is identical to the persisted Evaluation.
5. Existing direct Evaluator behavior remains unchanged.
6. Tests cover successful durable evaluation and missing Run rejection.
7. No new persistence mechanism or subsystem is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
