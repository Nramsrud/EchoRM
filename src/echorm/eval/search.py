"""Search-backend adapters."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .objectives import ObjectiveScorecard, enforce_mutation_guard


@dataclass(frozen=True, slots=True)
class SearchTrial:
    """One optimization trial."""

    params: dict[str, object]
    objective: float

    def to_dict(self) -> dict[str, object]:
        """Serialize one simple trial."""
        return {"params": self.params, "objective": self.objective}


@dataclass(frozen=True, slots=True)
class BackendSearchTrial:
    """One backend-normalized optimization trial."""

    params: dict[str, object]
    scorecard: ObjectiveScorecard

    def to_dict(self) -> dict[str, object]:
        """Serialize one backend trial."""
        return {"params": self.params, "scorecard": self.scorecard.to_dict()}


@dataclass(frozen=True, slots=True)
class SearchBackendResult:
    """Normalized result for one optimization backend."""

    backend_name: str
    trials: tuple[BackendSearchTrial, ...]
    pareto_front: tuple[BackendSearchTrial, ...]
    best_params: dict[str, object]
    best_scorecard: ObjectiveScorecard


def _ordered_pareto_trials(
    trials: list[BackendSearchTrial],
) -> tuple[tuple[BackendSearchTrial, ...], tuple[BackendSearchTrial, ...]]:
    if not trials:
        return (), ()
    domination_counts: dict[int, int] = {}
    for index, trial in enumerate(trials):
        domination_counts[index] = sum(
            other.scorecard.dominates(trial.scorecard)
            for other in trials
            if other is not trial
        )
    ordered = tuple(
        trial
        for _index, trial in sorted(
            enumerate(trials),
            key=lambda item: (
                domination_counts[item[0]],
                -item[1].scorecard.representative_utility,
                tuple(-value for value in item[1].scorecard.maximize_vector()),
            ),
        )
    )
    pareto_front = tuple(
        trial
        for index, trial in enumerate(trials)
        if domination_counts[index] == 0
    )
    pareto_front = tuple(
        sorted(
            pareto_front,
            key=lambda trial: (
                -trial.scorecard.representative_utility,
                tuple(-value for value in trial.scorecard.maximize_vector()),
            ),
        )
    )
    return ordered, pareto_front


def run_grid_search(
    *,
    candidates: tuple[dict[str, object], ...],
    evaluator: Callable[[dict[str, object]], float],
    allowed_fields: tuple[str, ...],
    prohibited_targets: tuple[str, ...],
    trial_budget: int,
) -> tuple[SearchTrial, ...]:
    """Run a benchmark-guarded grid search."""
    trials = []
    for candidate in candidates[:trial_budget]:
        enforce_mutation_guard(
            candidate=candidate,
            allowed_fields=allowed_fields,
            prohibited_targets=prohibited_targets,
        )
        objective = float(evaluator(candidate))
        trials.append(SearchTrial(params=candidate, objective=objective))
    return tuple(sorted(trials, key=lambda trial: trial.objective, reverse=True))


def run_backend_search(
    *,
    backend_name: str,
    candidates: tuple[dict[str, object], ...],
    evaluator: Callable[[dict[str, object]], ObjectiveScorecard],
    allowed_fields: tuple[str, ...],
    prohibited_targets: tuple[str, ...],
    trial_budget: int,
) -> SearchBackendResult:
    """Run one backend-normalized benchmark-governed search."""
    trials: list[BackendSearchTrial] = []
    for candidate in candidates[:trial_budget]:
        enforce_mutation_guard(
            candidate=candidate,
            allowed_fields=allowed_fields,
            prohibited_targets=prohibited_targets,
        )
        scorecard = evaluator(candidate)
        trials.append(BackendSearchTrial(params=candidate, scorecard=scorecard))
    ordered, pareto_front = _ordered_pareto_trials(trials)
    if not ordered:
        zero = ObjectiveScorecard(0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
        return SearchBackendResult(
            backend_name=backend_name,
            trials=(),
            pareto_front=(),
            best_params={},
            best_scorecard=zero,
        )
    representative = pareto_front[0] if pareto_front else ordered[0]
    return SearchBackendResult(
        backend_name=backend_name,
        trials=ordered,
        pareto_front=pareto_front,
        best_params=representative.params,
        best_scorecard=representative.scorecard,
    )
