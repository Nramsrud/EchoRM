"""Quality-score and review-priority logic."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QualityAssessment:
    """Quality-control outputs for one time series."""

    quality_score: float
    gap_flag: bool
    review_priority: str


def assess_series_quality(
    *,
    mjd_obs: tuple[float, ...],
    quality_flags: tuple[str, ...],
    line_coverage: str,
) -> QualityAssessment:
    """Score a time series without interpolation or hidden smoothing."""
    cadence_gaps = [
        later - earlier
        for earlier, later in zip(mjd_obs, mjd_obs[1:], strict=False)
    ]
    max_gap = max(cadence_gaps, default=0.0)
    gap_flag = max_gap > 5.0
    flagged_fraction = sum(flag != "ok" for flag in quality_flags) / max(
        len(quality_flags), 1
    )
    line_bonus = 0.1 if "Hbeta" in line_coverage else 0.0
    quality_score = max(
        0.0,
        1.0 - flagged_fraction - (0.2 if gap_flag else 0.0) + line_bonus,
    )
    if gap_flag or flagged_fraction > 0.25:
        review_priority = "high"
    elif flagged_fraction > 0.0:
        review_priority = "medium"
    else:
        review_priority = "low"
    return QualityAssessment(
        quality_score=round(quality_score, 3),
        gap_flag=gap_flag,
        review_priority=review_priority,
    )
