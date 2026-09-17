# AI Foundry Roadmap

This roadmap describes direction, not a promise of dates or an instruction to implement everything listed immediately.

## Phase 0 — Foundation

- Establish project identity and licensing.
- Define the laboratory concept and working vocabulary.
- Establish architectural boundaries and engineering rules.
- Preserve the established Organ communication conventions where applicable.

## Phase 1 — First Laboratory Loop

Build one complete local path:

**configuration → execution → captured result → preserved experiment**

Then add the minimum testing and evaluation needed to make the result meaningful.

Target capabilities:

- local runtime adapter
- model/configuration representation
- prompt representation
- parameter representation
- execution record
- result persistence
- basic test cases
- basic evaluation
- reproducible experiment record

## Phase 2 — Experimentation

Turn the first loop into a real laboratory.

Potential capabilities:

- experiment definitions
- versioned configurations
- datasets
- evaluation suites
- repeated runs
- controlled comparisons
- regression testing
- provenance inspection
- experiment history

## Phase 3 — Engineering Workbench

Make AI Foundry useful for constructing and maintaining larger AI configurations.

Potential capabilities:

- Modelfile construction
- prompt composition and versioning
- configuration validation
- runtime profiles
- model/provider adapters
- resource controls
- artifact packaging
- import/export
- richer diagnostics

## Phase 4 — Training and Adaptation

Only after the experimentation foundation is trustworthy should training-oriented workflows become a major focus.

Potential capabilities:

- dataset preparation
- fine-tuning configuration
- training job definitions
- adapter/LoRA workflows
- quantization workflows
- training/evaluation comparison
- model artifact provenance

## Phase 5 — Full AI Laboratory

The long-term destination is a coherent environment spanning the AI engineering lifecycle:

**discover → configure → construct → run → observe → test → compare → evaluate → tune → package → reproduce → deploy**

Possible future areas include:

- multi-runtime orchestration
- advanced evaluators
- human evaluation workflows
- automated regression analysis
- hardware/resource awareness
- deployment adapters
- collaboration and review
- richer observability
- experiment knowledge/history

## Scope Discipline

A future capability should earn its place by serving the laboratory's core loop or by providing a clear enabling function.

The project will avoid accumulating disconnected features simply because they are fashionable or technically interesting.

When a proposed feature requires a new architectural concept, its contract and necessity should be established before implementation.
