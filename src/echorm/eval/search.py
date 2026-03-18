"""Search-backend adapters."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .objectives import enforce_mutation_guard


@dataclass(frozen=True, slots=True)
class SearchTrial:
    """One optimization trial."""

    params: dict[str, object]
    objective: float


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
