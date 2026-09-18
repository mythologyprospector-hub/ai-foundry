# REQ-001 — First Laboratory Loop

**Status:** Complete
**Phase:** 1 — First Laboratory Loop
**Tracking:** GitHub Issue #1

## Purpose

Establish the first executable vertical slice of AI Foundry.

## Core loop

`define → run → observe → test → evaluate → compare → preserve → reproduce`

The first implementation does not need to expose the entire loop as a polished user interface. It does need to establish the underlying contracts and artifacts that make the loop real and reproducible.

## Initial outcome

AI Foundry must be able to represent a small AI experiment as explicit artifacts, execute it through a runtime adapter, capture the result, evaluate it with basic tests, and preserve enough information to reproduce the run.

## Scope

- Local runtime adapter boundary
- Model/configuration representation
- Prompt and parameter representation
- Execution/run record
- Result persistence
- Basic tests/evaluation
- Reproducible experiment record

## Constraints

- Python-first
- Local-first
- Artifacts over hidden state
- Reproducibility is a first-class requirement
- Tests are included with implementation
- Runtime-specific details remain behind an adapter boundary
- Follow the established Organ communication conventions where they apply; do not invent a second communication protocol
- No training system, distributed orchestration, or speculative architecture in this requirement

## Acceptance criteria

1. A minimal experiment can be defined as inspectable data.
2. A local model can be invoked through a runtime adapter.
3. The invocation produces a durable run/result record.
4. The run contains sufficient configuration and provenance to understand what was executed.
5. A basic evaluation/test can be run against the result.
6. The experiment can be repeated from its preserved definition.
7. Automated tests cover the implemented contracts.

## Verification evidence

- Local automated suite: **3 passed in 0.02s** on the reproducibility implementation branch.
- GitHub Actions `tests` workflow for commit `72c54fb` completed successfully.
- Live local runtime verification was executed with Ollama `0.30.6` and local model `llama3.1:8b`.
- The live run returned the expected test response and produced experiment, run, and result artifacts.
- Reproducibility implementation was merged to `main` as commit `b790969`.

## Implementation guidance

Start with the smallest useful vertical slice. Do not introduce a framework, service, database, UI, or abstraction merely because the long-term vision may eventually need one.

A component earns its place when the current contracts demonstrate that it is needed. Runtime integrations should remain replaceable, experiment definitions should remain inspectable, and persisted results should retain enough provenance to explain a run without relying on hidden application state.

## Communication boundary

Where AI Foundry participates in the established Organ communication environment, use the existing conventions for discovery, heartbeat, correlation IDs, BUS communication, dispatch state, telemetry, and error envelopes. This requirement does not define a new communication protocol.

## Completion condition

REQ-001 is complete when the acceptance criteria are demonstrated by an executable implementation and automated tests, with the resulting artifacts documented well enough that another developer can inspect and reproduce the basic experiment flow.
