# REQ-003 — Dataset and Test Case Foundation

**Status:** Complete
**Phase:** 2 — Experimentation
**Tracking:** GitHub Issue #5

## Purpose

Give AI Foundry a small, explicit way to preserve the inputs used for repeated experimentation and evaluation.

## Why this is next

REQ-002 established preserved experiment and run history. The next missing piece in the Phase 2 laboratory loop is a stable input specimen: a named, inspectable dataset/test-case representation that can be reused rather than embedded ad hoc in individual calls.

This requirement deliberately stops short of evaluation suites, batch orchestration, UI, database-backed storage, or dataset-driven execution.

## Scope

- Define a minimal dataset contract.
- Define a minimal test-case representation within that contract.
- Preserve datasets as human-readable local artifacts.
- Load and enumerate preserved datasets explicitly.
- Preserve enough dataset identity/content to support reproducible evaluation.
- Add automated regression coverage.

## Acceptance criteria

1. A dataset can contain one or more explicit test cases.
2. A test case has a stable identity and explicit input data; expected output/criteria may be represented when present.
3. Dataset artifacts are persisted in a human-readable filesystem form.
4. Re-saving an existing dataset identifier cannot silently replace a different definition.
5. Preserved datasets can be loaded and enumerated through explicit contracts.
6. Tests demonstrate preservation, immutability, loading, and enumeration.
7. The implementation remains small and does not introduce a database, UI, service, orchestration layer, or new communication protocol.
8. Existing REQ-001 and REQ-002 behavior remains intact.

## Engineering constraints

- Python-first.
- Local-first.
- Artifacts over hidden state.
- Reproducibility remains first-class.
- Do not expand runtime architecture.
- Follow established Organ communication conventions only where they apply.

Dataset-driven execution is intentionally deferred. The current laboratory can preserve and retrieve test specimens without changing the existing runtime execution contract.

## Verification evidence

- Owner-machine verification on the REQ-003 branch: **9 passed in 0.04s**.
- GitHub Actions `tests` workflow for commit `15e35e9` completed successfully.
- The test collection warning caused by the domain class name `TestCase` was removed without changing production behavior.
- PR #6 was merged to `main` as commit `b8fac9d07c26178f46d224c32e9a33cbaf2004bb`.
- GitHub Issue #5 was closed as completed.

## Completion condition

REQ-003 is complete when the acceptance criteria are demonstrated by executable implementation and automated tests, with the dataset/test-case contract documented well enough for another developer to inspect and reproduce.
