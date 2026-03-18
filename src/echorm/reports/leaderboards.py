"""Validation and efficacy report builders."""

from __future__ import annotations

from ..eval.efficacy import BlindedTaskResult
from ..eval.validation import ValidationResult


def build_validation_leaderboard(
    results: tuple[ValidationResult, ...],
) -> list[dict[str, object]]:
    """Build a compact validation leaderboard."""
    ranked = sorted(results, key=lambda result: (result.lag_error, result.runtime_sec))
    return [
        {
            "rank": index + 1,
            "object_uid": result.object_uid,
            "family": result.family,
            "lag_error": result.lag_error,
            "runtime_sec": result.runtime_sec,
        }
        for index, result in enumerate(ranked)
    ]


def build_efficacy_leaderboard(
    results: tuple[BlindedTaskResult, ...],
) -> list[dict[str, object]]:
    """Build a compact efficacy leaderboard."""
    ranked = sorted(
        results,
        key=lambda result: (
            -int(result.correct),
            result.decision_time_sec,
            -result.confidence,
        ),
    )
    return [
        {
            "rank": index + 1,
            "task_id": result.task_id,
            "mode": result.mode,
            "correct": result.correct,
            "decision_time_sec": result.decision_time_sec,
        }
        for index, result in enumerate(ranked)
    ]
