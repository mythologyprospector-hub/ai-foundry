# REQ-002 — Experiment History and Immutable Artifacts

**Status:** Proposed
**Phase:** 2 — Experimentation

## Purpose

Turn the working first laboratory loop into a laboratory that can retain an understandable history of experiments and runs without relying on overwritten files or hidden application state.

## Relationship to REQ-001

REQ-001 established one executable, reproducible experiment path. REQ-002 builds only the smallest persistence capability needed to make repeated experimentation safely inspectable.

## Scope

- Preserve distinct experiment definitions without silent overwrite.
- Preserve distinct run and result artifacts for repeated executions.
- Provide explicit retrieval of stored experiment/run history.
- Keep artifacts human-readable and filesystem-based.
- Keep the existing runtime and evaluation boundaries unchanged.

## Acceptance criteria

1. Saving an experiment does not silently replace an existing preserved definition.
2. Repeated runs remain independently identifiable and preserved.
3. Stored experiment history can be enumerated or retrieved through an explicit contract.
4. Existing preserved experiments remain loadable for reproduction.
5. Automated tests demonstrate the history and immutability behavior.
6. The implementation remains small and does not introduce a database, UI, service, orchestration layer, or new communication protocol.

## Engineering constraints

- Python-first.
- Local-first.
- Artifacts over hidden state.
- Reproducibility remains first-class.
- Do not expand runtime architecture.
- Follow established Organ communication conventions only where they apply.

## Completion condition

REQ-002 is complete when the acceptance criteria are demonstrated by executable implementation and automated tests, with the preserved history behavior documented well enough for another developer to inspect and reproduce.
