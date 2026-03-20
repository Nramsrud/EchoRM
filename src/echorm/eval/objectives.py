"""Optimization objectives and constraints."""

from __future__ import annotations

from dataclasses import dataclass

from ..eval.validation import ValidationResult


def compute_mean_validation_score(
    results: tuple[ValidationResult, ...],
) -> float:
    """Compute a benchmark-locked validation objective."""
    if not results:
        return 0.0
    penalty = sum(result.lag_error + float(result.false_positive) for result in results)
    return round(max(0.0, 1.0 - (penalty / len(results))), 3)


def enforce_mutation_guard(
    *,
    candidate: dict[str, object],
    allowed_fields: tuple[str, ...],
    prohibited_targets: tuple[str, ...],
) -> None:
    """Reject mutation candidates that reach prohibited surfaces."""
    for key in candidate:
        if key in prohibited_targets:
            raise ValueError(f"prohibited optimization target: {key}")
        if key not in allowed_fields:
            raise ValueError(f"non-mutable optimization field: {key}")


@dataclass(frozen=True, slots=True)
class ObjectiveScorecard:
    """Multi-objective benchmark scorecard."""

    science: float
    sonification: float
    engineering: float
    overall: float

    def to_dict(self) -> dict[str, float]:
        """Serialize the scorecard."""
        return {
            "science": self.science,
            "sonification": self.sonification,
            "engineering": self.engineering,
            "overall": self.overall,
        }


def compute_objective_scorecard(
    results: tuple[ValidationResult, ...],
    *,
    audio_only_accuracy: float,
    plot_only_accuracy: float,
    plot_audio_accuracy: float,
    runtime_sec_mean: float,
    reproducibility_rate: float,
) -> ObjectiveScorecard:
    """Compute a root-scope multi-objective scorecard."""
    science = compute_mean_validation_score(results)
    sonification_gain = max(
        0.0,
        ((audio_only_accuracy - plot_only_accuracy) + plot_audio_accuracy) / 2.0,
    )
    sonification = round(min(1.0, sonification_gain), 3)
    engineering = round(
        max(
            0.0,
            min(1.0, reproducibility_rate)
            * max(0.0, 1.0 - (runtime_sec_mean / 2.0)),
        ),
        3,
    )
    overall = round((science + sonification + engineering) / 3.0, 3)
    return ObjectiveScorecard(
        science=science,
        sonification=sonification,
        engineering=engineering,
        overall=overall,
    )
