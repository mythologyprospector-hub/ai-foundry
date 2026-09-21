"""Small, inspectable contracts for the AI Foundry laboratory."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class TestCase:
    """One explicit input specimen for an experiment or evaluation."""

    test_case_id: str
    input: str
    expected_output: str | None = None
    criteria: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Dataset:
    """A named, reproducible collection of test cases."""

    dataset_id: str
    test_cases: tuple[TestCase, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvaluationSuite:
    """A named, ordered collection of explicit test cases."""

    suite_id: str
    test_cases: tuple[TestCase, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Experiment:
    """A reproducible definition of one AI experiment."""

    experiment_id: str
    model: str
    prompt: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Run:
    """The execution record connecting an experiment to a result."""

    run_id: str
    experiment_id: str
    started_at: datetime
    finished_at: datetime
    configuration: Mapping[str, Any]
    provenance: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["started_at"] = self.started_at.isoformat()
        data["finished_at"] = self.finished_at.isoformat()
        return data


@dataclass(frozen=True)
class Result:
    """The durable output of a run."""

    run_id: str
    output: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Evaluation:
    """A durable outcome of one explicit test applied to a result."""

    evaluation_id: str
    run_id: str
    name: str
    passed: bool
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Regression:
    """An explicit baseline/candidate evaluation difference requiring inspection."""

    name: str
    status: str
    baseline_evaluation_id: str | None = None
    candidate_evaluation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Comparison:
    """A durable selection of runs for explicit side-by-side comparison."""

    comparison_id: str
    run_ids: tuple[str, ...]
    note: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
