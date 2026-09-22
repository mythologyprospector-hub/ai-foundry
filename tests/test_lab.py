from datetime import datetime, timezone
from pathlib import Path

import pytest

from ai_foundry.contracts import Dataset, Evaluation, Experiment, Regression, Result, Run, RunProvenance, TestCase as DatasetTestCase
from ai_foundry.evaluation import Evaluator
from ai_foundry.lab import Lab
from ai_foundry.runtime import RuntimeAdapter
from ai_foundry.store import ArtifactStore


class FakeRuntime(RuntimeAdapter):
    def generate(self, *, model, prompt, parameters):
        return f"{model}: {prompt}"


def preserve_run(store: ArtifactStore, run_id: str) -> None:
    store.save_run(
        Run(
            run_id=run_id,
            experiment_id=f"experiment-{run_id}",
            started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            finished_at=datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
            configuration={},
        )
    )


def test_experiment_runs_and_persists_artifacts(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))
    experiment = Experiment(
        experiment_id="hello-world",
        model="fake-model",
        prompt="Say hello.",
        parameters={"temperature": 0},
    )

    run, result = lab.run(experiment)

    assert run.experiment_id == "hello-world"
    assert result.run_id == run.run_id
    assert result.output == "fake-model: Say hello."
    assert (tmp_path / "experiments/hello-world.json").exists()
    assert (tmp_path / f"runs/{run.run_id}.json").exists()
    assert (tmp_path / f"results/{run.run_id}.json").exists()
    assert run.provenance == {
        "runtime_adapter": "FakeRuntime",
        "runtime_module": "test_lab",
    }


def test_evaluator_applies_explicit_test(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))
    _, result = lab.run(
        Experiment("eval", "fake-model", "hello", {"temperature": 0})
    )

    evaluation = Evaluator().check(
        result,
        name="contains-model-name",
        test=lambda output: "fake-model" in output,
        evaluation_id="eval-1",
    )

    assert evaluation.passed is True
    assert evaluation.run_id == result.run_id


def test_lab_evaluate_persists_evaluation(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    _, result = lab.run(Experiment("durable-eval", "fake-model", "hello"))

    evaluation = lab.evaluate(
        result,
        name="contains-model",
        test=lambda output: "fake-model" in output,
        evaluation_id="durable-eval-1",
    )

    assert evaluation == store.load_evaluation("durable-eval-1")
    assert evaluation.run_id == result.run_id
    assert evaluation.passed is True


def test_lab_evaluate_rejects_result_without_preserved_run(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    result = Result(run_id="missing-run", output="actual")

    with pytest.raises(FileNotFoundError, match="Evaluation run reference does not exist"):
        lab.evaluate(
            result,
            name="check",
            test=lambda output: True,
            evaluation_id="missing-run-eval",
        )


def test_preserved_experiment_can_be_reloaded_and_run_again(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    original = Experiment(
        experiment_id="reproducible",
        model="fake-model",
        prompt="Repeat this.",
        parameters={"temperature": 0, "seed": 42},
        metadata={"purpose": "reproduction test"},
    )

    first_run, first_result = lab.run(original)
    preserved = store.load_experiment(original.experiment_id)
    second_run, second_result = lab.run(preserved)

    assert preserved == original
    assert second_run.run_id != first_run.run_id
    assert second_run.experiment_id == original.experiment_id
    assert second_result.run_id == second_run.run_id
    assert second_result.output == first_result.output
    assert second_run.configuration == first_run.configuration


def test_experiment_definition_cannot_be_silently_overwritten(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    original = Experiment("immutable", "model-a", "first")
    changed = Experiment("immutable", "model-b", "second")

    store.save_experiment(original)

    with pytest.raises(FileExistsError):
        store.save_experiment(changed)

    assert store.load_experiment("immutable") == original


def test_experiment_history_can_be_enumerated(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    experiments = [
        Experiment("beta", "model-b", "second"),
        Experiment("alpha", "model-a", "first"),
    ]

    for experiment in experiments:
        store.save_experiment(experiment)

    assert store.list_experiments() == [experiments[1], experiments[0]]


def test_results_are_enumerated_in_stable_order(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    first_run, first_result = lab.run(Experiment("history-a", "fake-model", "first"))
    second_run, second_result = lab.run(Experiment("history-b", "fake-model", "second"))

    assert store.list_results() == sorted(
        [first_result, second_result], key=lambda result: result.run_id
    )


def test_results_can_be_filtered_by_run_id(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    first_run, first_result = lab.run(Experiment("filter-a", "fake-model", "first"))
    _, second_result = lab.run(Experiment("filter-b", "fake-model", "second"))

    assert store.list_results(first_run.run_id) == [first_result]
    assert store.list_results(second_result.run_id) == [second_result]


def test_run_can_be_loaded_directly_by_run_id(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, _ = lab.run(Experiment("direct-load", "fake-model", "hello"))

    assert store.load_run(run.run_id) == run


def test_missing_run_load_raises_file_not_found(tmp_path: Path):
    store = ArtifactStore(tmp_path)

    with pytest.raises(FileNotFoundError):
        store.load_run("missing-run")


def test_run_cannot_be_silently_overwritten(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, _ = lab.run(Experiment("run-integrity", "fake-model", "hello"))

    changed = run.__class__(
        run_id=run.run_id,
        experiment_id=run.experiment_id,
        started_at=run.started_at,
        finished_at=run.finished_at,
        configuration={"model": "changed"},
        provenance=run.provenance,
    )

    with pytest.raises(FileExistsError):
        store.save_run(changed)
    assert store.list_runs("run-integrity")[0] == run


def test_result_cannot_be_silently_overwritten(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, result = lab.run(Experiment("result-integrity", "fake-model", "hello"))

    changed = result.__class__(run_id=run.run_id, output="changed")

    with pytest.raises(FileExistsError):
        store.save_result(changed)
    assert store.load_result(run.run_id) == result


def test_run_and_result_identical_resaves_are_idempotent(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, result = lab.run(Experiment("idempotent", "fake-model", "hello"))

    assert store.save_run(run) == tmp_path / f"runs/{run.run_id}.json"
    assert store.save_result(result) == tmp_path / f"results/{run.run_id}.json"


def test_repeated_runs_are_independently_preserved_and_listable(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    experiment = Experiment("repeat", "fake-model", "run me")

    first_run, _ = lab.run(experiment)
    second_run, _ = lab.run(store.load_experiment("repeat"))

    runs = store.list_runs("repeat")

    assert first_run.run_id != second_run.run_id
    assert {run.run_id for run in runs} == {first_run.run_id, second_run.run_id}
    assert all(run.experiment_id == "repeat" for run in runs)


def test_dataset_preserves_explicit_test_cases(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    dataset = Dataset(
        dataset_id="basic",
        test_cases=(
            DatasetTestCase("greeting", "Say hello.", expected_output="Hello."),
            DatasetTestCase("math", "2 + 2", criteria={"exact": "4"}),
        ),
        metadata={"purpose": "foundation test"},
    )

    path = store.save_dataset(dataset)
    preserved = store.load_dataset("basic")

    assert path == tmp_path / "datasets/basic.json"
    assert preserved == dataset
    assert preserved.test_cases[0].expected_output == "Hello."
    assert preserved.test_cases[1].criteria == {"exact": "4"}


def test_dataset_definition_cannot_be_silently_overwritten(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    original = Dataset("immutable", (DatasetTestCase("one", "first"),))
    changed = Dataset("immutable", (DatasetTestCase("one", "second"),))

    store.save_dataset(original)

    with pytest.raises(FileExistsError):
        store.save_dataset(changed)

    assert store.load_dataset("immutable") == original


def test_dataset_history_can_be_loaded_and_enumerated(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    datasets = [
        Dataset("beta", (DatasetTestCase("b", "second"),)),
        Dataset("alpha", (DatasetTestCase("a", "first"),)),
    ]

    for dataset in datasets:
        store.save_dataset(dataset)

    assert store.list_datasets() == [datasets[1], datasets[0]]


def test_evaluation_can_be_preserved_and_reloaded(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-001")
    evaluation = Evaluation(
        evaluation_id="eval-001",
        run_id="run-001",
        name="exact-output",
        passed=True,
        detail="Output matched expected text.",
    )

    path = store.save_evaluation(evaluation)
    preserved = store.load_evaluation("eval-001")

    assert path == tmp_path / "evaluations/eval-001.json"
    assert preserved == evaluation


def test_evaluation_history_can_be_enumerated_and_filtered(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-b")
    preserve_run(store, "run-a")
    evaluations = [
        Evaluation("eval-beta", "run-b", "check-b", False, "failed"),
        Evaluation("eval-alpha", "run-a", "check-a", True, "passed"),
    ]

    for evaluation in evaluations:
        store.save_evaluation(evaluation)

    assert store.list_evaluations() == [evaluations[1], evaluations[0]]
    assert store.list_evaluations("run-a") == [evaluations[1]]


def test_evaluation_cannot_be_silently_overwritten(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-1")
    preserve_run(store, "run-2")
    original = Evaluation("immutable", "run-1", "check", True, "original")
    changed = Evaluation("immutable", "run-2", "check", False, "changed")

    store.save_evaluation(original)

    with pytest.raises(FileExistsError):
        store.save_evaluation(changed)

    assert store.load_evaluation("immutable") == original


def test_comparison_can_be_preserved_and_reloaded(tmp_path: Path):
    from ai_foundry.contracts import Comparison

    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-b")
    preserve_run(store, "run-a")
    comparison = Comparison(
        comparison_id="compare-001",
        run_ids=("run-b", "run-a"),
        note="Compare two explicit runs.",
        metadata={"purpose": "comparison test"},
    )

    path = store.save_comparison(comparison)
    preserved = store.load_comparison("compare-001")

    assert path == tmp_path / "comparisons/compare-001.json"
    assert preserved == comparison


def test_comparison_history_can_be_enumerated(tmp_path: Path):
    from ai_foundry.contracts import Comparison

    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-b")
    preserve_run(store, "run-a")
    comparisons = [
        Comparison("compare-beta", ("run-b",)),
        Comparison("compare-alpha", ("run-a", "run-b")),
    ]

    for comparison in comparisons:
        store.save_comparison(comparison)

    assert store.list_comparisons() == [comparisons[1], comparisons[0]]


def test_comparison_cannot_be_silently_overwritten(tmp_path: Path):
    from ai_foundry.contracts import Comparison

    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-1")
    preserve_run(store, "run-2")
    original = Comparison("immutable", ("run-1",), "original")
    changed = Comparison("immutable", ("run-2",), "changed")

    store.save_comparison(original)

    with pytest.raises(FileExistsError):
        store.save_comparison(changed)

    assert store.load_comparison("immutable") == original


def test_run_provenance_survives_save_and_reload(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, _ = lab.run(Experiment("provenance", "fake-model", "hello"))

    preserved = store.list_runs("provenance")[0]

    assert preserved.run_id == run.run_id
    assert preserved.provenance == run.provenance
    assert preserved.provenance["runtime_adapter"] == "FakeRuntime"
    assert preserved.provenance["runtime_module"] == "test_lab"


def test_legacy_run_without_explicit_provenance_fields_remains_loadable(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    path = tmp_path / "runs/legacy.json"
    path.parent.mkdir(parents=True)
    path.write_text(
        '{"run_id":"legacy","experiment_id":"old","started_at":"2026-01-01T00:00:00+00:00",'
        '"finished_at":"2026-01-01T00:00:01+00:00","configuration":{},"provenance":{"runtime":"OldRuntime"}}',
        encoding="utf-8",
    )

    run = store.list_runs()[0]

    assert run.run_id == "legacy"
    assert run.provenance == {"runtime": "OldRuntime"}


def test_evaluation_suite_applies_one_evaluation_per_case_in_order(tmp_path: Path):
    from ai_foundry.contracts import EvaluationSuite

    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))
    _, result = lab.run(Experiment("suite", "fake-model", "hello"))
    suite = EvaluationSuite(
        suite_id="basic-suite",
        test_cases=(
            DatasetTestCase("contains-model", "ignored"),
            DatasetTestCase("contains-prompt", "ignored"),
        ),
    )

    evaluations = Evaluator().run_suite(
        result,
        suite,
        test=lambda output, case: (
            ("fake-model" in output)
            if case.test_case_id == "contains-model"
            else ("hello" in output)
        ),
    )

    assert evaluations == (
        Evaluation(
            evaluation_id="basic-suite:contains-model",
            run_id=result.run_id,
            name="contains-model",
            passed=True,
        ),
        Evaluation(
            evaluation_id="basic-suite:contains-prompt",
            run_id=result.run_id,
            name="contains-prompt",
            passed=True,
        ),
    )


def test_evaluation_suite_can_record_failures_without_ranking(tmp_path: Path):
    from ai_foundry.contracts import EvaluationSuite

    result = Result(
        run_id="run-suite",
        output="actual",
    )
    suite = EvaluationSuite(
        suite_id="failure-suite",
        test_cases=(DatasetTestCase("exact", "ignored"),),
    )

    evaluations = Evaluator().run_suite(
        result,
        suite,
        test=lambda output, case: output == "expected",
    )

    assert len(evaluations) == 1
    assert evaluations[0].passed is False
    assert evaluations[0].run_id == "run-suite"
    assert evaluations[0].evaluation_id == "failure-suite:exact"


def test_evaluation_suite_preserves_single_test_behavior(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))
    _, result = lab.run(Experiment("single", "fake-model", "hello"))

    evaluation = Evaluator().check(
        result,
        name="single-check",
        test=lambda output: output == "fake-model: hello",
        evaluation_id="single-1",
    )

    assert evaluation.passed is True
    assert evaluation.evaluation_id == "single-1"


def test_lab_dataset_run_preserves_dataset(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    dataset = Dataset(
        "preserved-dataset",
        (
            DatasetTestCase("case-a", "first"),
            DatasetTestCase("case-b", "second"),
        ),
    )
    experiment = Experiment("dataset-preserve", "fake-model", "unused")

    runs = lab.run_dataset(experiment, dataset)

    assert store.load_dataset(dataset.dataset_id) == dataset
    assert len(runs) == 2
    assert [run.configuration["prompt"] for run, _ in runs] == ["first", "second"]


def test_lab_can_execute_a_finite_number_of_repeated_runs(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    experiment = Experiment("repeat-api", "fake-model", "repeat me")

    runs = lab.run_repeated(experiment, 3)

    assert len(runs) == 3
    assert len({run.run_id for run, _ in runs}) == 3
    assert len({result.run_id for _, result in runs}) == 3
    assert [run.experiment_id for run, _ in runs] == ["repeat-api"] * 3
    assert [result.run_id for _, result in runs] == [run.run_id for run, _ in runs]
    assert len(store.list_runs("repeat-api")) == 3


def test_lab_repeated_runs_require_a_positive_count(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))

    with pytest.raises(ValueError, match="count must be at least 1"):
        lab.run_repeated(Experiment("repeat-invalid", "fake-model", "repeat"), 0)



def test_lab_can_execute_an_experiment_against_dataset_in_order(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    experiment = Experiment("dataset-run", "fake-model", "unused")
    dataset = Dataset(
        "inputs",
        (
            DatasetTestCase("first", "alpha"),
            DatasetTestCase("second", "beta"),
        ),
    )

    runs = lab.run_dataset(experiment, dataset)

    assert len(runs) == 2
    assert [result.output for _, result in runs] == [
        "fake-model: alpha",
        "fake-model: beta",
    ]
    assert [run.configuration["prompt"] for run, _ in runs] == ["alpha", "beta"]
    assert [result.run_id for _, result in runs] == [run.run_id for run, _ in runs]
    assert len(store.list_runs("dataset-run")) == 2


def test_lab_dataset_execution_of_empty_dataset_returns_no_runs(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    experiment = Experiment("dataset-empty", "fake-model", "unused")

    assert lab.run_dataset(experiment, Dataset("empty", ())) == ()
    assert store.list_runs("dataset-empty") == []


def test_evaluator_reports_regressions_and_missing_names_deterministically(tmp_path: Path):
    baseline = (
        Evaluation("base-b", "run-base", "beta", True),
        Evaluation("base-a", "run-base", "alpha", True),
        Evaluation("base-stable", "run-base", "stable", False),
    )
    candidate = (
        Evaluation("candidate-new", "run-candidate", "gamma", True),
        Evaluation("candidate-a", "run-candidate", "alpha", False),
        Evaluation("candidate-stable", "run-candidate", "stable", False),
    )

    records = Evaluator().compare_evaluations(baseline, candidate)

    assert records == (
        Regression(
            name="alpha",
            status="regression",
            baseline_evaluation_id="base-a",
            candidate_evaluation_id="candidate-a",
        ),
        Regression(
            name="beta",
            status="missing-candidate",
            baseline_evaluation_id="base-b",
        ),
        Regression(
            name="gamma",
            status="missing-baseline",
            candidate_evaluation_id="candidate-new",
        ),
        Regression(
            name="stable",
            status="missing-candidate",
            baseline_evaluation_id="base-stable",
        ),
    )


def test_evaluator_does_not_report_unchanged_pass_or_fail_as_regression():
    baseline = (
        Evaluation("base-pass", "run-base", "pass", True),
        Evaluation("base-fail", "run-base", "fail", False),
    )
    candidate = (
        Evaluation("candidate-pass", "run-candidate", "pass", True),
        Evaluation("candidate-fail", "run-candidate", "fail", False),
    )

    assert Evaluator().compare_evaluations(baseline, candidate) == ()


def test_evaluator_rejects_duplicate_evaluation_names():
    duplicate = (
        Evaluation("one", "run-base", "same", True),
        Evaluation("two", "run-base", "same", False),
    )

    with pytest.raises(ValueError, match="duplicate baseline evaluation name"):
        Evaluator().compare_evaluations(duplicate, ())


def test_regression_can_be_preserved_and_reloaded(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-base")
    preserve_run(store, "run-candidate")
    store.save_evaluation(Evaluation("base", "run-base", "accuracy", True))
    store.save_evaluation(Evaluation("candidate", "run-candidate", "accuracy", False))
    regression = Regression(
        name="accuracy",
        status="regression",
        baseline_evaluation_id="base",
        candidate_evaluation_id="candidate",
    )

    path = store.save_regression("regression-001", regression)

    assert path == tmp_path / "regressions/regression-001.json"
    assert store.load_regression("regression-001") == regression


def test_regression_history_is_enumerated_in_stable_order(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-base")
    preserve_run(store, "run-candidate")
    store.save_evaluation(Evaluation("base-b", "run-base", "beta", True))
    store.save_evaluation(Evaluation("base-a", "run-base", "alpha", True))
    store.save_evaluation(Evaluation("candidate-a", "run-candidate", "alpha", False))
    regressions = {
        "regression-beta": Regression("beta", "missing-candidate", baseline_evaluation_id="base-b"),
        "regression-alpha": Regression("alpha", "regression", "base-a", "candidate-a"),
    }

    for regression_id, regression in regressions.items():
        store.save_regression(regression_id, regression)

    assert store.list_regressions() == [
        regressions["regression-alpha"],
        regressions["regression-beta"],
    ]


def test_regression_cannot_be_silently_overwritten(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-base")
    preserve_run(store, "run-candidate")
    store.save_evaluation(Evaluation("base", "run-base", "accuracy", True))
    store.save_evaluation(Evaluation("candidate", "run-candidate", "accuracy", False))
    original = Regression("accuracy", "regression", "base", "candidate")
    changed = Regression("accuracy", "missing-candidate", "base", None)

    store.save_regression("immutable", original)

    with pytest.raises(FileExistsError):
        store.save_regression("immutable", changed)

    assert store.load_regression("immutable") == original


def test_regression_identical_resave_is_idempotent(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-base")
    preserve_run(store, "run-candidate")
    store.save_evaluation(Evaluation("base", "run-base", "accuracy", True))
    store.save_evaluation(Evaluation("candidate", "run-candidate", "accuracy", False))
    regression = Regression("accuracy", "regression", "base", "candidate")

    path = store.save_regression("repeat", regression)

    assert store.save_regression("repeat", regression) == path


def test_evaluation_rejects_missing_run_reference(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    with pytest.raises(FileNotFoundError, match="Evaluation run reference does not exist"):
        store.save_evaluation(Evaluation("eval-missing", "run-missing", "check", True))


def test_comparison_rejects_missing_run_reference(tmp_path: Path):
    from ai_foundry.contracts import Comparison
    store = ArtifactStore(tmp_path)
    with pytest.raises(FileNotFoundError, match="Comparison run reference does not exist"):
        store.save_comparison(Comparison("compare-missing", ("run-missing",)))


def test_regression_rejects_missing_evaluation_reference(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    with pytest.raises(FileNotFoundError, match="Regression evaluation reference does not exist"):
        store.save_regression("regression-missing", Regression("accuracy", "regression", "eval-missing", None))


def test_regression_allows_legitimate_missing_side(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    preserve_run(store, "run-base")
    store.save_evaluation(Evaluation("base", "run-base", "accuracy", True))
    regression = Regression("accuracy", "missing-candidate", baseline_evaluation_id="base")
    assert store.save_regression("missing-candidate", regression).exists()


def test_regression_record_is_inspectable():
    regression = Regression(
        name="accuracy",
        status="regression",
        baseline_evaluation_id="base",
        candidate_evaluation_id="candidate",
    )

    assert regression.to_dict() == {
        "name": "accuracy",
        "status": "regression",
        "baseline_evaluation_id": "base",
        "candidate_evaluation_id": "candidate",
    }


def test_lab_inspects_complete_run_provenance(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, result = lab.run(Experiment("inspect", "fake-model", "hello"))
    lab.evaluate(
        result,
        name="contains-model",
        test=lambda output: "fake-model" in output,
        evaluation_id="inspect-eval",
    )

    provenance = lab.inspect_provenance(run.run_id)

    assert provenance == RunProvenance(
        run=run,
        result=result,
        evaluations=(store.load_evaluation("inspect-eval"),),
    )


def test_lab_inspects_run_without_evaluations(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, result = lab.run(Experiment("unevaluated", "fake-model", "hello"))

    provenance = lab.inspect_provenance(run.run_id)

    assert provenance.run == run
    assert provenance.result == result
    assert provenance.evaluations == ()


def test_lab_provenance_inspection_reports_missing_result(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    run, _ = lab.run(Experiment("missing-result", "fake-model", "hello"))
    (tmp_path / f"results/{run.run_id}.json").unlink()

    with pytest.raises(FileNotFoundError):
        lab.inspect_provenance(run.run_id)


def test_lab_compare_persists_comparison(tmp_path: Path):
    from ai_foundry.contracts import Comparison

    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    first_run, _ = lab.run(Experiment("compare-a", "fake-model", "first"))
    second_run, _ = lab.run(Experiment("compare-b", "fake-model", "second"))

    comparison = lab.compare(
        (first_run.run_id, second_run.run_id),
        comparison_id="durable-comparison-1",
        note="Compare two runs.",
        metadata={"purpose": "workflow test"},
    )

    assert comparison == Comparison(
        comparison_id="durable-comparison-1",
        run_ids=(first_run.run_id, second_run.run_id),
        note="Compare two runs.",
        metadata={"purpose": "workflow test"},
    )
    assert comparison == store.load_comparison("durable-comparison-1")


def test_lab_compare_rejects_missing_run_reference(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)

    with pytest.raises(FileNotFoundError, match="Comparison run reference does not exist"):
        lab.compare(
            ("missing-run",),
            comparison_id="missing-run-comparison",
        )


def test_lab_dataset_run_preserves_dataset_and_test_case_provenance(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    dataset = Dataset(
        "provenance-dataset",
        (DatasetTestCase("case-a", "first"),),
    )

    run, _ = lab.run_dataset(
        Experiment("dataset-provenance", "fake-model", "unused"),
        dataset,
    )[0]

    assert run.provenance["dataset_id"] == "provenance-dataset"
    assert run.provenance["test_case_id"] == "case-a"
    assert store.load_dataset("provenance-dataset") == dataset


def test_lab_ordinary_run_has_no_dataset_test_case_provenance(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))

    run, _ = lab.run(Experiment("ordinary-provenance", "fake-model", "hello"))

    assert "dataset_id" not in run.provenance
    assert "test_case_id" not in run.provenance


def test_lab_regress_persists_regression_records(tmp_path: Path):
    store = ArtifactStore(tmp_path)
    lab = Lab(FakeRuntime(), store)
    preserve_run(store, "run-base")
    preserve_run(store, "run-candidate")
    store.save_evaluation(Evaluation("base-alpha", "run-base", "alpha", True))
    store.save_evaluation(Evaluation("base-stable", "run-base", "stable", False))
    store.save_evaluation(Evaluation("candidate-alpha", "run-candidate", "alpha", False))
    store.save_evaluation(Evaluation("candidate-new", "run-candidate", "gamma", True))

    regressions = lab.regress(
        ("base-alpha", "base-stable"),
        ("candidate-alpha", "candidate-new"),
        regression_id_prefix="comparison-1",
    )

    assert regressions == (
        Regression(
            name="alpha",
            status="regression",
            baseline_evaluation_id="base-alpha",
            candidate_evaluation_id="candidate-alpha",
        ),
        Regression(
            name="gamma",
            status="missing-baseline",
            candidate_evaluation_id="candidate-new",
        ),
    )
    assert store.load_regression("comparison-1-0") == regressions[0]
    assert store.load_regression("comparison-1-1") == regressions[1]
    assert store.list_regressions() == list(regressions)


def test_lab_regress_requires_preserved_evaluations(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))

    with pytest.raises(FileNotFoundError):
        lab.regress(
            ("missing-baseline",),
            ("missing-candidate",),
            regression_id_prefix="missing",
        )
