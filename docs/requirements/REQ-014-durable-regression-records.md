# REQ-014 — Durable Regression Records

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Issue:** #30

## Purpose

Make the explicit regression records introduced by REQ-013 durable and inspectable through the existing filesystem artifact store.

## Scope

- persist `Regression` records as human-readable JSON artifacts
- load a regression by stable caller-provided regression identifier
- enumerate preserved regression records in deterministic identifier order
- preserve existing no-silent-overwrite behavior
- add regression persistence tests
- keep `Evaluator.compare_evaluations()` behavior unchanged

## Non-goals

- scoring, ranking, or winner selection
- automatic regression analysis
- changing Evaluation or EvaluationSuite schemas
- databases, UI, services, orchestration, or concurrency
- new communication protocols

## Acceptance Criteria

1. A Regression can be saved as an inspectable artifact.
2. A saved Regression can be loaded by stable identifier.
3. Regression history can be enumerated in stable order.
4. Different content cannot silently replace the same regression identifier.
5. Identical re-save is idempotent.
6. Existing REQ-013 comparison behavior remains unchanged.
7. Tests cover persistence and integrity.
8. No new subsystem or architectural mechanism is introduced.

## Verification

Owner-machine and GitHub Actions verification are required before completion.
