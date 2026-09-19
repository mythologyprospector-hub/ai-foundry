# REQ-012 — Dataset-Driven Experiment Runs

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #26

## Purpose

Connect the existing Dataset/TestCase artifact to execution so a preserved Experiment can be run against each explicit test case without introducing batch/orchestration infrastructure.

## Contract

For each TestCase, the existing Experiment's model and parameters are retained and the TestCase input becomes the concrete prompt for one sequential Lab run. The resulting Run configuration therefore records the actual input used.

An empty Dataset produces no runs.

## Deliberate non-goals

Scheduling, concurrency, distributed execution, retries, statistical aggregation/ranking, automatic evaluation, schema changes, UI/database/services/training, and new communication protocols.

## Acceptance Criteria

1. One Experiment can be executed against one Dataset.
2. Each TestCase produces exactly one distinct Run and Result.
3. Dataset/TestCase order is preserved in returned execution records.
4. Existing preservation/integrity protections remain in force.
5. Run configuration records the concrete TestCase input.
6. Existing single-run and repeated-run behavior remains unchanged.
7. Successful and empty-dataset behavior are tested.
8. No new architectural subsystem is introduced.

## Verification

Owner-machine verification is required before merge.
