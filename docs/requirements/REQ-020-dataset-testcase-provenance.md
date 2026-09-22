# REQ-020 — Preserve Dataset/Test-Case Provenance

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Issue:** #42

## Purpose

Close the concrete provenance gap exposed by the completed experimentation foundation.

Dataset-driven execution already preserves the Dataset and the concrete prompt used by each Run, but the Run record does not explicitly preserve which Dataset and Test Case produced that execution.

## Scope

- preserve optional Dataset identity on dataset-driven Runs
- preserve optional Test Case identity on dataset-driven Runs
- retain compatibility for ordinary runs and legacy Run artifacts
- use the existing Dataset/TestCase artifacts and existing Run provenance structure
- make the relationship inspectable without introducing a graph, index, or second persistence mechanism

## Non-goals

- new persistence mechanisms
- graph/database/index infrastructure
- automatic dataset discovery
- changing Dataset or TestCase semantics
- changing execution behavior
- UI/services/orchestration
- ranking/scoring
- speculative provenance graphs

## Acceptance Criteria

1. A dataset-driven Run explicitly identifies its originating Dataset.
2. A dataset-driven Run explicitly identifies its originating Test Case.
3. The referenced Dataset remains durably preserved by the existing ArtifactStore.
4. Ordinary runs remain valid without dataset/test-case provenance.
5. Existing/legacy Run artifacts remain loadable.
6. Provenance inspection can expose the preserved relationship through the existing Run record.
7. Tests cover dataset-driven identity, ordinary-run compatibility, and legacy loading.
8. No new persistence subsystem is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
