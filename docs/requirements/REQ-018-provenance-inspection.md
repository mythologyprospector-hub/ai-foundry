# REQ-018 — Provenance Inspection

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Issue:** #38

## Purpose

Close the remaining Phase 2 provenance-inspection gap without introducing a graph, database, index, or second persistence mechanism.

AI Foundry already preserves the artifacts and reference integrity needed to follow a Run through its existing artifacts. This requirement provides one explicit operation for inspecting that existing provenance chain.

## Scope

- add one explicit Lab-level provenance inspection operation for a preserved Run
- use existing ArtifactStore loading and reference relationships
- expose the Run, its Result, and its Evaluation records as one inspectable provenance view
- preserve stable ordering and existing artifact contracts
- add regression coverage for complete and partially evaluated Runs

## Non-goals

- new persistence mechanisms
- graph/database/index infrastructure
- changing artifact schemas
- automatic provenance generation
- provenance mutation
- ranking or scoring
- UI/services/orchestration
- changing existing evaluation or execution semantics

## Acceptance Criteria

1. A Lab can inspect provenance for an existing Run.
2. The inspection includes the preserved Run and Result and all evaluations linked to that Run.
3. Evaluation ordering is stable.
4. Missing Result is reported explicitly rather than silently omitted.
5. A Run with no evaluations remains inspectable.
6. Existing ArtifactStore persistence and reference-integrity behavior remains unchanged.
7. Tests cover complete, unevaluated, and missing-result cases.
8. No new persistence mechanism or subsystem is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
