"""Blinded-task metrics and scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlindedTaskPackage:
    """A blinded review task separated from its answer key."""

    task_id: str
    mode: str
    artifacts: tuple[str, ...]
    answer_key: str


@dataclass(frozen=True, slots=True)
class BlindedTaskResult:
    """One scored blinded-task response."""

    task_id: str
    mode: str
    correct: bool
    decision_time_sec: float
    confidence: float


def package_blinded_task(
    *,
    task_id: str,
    mode: str,
    artifacts: tuple[str, ...],
    answer_key: str,
) -> BlindedTaskPackage:
    """Package one blinded task."""
    return BlindedTaskPackage(
        task_id=task_id,
        mode=mode,
        artifacts=artifacts,
        answer_key=answer_key,
    )


def score_blinded_task(
    package: BlindedTaskPackage,
    *,
    prediction: str,
    decision_time_sec: float,
    confidence: float,
) -> BlindedTaskResult:
    """Score a blinded-task response."""
    return BlindedTaskResult(
        task_id=package.task_id,
        mode=package.mode,
        correct=prediction == package.answer_key,
        decision_time_sec=decision_time_sec,
        confidence=confidence,
    )
