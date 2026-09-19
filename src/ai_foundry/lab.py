"""Execution of the first AI Foundry laboratory loop."""

from __future__ import annotations

from uuid import uuid4

from .contracts import Dataset, Experiment, Result, Run, utc_now
from .runtime import RuntimeAdapter
from .store import ArtifactStore


class Lab:
    """Coordinate definition, execution, and preservation of one experiment."""

    def __init__(self, runtime: RuntimeAdapter, store: ArtifactStore) -> None:
        self.runtime = runtime
        self.store = store

    def run_dataset(self, experiment: Experiment, dataset: Dataset) -> tuple[tuple[Run, Result], ...]:
        """Execute one experiment once for each test case in dataset order."""
        return tuple(
            self.run(
                Experiment(
                    experiment_id=experiment.experiment_id,
                    model=experiment.model,
                    prompt=case.input,
                    parameters=experiment.parameters,
                    metadata=experiment.metadata,
                )
            )
            for case in dataset.test_cases
        )

    def run_repeated(self, experiment: Experiment, count: int) -> tuple[tuple[Run, Result], ...]:
        """Execute one experiment a finite number of times in sequence."""
        if count < 1:
            raise ValueError("count must be at least 1")
        return tuple(self.run(experiment) for _ in range(count))

    def run(self, experiment: Experiment) -> tuple[Run, Result]:
        self.store.save_experiment(experiment)
        run_id = uuid4().hex
        started_at = utc_now()
        output = self.runtime.generate(
            model=experiment.model,
            prompt=experiment.prompt,
            parameters=experiment.parameters,
        )
        finished_at = utc_now()

        runtime_type = type(self.runtime)
        run = Run(
            run_id=run_id,
            experiment_id=experiment.experiment_id,
            started_at=started_at,
            finished_at=finished_at,
            configuration={
                "model": experiment.model,
                "prompt": experiment.prompt,
                "parameters": dict(experiment.parameters),
            },
            provenance={
                "runtime_adapter": runtime_type.__qualname__,
                "runtime_module": runtime_type.__module__,
            },
        )
        result = Result(run_id=run_id, output=output)
        self.store.save_run(run)
        self.store.save_result(result)
        return run, result
