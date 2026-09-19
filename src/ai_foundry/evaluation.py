"""Basic result evaluation contracts for the first laboratory loop."""

from __future__ import annotations

from typing import Callable

from .contracts import Evaluation, EvaluationSuite, Result, TestCase


class Evaluator:
    """Run small, explicit tests against a result."""

    def check(
        self,
        result: Result,
        *,
        name: str,
        test: Callable[[str], bool],
        detail: str = "",
        evaluation_id: str | None = None,
    ) -> Evaluation:
        """Apply one explicit test and return its inspectable evaluation."""
        if evaluation_id is None:
            raise ValueError("evaluation_id is required for a durable evaluation")
        return Evaluation(
            evaluation_id=evaluation_id,
            run_id=result.run_id,
            name=name,
            passed=bool(test(result.output)),
            detail=detail,
        )

    def run_suite(
        self,
        result: Result,
        suite: EvaluationSuite,
        *,
        test: Callable[[str, TestCase], bool],
    ) -> tuple[Evaluation, ...]:
        """Apply one explicit test function to every case in suite order."""
        return tuple(
            self.check(
                result,
                name=case.test_case_id,
                test=lambda output, case=case: test(output, case),
                evaluation_id=f"{suite.suite_id}:{case.test_case_id}",
            )
            for case in suite.test_cases
        )
