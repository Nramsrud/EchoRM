from __future__ import annotations

from echorm.eval.objectives import (
    compute_mean_validation_score,
    compute_objective_scorecard,
    enforce_mutation_guard,
)
from echorm.eval.search import run_backend_search, run_grid_search
from echorm.eval.validation import ValidationResult


def test_objective_calculation_uses_validation_outputs() -> None:
    results = (
        ValidationResult("a", "clean", 0.1, True, False, 1.0),
        ValidationResult("b", "clean", 0.0, True, False, 1.2),
    )
    assert compute_mean_validation_score(results) == 0.95


def test_mutation_guards_reject_prohibited_targets() -> None:
    try:
        enforce_mutation_guard(
            candidate={"benchmark_labels": "mutate"},
            allowed_fields=("mapping_family",),
            prohibited_targets=("benchmark_labels", "discovery_pool"),
        )
    except ValueError as error:
        assert "prohibited optimization target" in str(error)
    else:
        raise AssertionError("expected prohibited optimization target to fail")


def test_grid_search_respects_trial_budget_and_field_guards() -> None:
    trials = run_grid_search(
        candidates=(
            {"mapping_family": "echo_ensemble"},
            {"mapping_family": "token_stream"},
        ),
        evaluator=lambda candidate: (
            1.0 if candidate["mapping_family"] == "echo_ensemble" else 0.7
        ),
        allowed_fields=("mapping_family",),
        prohibited_targets=("benchmark_labels", "discovery_pool"),
        trial_budget=1,
    )
    assert len(trials) == 1
    assert trials[0].params["mapping_family"] == "echo_ensemble"


def test_backend_search_emits_multi_objective_scorecards() -> None:
    results = (
        ValidationResult("a", "clean", 0.1, True, False, 1.0),
        ValidationResult("b", "clean", 0.0, True, False, 1.2),
    )
    backend = run_backend_search(
        backend_name="optuna",
        candidates=({"mapping_family": "echo_ensemble"},),
        evaluator=lambda candidate: compute_objective_scorecard(
            results,
            audio_only_accuracy=0.8,
            plot_only_accuracy=0.6,
            plot_audio_accuracy=0.9,
            runtime_sec_mean=0.4,
            reproducibility_rate=1.0,
        ),
        allowed_fields=("mapping_family",),
        prohibited_targets=("benchmark_labels", "discovery_pool"),
        trial_budget=1,
    )
    assert backend.backend_name == "optuna"
    assert backend.best_scorecard.overall > 0.0
    trial_payload = backend.trials[0].to_dict()
    scorecard = trial_payload["scorecard"]
    assert isinstance(scorecard, dict)
    assert float(str(scorecard["science"])) > 0.0
