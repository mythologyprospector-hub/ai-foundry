# REQ-004 — Persisted Evaluation Record

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #8

## Purpose

Provide a durable, inspectable evaluation record for the laboratory loop.

## Scope

- explicit `Evaluation` contract with stable identity
- association of an evaluation with the evaluated `run_id`
- human-readable filesystem persistence
- loading and enumeration of evaluations
- optional enumeration filtering by run ID
- protection against silently replacing a different evaluation
- regression coverage
- explicit evaluation IDs for durable evaluator output

## Deliberate non-goals

Evaluation suites, batch execution, dataset-driven execution, evaluator discovery, scoring frameworks, comparison dashboards, UI, database/service/orchestration expansion, and new communication protocols.

## Acceptance Criteria

1. Evaluations have explicit stable identities.
2. Evaluations retain the run they describe.
3. Evaluation records are preserved as human-readable artifacts.
4. Preserved evaluations can be loaded and enumerated, including filtering by run ID.
5. A different evaluation cannot silently replace an existing evaluation with the same ID.
6. Automated regression tests cover persistence, enumeration/filtering, and immutability.
7. The existing laboratory execution path remains intact without introducing a new subsystem.

## Verification

Owner-machine verification:

```
uv run pytest -q
12 passed in 0.05s
```

GitHub Actions:

- workflow run #16
- conclusion: success
- verified implementation commit: `204f6120bcec9d699de9fffcd34ccb2323233cf8`

Implementation merged to `main` in PR #9 as merge commit `66d62971b4ee2e441fa5ab41c19ac35ea4b7792f`.

Issue #8 closed as completed.
