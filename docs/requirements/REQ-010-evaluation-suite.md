# REQ-010 — Evaluation Suite

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #21

## Purpose

Turn the existing single-test evaluation capability into a repeatable evaluation suite over an existing result.

## Scope

- named evaluation-suite contract composed from existing test cases
- apply one explicit test function to every case in suite order
- produce durable, inspectable Evaluation records
- deterministic evaluation identifiers derived from suite and test-case identifiers
- preserve existing single-test evaluation behavior
- regression coverage

## Deliberate non-goals

- new model/runtime adapters
- orchestration or batch infrastructure
- automatic test generation
- statistical scoring or ranking
- changing the existing Dataset, Result, or Evaluation schemas
- UI, database, remote services, or training
- persistence of a separate suite artifact

## Acceptance Criteria

1. A named suite can be explicitly defined from existing test cases.
2. Applying it to a Result produces one Evaluation per test case.
3. Evaluations are deterministic in suite order and tied to the source run.
4. Existing single-test evaluation behavior remains intact.
5. Existing Evaluation persistence/retrieval remains intact.
6. Regression tests cover suite behavior, including failures.
7. REQ-001 through REQ-009 remain intact.
8. No new architectural subsystem is introduced.

## Engineering Constraints

Python-first, local-first, artifact-based, reproducible, smallest justified vertical slice.

## Verification

Owner-machine verification is required before merge.
