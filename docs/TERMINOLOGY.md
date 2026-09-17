# AI Foundry Terminology

This document establishes the initial working vocabulary for the project. Terms may be refined as implementation exposes better distinctions.

| Term | Meaning |
|---|---|
| **AI Foundry** | The overall project: a local-first laboratory for engineering AI behavior and AI configurations. |
| **Model** | A model available to an execution or training runtime. |
| **Runtime** | The mechanism that loads or executes a model. |
| **Provider / Adapter** | An integration layer connecting the Foundry to a particular runtime or external capability. |
| **Configuration** | The explicit collection of settings describing how a model is to be operated. |
| **Modelfile** | A runtime-specific model/configuration description, such as an Ollama Modelfile. |
| **Prompt** | Instructions or structured input supplied to a model. |
| **Template** | A reusable structure for assembling prompts, inputs, or other configuration material. |
| **Parameter** | A runtime or generation setting that affects execution behavior. |
| **Dataset** | A named, versionable collection of inputs and/or expected outputs used by experiments or evaluations. |
| **Test Case** | A defined input and expected or checkable behavior used to test a configuration. |
| **Evaluation** | A measurement, comparison, or judgment applied to one or more results. |
| **Experiment** | A controlled execution or set of executions performed against defined inputs and configuration. |
| **Run** | One concrete execution of an experiment or configuration. |
| **Result** | The output and associated execution evidence produced by a run. |
| **Artifact** | A preserved, identifiable object produced or consumed by the engineering process. |
| **Provenance** | Information connecting an artifact or result to the inputs, configuration, runtime, and process involved in producing it. |
| **Reproducibility** | The ability to reconstruct or repeat an experiment from its preserved definition and evidence. |

## Important Distinctions

### Model vs. Configuration

A model is not the complete AI system. A configuration describes how that model is operated and may materially change its behavior.

### Experiment vs. Run

An experiment describes what is being investigated. A run is one execution of that experiment.

### Result vs. Evaluation

A result is what the runtime produced. An evaluation is what the laboratory measures or concludes about that result.

### Artifact vs. Provenance

An artifact is an object. Provenance is the history and relationships that explain where that object came from and how it was produced.

## Naming Rule

Use precise existing terminology where it accurately describes a concept. Do not introduce new names merely to make familiar components sound novel.
