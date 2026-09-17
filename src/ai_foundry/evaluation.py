"""Basic result evaluation contracts for the first laboratory loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .contracts import Result


@dataclass(frozen=True)
class Evaluation:
    """Outcome of one test applied to a result."""

    name: str
    passed: bool
    detail: str = ""


class Evaluator:
    """Run small, explicit tests against a result."""

    def check(
        self,
        result: Result,
        *,
        name: str,
        test: Callable[[str], bool],
        detail: str = "",
    ) -> Evaluation:
        return Evaluation(name=name, passed=bool(test(result.output)), detail=detail)
