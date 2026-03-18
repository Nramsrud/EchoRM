"""Benchmark validation metrics."""

from __future__ import annotations

from dataclasses import dataclass

from ..simulate.benchmarks import BenchmarkRealization


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Validation metrics for one benchmark object."""

    object_uid: str
    family: str
    lag_error: float
    interval_contains_truth: bool
    false_positive: bool
    runtime_sec: float


def validate_benchmark(
    *,
    realization: BenchmarkRealization,
    recovered_lag: float,
    interval: tuple[float, float],
    runtime_sec: float,
) -> ValidationResult:
    """Score one benchmark result against truth."""
    truth_lag = realization.truth.delay_steps
    return ValidationResult(
        object_uid=str(realization.lag_record["object_uid"]),
        family=realization.truth.family,
        lag_error=round(abs(recovered_lag - truth_lag), 3),
        interval_contains_truth=interval[0] <= truth_lag <= interval[1],
        false_positive=recovered_lag > 0 and realization.truth.family == "failure_case",
        runtime_sec=runtime_sec,
    )
