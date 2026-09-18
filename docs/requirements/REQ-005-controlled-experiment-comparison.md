# REQ-005 — Controlled Experiment Comparison

**Status:** Complete  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #10

## Purpose

Provide the smallest durable form of the **compare** step in AI Foundry's laboratory loop.

REQ-001 through REQ-004 established durable experiment, run, result, dataset/test-case, and evaluation artifacts. This requirement adds an explicit artifact for placing selected runs side-by-side without introducing ranking, scoring, dashboards, or orchestration.

## Scope

- explicit comparison contract
- stable comparison identity
- explicit selection of run IDs
- optional human-readable note and metadata
- human-readable filesystem persistence
- load and stable enumeration
- protection against silent replacement
- regression coverage

## Deliberate non-goals

- automatic model ranking
- universal scoring system
- statistical analysis framework
- batch execution
- dataset-driven execution
- comparison dashboard or UI
- database
- service/orchestration layer
- new communication protocol
- evaluator discovery
- training/fine-tuning

A comparison organizes selected evidence; it does not invent a judgment or scoring framework.

## Acceptance Criteria

1. A comparison is represented by an explicit inspectable contract.
2. A comparison identifies selected runs unambiguously.
3. A comparison is preserved as a human-readable filesystem artifact.
4. Preserved comparisons can be loaded and enumerated.
5. A comparison cannot be silently overwritten by a different definition.
6. Automated regression tests cover the behavior.
7. REQ-001 through REQ-004 remain intact.
8. Runtime execution and the existing architecture are not expanded.

## Engineering Constraints

- Python-first
- local-first
- artifact-based
- reproducible
- small vertical slice
- contracts before complexity
- preserve evaluation as evidence rather than turning comparison into automatic ranking

## Verification

Owner-machine verification is required before merge, using the project's established uv workflow.

## Completion

REQ-005 is complete when the implementation, tests, and documentation provide a small, reproducible, inspectable comparison capability without introducing the excluded architecture or behavior.
