from pathlib import Path

import pytest

from ai_foundry.contracts import Dataset, Experiment, TestCase as DatasetTestCase
from ai_foundry.evaluation import Evaluator
from ai_foundry.lab import Lab
from ai_foundry.runtime import RuntimeAdapter
from ai_foundry.store import ArtifactStore


class FakeRuntime(RuntimeAdapter):
    def generate(self, *, model, prompt, parameters):
        return f"{model}: {prompt}"


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


def test_evaluator_applies_explicit_test(tmp_path: Path):
    lab = Lab(FakeRuntime(), ArtifactStore(tmp_path))
    _, result = lab.run(
        Experiment("eval", "fake-model", "hello", {"temperature": 0})
    )

    evaluation = Evaluator().check(
        result,
        name="contains-model-name",
        test=lambda output: "fake-model" in output,
    )

    assert evaluation.passed is True


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
