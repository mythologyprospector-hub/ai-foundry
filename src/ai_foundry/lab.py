"""Execution of the first AI Foundry laboratory loop."""

from __future__ import annotations

from uuid import uuid4

from .contracts import Dataset, Evaluation, Experiment, Result, Run, utc_now
from .evaluation import Evaluator
from .runtime import RuntimeAdapter
from .store import ArtifactStore


class Lab:
    """Coordinate definition, execution, and preservation of one experiment."""

    def __init__(self, runtime: RuntimeAdapter, store: ArtifactStore) -> None:
        self.runtime = runtime
        self.store = store
        self.evaluator = Evaluator()

    def evaluate(
        self,
        result: Result,
        *,
        name: str,
        test,
        detail: str = "",
        evaluation_id: str,
    ) -> Evaluation:
        """Evaluate a preserved result and durably preserve the evaluation."""
        evaluation = self.evaluator.check(
            result,
            name=name,
            test=test,
            detail=detail,
            evaluation_id=evaluation_id,
        )
        self.store.save_evaluation(evaluation)
        return evaluation

    def run_dataset(self, experiment: Experiment, dataset: Dataset) -> tuple[tuple[Run, Result], ...]:
        """Execute one experiment once for each test case in dataset order."""
        self.store.save_experiment(experiment)
        self.store.save_dataset(dataset)
        return tuple(
            self._run(experiment, prompt=case.input)
            for case in dataset.test_cases
        )

    def run_repeated(self, experiment: Experiment, count: int) -> tuple[tuple[Run, Result], ...]:
        """Execute one experiment a finite number of times in sequence."""
        if count < 1:
            raise ValueError("count must be at least 1")
        return tuple(self.run(experiment) for _ in range(count))

    def run(self, experiment: Experiment) -> tuple[Run, Result]:
        self.store.save_experiment(experiment)
        return self._run(experiment)

    def _run(self, experiment: Experiment, *, prompt: str | None = None) -> tuple[Run, Result]:
        run_id = uuid4().hex
        started_at = utc_now()
        output = self.runtime.generate(
            model=experiment.model,
            prompt=experiment.prompt if prompt is None else prompt,
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
                "prompt": experiment.prompt if prompt is None else prompt,
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
