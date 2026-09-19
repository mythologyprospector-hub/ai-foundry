# REQ-008 — Result History Enumeration

**Status:** Proposed  
**Phase:** 2 — Experimentation  
**Tracking Issue:** #16

## Purpose

Complete the durable result-history surface by adding explicit enumeration to the existing result save/load capability.

## Scope

- enumerate preserved results
- stable identifier ordering
- optional filtering by run ID
- preserve existing behavior
- regression tests
- requirement documentation

## Deliberate non-goals

Dataset-driven execution, batch orchestration, automatic ranking, scoring/statistics frameworks, UI, database, remote service, new communication protocol, and training/fine-tuning.

## Acceptance Criteria

1. Preserved results can be enumerated.
2. Enumeration is deterministic by result/run identifier.
3. Results can be filtered by run ID.
4. Existing save/load behavior remains intact.
5. Automated regression tests cover enumeration and filtering.
6. REQ-001 through REQ-007 remain intact.
7. No new architectural subsystem is introduced.

## Verification

Owner-machine verification is required before merge using `uv run pytest -q`.
