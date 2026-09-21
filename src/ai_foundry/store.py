"""Simple filesystem persistence for laboratory artifacts."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .contracts import Comparison, Dataset, Evaluation, Experiment, Regression, Result, Run, TestCase


class ArtifactStore:
    """Persist laboratory artifacts as human-readable JSON files."""

    def __init__(self, root: str | Path = "artifacts") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save_dataset(self, dataset: Dataset) -> Path:
        """Preserve a dataset; identical definitions may be reused."""
        path = self.root / "datasets" / f"{dataset.dataset_id}.json"
        if path.exists():
            preserved = self.load_dataset(dataset.dataset_id)
            if preserved != dataset:
                raise FileExistsError(
                    f"Dataset already preserved with a different definition: "
                    f"{dataset.dataset_id}"
                )
            return path
        return self._write("datasets", dataset.dataset_id, dataset.to_dict())

    def load_dataset(self, dataset_id: str) -> Dataset:
        """Load a preserved dataset definition."""
        path = self.root / "datasets" / f"{dataset_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Dataset(
            dataset_id=str(data["dataset_id"]),
            test_cases=tuple(
                TestCase(
                    test_case_id=str(case["test_case_id"]),
                    input=str(case["input"]),
                    expected_output=(
                        None
                        if case.get("expected_output") is None
                        else str(case["expected_output"])
                    ),
                    criteria=dict(case.get("criteria", {})),
                )
                for case in data["test_cases"]
            ),
            metadata=dict(data.get("metadata", {})),
        )

    def list_datasets(self) -> list[Dataset]:
        """Return preserved datasets in stable identifier order."""
        directory = self.root / "datasets"
        if not directory.exists():
            return []
        return [
            self.load_dataset(path.stem)
            for path in sorted(directory.glob("*.json"), key=lambda item: item.name)
        ]

    def save_experiment(self, experiment: Experiment) -> Path:
        """Preserve an experiment definition without silently changing it."""
        path = self.root / "experiments" / f"{experiment.experiment_id}.json"
        if path.exists():
            preserved = self.load_experiment(experiment.experiment_id)
            if preserved != experiment:
                raise FileExistsError(
                    f"Experiment already preserved with a different definition: "
                    f"{experiment.experiment_id}"
                )
            return path
        return self._write("experiments", experiment.experiment_id, experiment.to_dict())

    def load_experiment(self, experiment_id: str) -> Experiment:
        """Load a preserved experiment definition from the artifact store."""
        path = self.root / "experiments" / f"{experiment_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Experiment(
            experiment_id=str(data["experiment_id"]),
            model=str(data["model"]),
            prompt=str(data["prompt"]),
            parameters=dict(data.get("parameters", {})),
            metadata=dict(data.get("metadata", {})),
        )

    def list_experiments(self) -> list[Experiment]:
        """Return preserved experiment definitions in stable identifier order."""
        directory = self.root / "experiments"
        if not directory.exists():
            return []
        return [
            self.load_experiment(path.stem)
            for path in sorted(directory.glob("*.json"), key=lambda item: item.name)
        ]

    def save_run(self, run: Run) -> Path:
        """Preserve a run without silently changing it."""
        path = self.root / "runs" / f"{run.run_id}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            existing = Run(
                run_id=str(data["run_id"]),
                experiment_id=str(data["experiment_id"]),
                started_at=datetime.fromisoformat(data["started_at"]),
                finished_at=datetime.fromisoformat(data["finished_at"]),
                configuration=dict(data.get("configuration", {})),
                provenance=dict(data.get("provenance", {})),
            )
            if existing != run:
                raise FileExistsError(
                    f"Run already preserved with a different definition: {run.run_id}"
                )
            return path
        return self._write("runs", run.run_id, run.to_dict())

    def load_run(self, run_id: str) -> Run:
        """Load a preserved run by run ID."""
        path = self.root / "runs" / f"{run_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Run(
            run_id=str(data["run_id"]),
            experiment_id=str(data["experiment_id"]),
            started_at=datetime.fromisoformat(data["started_at"]),
            finished_at=datetime.fromisoformat(data["finished_at"]),
            configuration=dict(data.get("configuration", {})),
            provenance=dict(data.get("provenance", {})),
        )

    def save_result(self, result: Result) -> Path:
        """Preserve a result without silently changing it."""
        path = self.root / "results" / f"{result.run_id}.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            existing = Result(
                run_id=str(data["run_id"]),
                output=str(data["output"]),
                metadata=dict(data.get("metadata", {})),
            )
            if existing != result:
                raise FileExistsError(
                    f"Result already preserved with a different definition: {result.run_id}"
                )
            return path
        return self._write("results", result.run_id, result.to_dict())

    def load_result(self, run_id: str) -> Result:
        """Load a preserved result."""
        path = self.root / "results" / f"{run_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Result(
            run_id=str(data["run_id"]),
            output=str(data["output"]),
            metadata=dict(data.get("metadata", {})),
        )

    def list_results(self, run_id: str | None = None) -> list[Result]:
        """Return preserved results, optionally limited to one run."""
        directory = self.root / "results"
        if not directory.exists():
            return []

        results: list[Result] = []
        for path in sorted(directory.glob("*.json"), key=lambda item: item.name):
            result = self.load_result(path.stem)
            if run_id is None or result.run_id == run_id:
                results.append(result)
        return results

    def list_runs(self, experiment_id: str | None = None) -> list[Run]:
        """Return preserved runs, optionally limited to one experiment."""
        directory = self.root / "runs"
        if not directory.exists():
            return []

        runs: list[Run] = []
        for path in sorted(directory.glob("*.json"), key=lambda item: item.name):
            run = self.load_run(path.stem)
            if experiment_id is None or run.experiment_id == experiment_id:
                runs.append(run)
        return runs

    def save_evaluation(self, evaluation: Evaluation) -> Path:
        """Preserve an evaluation without silently changing it."""
        path = self.root / "evaluations" / f"{evaluation.evaluation_id}.json"
        if path.exists():
            preserved = self.load_evaluation(evaluation.evaluation_id)
            if preserved != evaluation:
                raise FileExistsError(
                    f"Evaluation already preserved with a different definition: "
                    f"{evaluation.evaluation_id}"
                )
            return path
        return self._write("evaluations", evaluation.evaluation_id, evaluation.to_dict())

    def load_evaluation(self, evaluation_id: str) -> Evaluation:
        """Load a preserved evaluation record."""
        path = self.root / "evaluations" / f"{evaluation_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Evaluation(
            evaluation_id=str(data["evaluation_id"]),
            run_id=str(data["run_id"]),
            name=str(data["name"]),
            passed=bool(data["passed"]),
            detail=str(data.get("detail", "")),
        )

    def list_evaluations(self, run_id: str | None = None) -> list[Evaluation]:
        """Return preserved evaluations, optionally limited to one run."""
        directory = self.root / "evaluations"
        if not directory.exists():
            return []

        evaluations: list[Evaluation] = []
        for path in sorted(directory.glob("*.json"), key=lambda item: item.name):
            evaluation = self.load_evaluation(path.stem)
            if run_id is None or evaluation.run_id == run_id:
                evaluations.append(evaluation)
        return evaluations

    def save_regression(self, regression_id: str, regression: Regression) -> Path:
        """Preserve a regression under a stable caller-provided identifier."""
        path = self.root / "regressions" / f"{regression_id}.json"
        if path.exists():
            preserved = self.load_regression(regression_id)
            if preserved != regression:
                raise FileExistsError(
                    f"Regression already preserved with a different definition: {regression_id}"
                )
            return path
        return self._write("regressions", regression_id, regression.to_dict())

    def load_regression(self, regression_id: str) -> Regression:
        """Load a preserved regression record by stable identifier."""
        path = self.root / "regressions" / f"{regression_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Regression(
            name=str(data["name"]),
            status=str(data["status"]),
            baseline_evaluation_id=(
                None
                if data.get("baseline_evaluation_id") is None
                else str(data["baseline_evaluation_id"])
            ),
            candidate_evaluation_id=(
                None
                if data.get("candidate_evaluation_id") is None
                else str(data["candidate_evaluation_id"])
            ),
        )

    def list_regressions(self) -> list[Regression]:
        """Return preserved regressions in stable identifier order."""
        directory = self.root / "regressions"
        if not directory.exists():
            return []
        return [
            self.load_regression(path.stem)
            for path in sorted(directory.glob("*.json"), key=lambda item: item.name)
        ]

    def save_comparison(self, comparison: Comparison) -> Path:
        """Preserve a comparison without silently changing it."""
        path = self.root / "comparisons" / f"{comparison.comparison_id}.json"
        if path.exists():
            preserved = self.load_comparison(comparison.comparison_id)
            if preserved != comparison:
                raise FileExistsError(
                    f"Comparison already preserved with a different definition: "
                    f"{comparison.comparison_id}"
                )
            return path
        return self._write("comparisons", comparison.comparison_id, comparison.to_dict())

    def load_comparison(self, comparison_id: str) -> Comparison:
        """Load a preserved comparison."""
        path = self.root / "comparisons" / f"{comparison_id}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return Comparison(
            comparison_id=str(data["comparison_id"]),
            run_ids=tuple(str(run_id) for run_id in data["run_ids"]),
            note=str(data.get("note", "")),
            metadata=dict(data.get("metadata", {})),
        )

    def list_comparisons(self) -> list[Comparison]:
        """Return preserved comparisons in stable identifier order."""
        directory = self.root / "comparisons"
        if not directory.exists():
            return []
        return [
            self.load_comparison(path.stem)
            for path in sorted(directory.glob("*.json"), key=lambda item: item.name)
        ]

    def _write(self, kind: str, identifier: str, data: dict[str, Any]) -> Path:
        directory = self.root / kind
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{identifier}.json"
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        return path
