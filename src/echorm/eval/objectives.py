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

    m1_lag_recovery_mae: float
    m2_coverage_calibration: float
    m3_null_false_positive_rate: float
    m4_anomaly_detection_score: float
    m5_audio_discriminability: float
    m6_runtime_efficiency: float
    m7_interpretability_score: float

    @property
    def representative_utility(self) -> float:
        """Return one display-only aggregate for ordering within a Pareto front."""
        maximize_vector = self.maximize_vector()
        return round(sum(maximize_vector) / len(maximize_vector), 3)

    def maximize_vector(self) -> tuple[float, float, float, float, float, float, float]:
        """Return a normalized maximize-only objective vector."""
        return (
            round(1.0 / (1.0 + self.m1_lag_recovery_mae), 3),
            self.m2_coverage_calibration,
            round(max(0.0, 1.0 - self.m3_null_false_positive_rate), 3),
            self.m4_anomaly_detection_score,
            self.m5_audio_discriminability,
            self.m6_runtime_efficiency,
            self.m7_interpretability_score,
        )

    def dominates(self, other: ObjectiveScorecard) -> bool:
        """Return whether this scorecard Pareto-dominates another."""
        this_vector = self.maximize_vector()
        other_vector = other.maximize_vector()
        return all(
            this >= that for this, that in zip(this_vector, other_vector, strict=True)
        ) and any(
            this > that for this, that in zip(this_vector, other_vector, strict=True)
        )

    def to_dict(self) -> dict[str, float]:
        """Serialize the scorecard."""
        return {
            "m1_lag_recovery_mae": self.m1_lag_recovery_mae,
            "m2_coverage_calibration": self.m2_coverage_calibration,
            "m3_null_false_positive_rate": self.m3_null_false_positive_rate,
            "m4_anomaly_detection_score": self.m4_anomaly_detection_score,
            "m5_audio_discriminability": self.m5_audio_discriminability,
            "m6_runtime_efficiency": self.m6_runtime_efficiency,
            "m7_interpretability_score": self.m7_interpretability_score,
            "representative_utility": self.representative_utility,
        }


def compute_objective_scorecard(
    results: tuple[ValidationResult, ...],
    *,
    audio_only_accuracy: float,
    plot_only_accuracy: float,
    plot_audio_accuracy: float,
    runtime_sec_mean: float,
    reproducibility_rate: float,
    anomaly_precision_at_k: float = 0.0,
    anomaly_auc: float = 0.0,
    interpretability_penalty: float = 0.0,
) -> ObjectiveScorecard:
    """Compute a root-scope multi-objective scorecard."""
    lag_recovery_mae = round(
        sum(result.lag_error for result in results) / max(len(results), 1),
        3,
    )
    coverage_calibration = round(
        sum(result.interval_contains_truth for result in results)
        / max(len(results), 1),
        3,
    )
    null_false_positive_rate = round(
        sum(float(result.false_positive) for result in results) / max(len(results), 1),
        3,
    )
    anomaly_detection_score = round(
        max(0.0, min(1.0, (anomaly_precision_at_k + anomaly_auc) / 2.0)),
        3,
    )
    audio_discriminability = round(
        max(
            0.0,
            min(
                1.0,
                (
                    max(0.0, audio_only_accuracy - plot_only_accuracy)
                    + plot_audio_accuracy
                )
                / 2.0,
            ),
        ),
        3,
    )
    runtime_efficiency = round(
        max(
            0.0,
            min(1.0, reproducibility_rate)
            * max(0.0, 1.0 - (runtime_sec_mean / 2.0)),
        ),
        3,
    )
    interpretability_score = round(max(0.0, 1.0 - interpretability_penalty), 3)
    return ObjectiveScorecard(
        m1_lag_recovery_mae=lag_recovery_mae,
        m2_coverage_calibration=coverage_calibration,
        m3_null_false_positive_rate=null_false_positive_rate,
        m4_anomaly_detection_score=anomaly_detection_score,
        m5_audio_discriminability=audio_discriminability,
        m6_runtime_efficiency=runtime_efficiency,
        m7_interpretability_score=interpretability_score,
    )
