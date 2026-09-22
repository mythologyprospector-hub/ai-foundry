# AI Foundry

**A local-first AI engineering studio for building, configuring, testing, evaluating, and reproducing AI systems.**

AI Foundry is intended to be a serious workshop for the *engineering of AI behavior* — not simply another chat interface.

The project aims to bring the pieces involved in constructing an AI system into one coherent, inspectable, reproducible environment: models, Modelfiles, prompts, templates, parameters, datasets, experiments, evaluations, runtime behavior, and eventually training and packaging.

## Vision

AI development is increasingly spread across model runtimes, configuration files, prompt editors, experiment trackers, evaluation tools, training frameworks, and deployment systems.

AI Foundry's long-term goal is to provide a unified laboratory around those activities.

The central idea is simple:

> **Models are experimental materials. Configurations are experimental apparatus. Datasets are test specimens. Runs are experiments. Evaluations are measurements. Results are evidence.**

A useful AI configuration should be something that can be inspected, tested, compared, versioned, reproduced, and eventually shared or deployed with confidence.

## Long-Term Scope

The vision encompasses the full AI engineering lifecycle:

**discover → configure → construct → run → observe → test → compare → evaluate → tune → package → reproduce → deploy**

Potential areas include:

- Model and runtime management
- Modelfile construction
- Prompt and system-instruction engineering
- Prompt templates and reusable components
- Model parameters and runtime controls
- Configuration versioning
- Dataset preparation and management
- Evaluation sets and regression tests
- Controlled experiments and model comparisons
- Human and automated evaluation
- Experiment provenance and reproducibility
- Fine-tuning and training workflows
- Quantization and packaging
- Runtime execution and resource controls
- Logs, telemetry, and diagnostics
- Git-native artifacts and history
- Local-first operation with extensible runtime adapters

This is a **long-term vision**, not a promise that every capability will exist in the first release.

## Design Principles

### Local-first

AI Foundry should work locally whenever practical. External services may be supported through explicit adapters rather than becoming hidden dependencies.

### Reproducible

A meaningful result should preserve enough configuration and provenance to understand how it was produced and, where practical, reproduce it.

### Inspectable

Important behavior should be represented as understandable artifacts rather than buried inside opaque application state.

### Experimental

The system should make controlled experimentation easy: change one thing, run it, measure it, compare it, and retain the evidence.

### Git-native

Configurations, prompts, tests, datasets, experiment definitions, and other appropriate artifacts should be versionable and reviewable.

### Python-first

Core engineering and services should favor Python where practical, with presentation layers remaining separate from the underlying system logic.

### Modular

Runtime providers, model backends, evaluators, and other integrations should be replaceable rather than defining the entire architecture.

### Safety-conscious

Operations that can create meaningful side effects should have explicit controls and clear boundaries. Automation should be supervised rather than assumed to be harmless.

## Communication Architecture

AI Foundry will use the established Organ communication conventions where applicable rather than creating competing communication mechanisms.

The reference architecture establishes:

- A standard HTTP surface through the shared organ base
- Registry-based service discovery and heartbeat
- Request correlation through `X-Correlation-ID`
- Communications BUS pub/sub and dispatch semantics
- Persistent consumer cursors and dispatch state
- Best-effort telemetry kept separate from safety/risk gating
- Consistent JSON error conventions

See the project's communication reference and subsequent canonical documentation as the implementation develops.

## Development Philosophy

AI Foundry is deliberately intended to be developed incrementally.

The architecture may eventually become large, but individual capabilities should remain understandable, testable, and independently useful.

The project will favor:

1. Clear contracts before implementation.
2. Small capabilities before large abstractions.
3. Tests alongside functionality.
4. Integration and hardening as first-class work.
5. Explicit provenance over implicit magic.
6. Working local capabilities before premature distributed infrastructure.

## Current Status

**Phase 2 — Experimentation foundation established.**

The initial laboratory loop and the core experimentation foundation are complete through **REQ-018**. AI Foundry now has explicit, durable contracts for experiments, datasets, runs, results, evaluations, comparisons, regressions, provenance, and their reference integrity.

The current implementation supports:

- repeated and dataset-driven runs
- durable experiment/run/result/evaluation/comparison/regression artifacts
- evaluation suites and explicit regression checks
- preserved dataset inputs
- artifact reference-integrity enforcement
- explicit durable evaluation through the Lab
- direct provenance inspection of a preserved Run

The repository remains intentionally small and local-first. The next capabilities should be driven by inspection of the completed system and demonstrated engineering pressure rather than by speculative architecture.

Phase 1's first laboratory loop was verified with automated tests, GitHub Actions, and a live local Ollama run. Phase 2 has continued through incremental, verified requirements with the same artifact-first and reproducibility constraints.

## Author

**James Earl Stambaugh III**  
`mythologyprospector@gmail.com`

## License

AI Foundry is released under the **MIT License**. See [LICENSE](LICENSE).
