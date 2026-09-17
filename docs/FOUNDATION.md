# AI Foundry Foundation

## Purpose

AI Foundry is a laboratory for engineering AI behavior.

The project is not primarily a chat application. Its central object is the **AI configuration as an engineered, testable artifact**.

A configuration may combine a model, instructions, templates, runtime parameters, tools, datasets, evaluation criteria, and other controlled inputs. The Studio should make those ingredients visible, manipulable, testable, and reproducible.

## The Core Loop

The first complete capability is not "AI training." It is the smallest useful laboratory loop:

**define → run → observe → test → evaluate → compare → preserve → reproduce**

Every later capability should strengthen this loop rather than bypass it.

## Working Model

- **Model** — an available inference/training model or model artifact.
- **Configuration** — the explicit settings used to operate a model.
- **Prompt** — instructions or structured input that influences model behavior.
- **Experiment** — a controlled execution of a defined configuration against defined inputs.
- **Dataset** — a named, versionable collection of inputs and/or expected outputs used for experimentation or evaluation.
- **Evaluation** — a measurement or judgment applied to an experiment result.
- **Result** — the recorded output and associated evidence from an execution.
- **Artifact** — a preserved, identifiable piece of the engineering process.
- **Provenance** — the record connecting a result to the inputs, configuration, runtime, and process that produced it.

These are working definitions. They become canonical only when established by project documentation and implementation contracts.

## Initial Boundary

The project will begin with local model execution and configuration management. Ollama is an intended early runtime adapter because it provides a practical local model interface and Modelfile-based configuration, but AI Foundry must not make one runtime the definition of the architecture.

Future adapters may support other local or remote runtimes where there is a clear engineering reason to do so.

## Engineering Rules

1. **Contracts before complexity.** Define the data and behavioral contracts before building elaborate interfaces around them.
2. **Artifacts over hidden state.** Important configuration and experiment information should be inspectable and persistable.
3. **Reproducibility is a feature.** A result without sufficient provenance is an incomplete experiment.
4. **Tests are part of the laboratory.** Functionality is not finished merely because it produces an output.
5. **Separate concerns.** Model execution, configuration, experimentation, evaluation, storage, and presentation should not become one inseparable component.
6. **Prefer local operation.** External services are adapters, not assumptions.
7. **Don't invent infrastructure twice.** Where the established Organ communication protocol applies, use its Registry, BUS, correlation, health, error, and telemetry conventions.
8. **Supervised automation.** Automation must have explicit boundaries and should never quietly turn an experiment into an uncontrolled operation.
9. **Build vertically.** Prefer one small end-to-end working slice over many disconnected subsystems.
10. **Harden continuously.** Integration, failure handling, validation, and documentation are ongoing work, not a final cleanup phase.

## What This Document Does Not Do

This document does not freeze the final architecture, prescribe every future subsystem, or authorize speculative features merely because they are technically possible.

The long-term vision is deliberately larger than the first implementation. Architecture should be earned by working requirements.

## Authorization Model

AI Foundry development is supervised by the project owner. Autonomous implementation is permitted only within the scope explicitly authorized for the current step. Destructive or consequential operations require explicit authorization.

The GitHub repository for this project is the sole implementation workspace. Existing repositories outside this project are not development targets.
