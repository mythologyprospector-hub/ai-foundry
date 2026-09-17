from pathlib import Path

from ai_foundry.contracts import Experiment
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
