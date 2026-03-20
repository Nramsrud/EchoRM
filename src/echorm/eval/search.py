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
    best_params: dict[str, object]
    best_scorecard: ObjectiveScorecard


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
    ordered = tuple(
        sorted(trials, key=lambda trial: trial.scorecard.overall, reverse=True)
    )
    if not ordered:
        zero = ObjectiveScorecard(0.0, 0.0, 0.0, 0.0)
        return SearchBackendResult(
            backend_name=backend_name,
            trials=(),
            best_params={},
            best_scorecard=zero,
        )
    return SearchBackendResult(
        backend_name=backend_name,
        trials=ordered,
        best_params=ordered[0].params,
        best_scorecard=ordered[0].scorecard,
    )
