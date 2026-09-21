# REQ-013 — Explicit Regression Check

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #28

## Purpose

Add the smallest explicit regression-testing capability to the existing evaluation model.

AI Foundry already has durable Evaluation records and EvaluationSuite execution. This requirement makes it possible to inspect whether a candidate run regressed relative to a baseline run without introducing scoring, ranking, or a new evaluation subsystem.

## Contract

Given a baseline collection of Evaluation records and a candidate collection of Evaluation records:

- match evaluations by their existing `name`
- identify cases that passed in the baseline and failed in the candidate
- preserve the explicit baseline/candidate relationship in returned Regression records
- do not assign scores, rankings, percentages, or overall winners
- represent missing evaluation names explicitly
- reject duplicate names rather than silently choosing one
- preserve existing Evaluation and EvaluationSuite contracts

The operation is deterministic and inspectable.

## Deliberate non-goals

Statistical significance, scoring/ranking, automatic winner selection, dataset execution changes, automatic test generation, UI/database/services/training, orchestration/concurrency, new communication protocols, and changes to existing Dataset, TestCase, Result, Evaluation, or EvaluationSuite schemas beyond the additive Regression contract.

## Acceptance Criteria

1. A baseline evaluation set can be compared with a candidate evaluation set.
2. A regression is reported only when a named evaluation passed in the baseline and failed in the candidate.
3. Evaluation names are matched deterministically.
4. Missing evaluation names are represented explicitly.
5. Duplicate evaluation names are rejected rather than silently overwritten.
6. No ranking, score, or winner is produced.
7. Existing single-test and suite evaluation behavior remains unchanged.
8. Regression behavior has focused automated coverage.
9. No new architectural subsystem is introduced.

## Verification

Owner-machine verification is required before merge.
