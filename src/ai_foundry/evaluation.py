"""Basic result evaluation contracts for the first laboratory loop."""

from __future__ import annotations

from typing import Callable

from .contracts import Evaluation, EvaluationSuite, Regression, Result, TestCase


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

    def compare_evaluations(
        self,
        baseline: tuple[Evaluation, ...],
        candidate: tuple[Evaluation, ...],
    ) -> tuple[Regression, ...]:
        """Identify regressions and missing evaluation names deterministically."""
        baseline_by_name: dict[str, Evaluation] = {}
        for evaluation in baseline:
            if evaluation.name in baseline_by_name:
                raise ValueError(f"duplicate baseline evaluation name: {evaluation.name}")
            baseline_by_name[evaluation.name] = evaluation

        candidate_by_name: dict[str, Evaluation] = {}
        for evaluation in candidate:
            if evaluation.name in candidate_by_name:
                raise ValueError(f"duplicate candidate evaluation name: {evaluation.name}")
            candidate_by_name[evaluation.name] = evaluation

        records: list[Regression] = []
        for name in sorted(baseline_by_name.keys() | candidate_by_name.keys()):
            baseline_evaluation = baseline_by_name.get(name)
            candidate_evaluation = candidate_by_name.get(name)

            if baseline_evaluation is None:
                records.append(
                    Regression(
                        name=name,
                        status="missing-baseline",
                        candidate_evaluation_id=candidate_evaluation.evaluation_id,
                    )
                )
                continue

            if candidate_evaluation is None:
                records.append(
                    Regression(
                        name=name,
                        status="missing-candidate",
                        baseline_evaluation_id=baseline_evaluation.evaluation_id,
                    )
                )
                continue

            if baseline_evaluation.passed and not candidate_evaluation.passed:
                records.append(
                    Regression(
                        name=name,
                        status="regression",
                        baseline_evaluation_id=baseline_evaluation.evaluation_id,
                        candidate_evaluation_id=candidate_evaluation.evaluation_id,
                    )
                )

        return tuple(records)
