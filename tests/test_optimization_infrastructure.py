from __future__ import annotations

from echorm.eval.objectives import compute_mean_validation_score, enforce_mutation_guard
from echorm.eval.search import run_grid_search
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
