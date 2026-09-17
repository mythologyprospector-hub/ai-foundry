"""Simple filesystem persistence for experiments, runs, and results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .contracts import Experiment, Result, Run


class ArtifactStore:
    """Persist laboratory artifacts as human-readable JSON files."""

    def __init__(self, root: str | Path = "artifacts") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save_experiment(self, experiment: Experiment) -> Path:
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

    def save_run(self, run: Run) -> Path:
        return self._write("runs", run.run_id, run.to_dict())

    def save_result(self, result: Result) -> Path:
        return self._write("results", result.run_id, result.to_dict())

    def _write(self, kind: str, identifier: str, data: dict[str, Any]) -> Path:
        directory = self.root / kind
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{identifier}.json"
        path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
        return path
