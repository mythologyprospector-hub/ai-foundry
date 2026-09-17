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
