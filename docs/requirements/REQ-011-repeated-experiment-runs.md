# REQ-011 — Repeated Experiment Runs

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #24

## Purpose

Allow one preserved Experiment definition to be executed repeatedly while preserving each Run and Result as distinct artifacts.

## Scope

- explicit finite repeated-run operation
- caller-controlled positive run count
- sequential execution through the existing Lab path
- preservation through the existing ArtifactStore
- return runs/results in execution order
- regression coverage

## Deliberate non-goals

- scheduling
- concurrency
- distributed execution
- automatic retry policy
- dataset-driven batch execution
- statistical aggregation or ranking
- UI, database, remote services, training
- new communication protocol or orchestration subsystem

## Acceptance Criteria

1. A caller can request a finite number of runs for one Experiment.
2. Each execution receives a distinct Run ID and Result artifact.
3. Existing preservation and overwrite protections remain in force.
4. Returned runs/results have deterministic correspondence and execution order.
5. Existing single-run behavior remains unchanged.
6. Invalid counts are rejected explicitly.
7. Regression tests cover repeated execution.
8. No new architectural subsystem is introduced.

## Engineering Constraints

Python-first, local-first, artifact-based, reproducible, smallest justified vertical slice.

## Verification

Owner-machine verification is required before merge.
