"""pyZDCF-style adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun, TimeSeries, build_pair_id


@dataclass(frozen=True, slots=True)
class PyzdcfConfig:
    """Configuration for the pyZDCF-style adapter."""

    max_lag: int = 5
    min_pairs: int = 2


def _paired_differences(
    driver: TimeSeries,
    response: TimeSeries,
    lag: int,
) -> list[float]:
    return [
        abs(left - right)
        for left, right in zip(driver.values, response.values[lag:], strict=False)
    ]


def run_pyzdcf(
    *,
    object_uid: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: PyzdcfConfig | None = None,
) -> LagRun:
    """Run a thin pyZDCF-style adapter over sampled series."""
    config = config or PyzdcfConfig()
    lag_scores = {}
    for lag in range(0, min(config.max_lag + 1, len(response.values))):
        differences = _paired_differences(driver, response, lag)
        lag_scores[lag] = 1.0 / (1.0 + (sum(differences) / max(len(differences), 1)))
    best_lag = max(lag_scores, key=lag_scores.__getitem__)
    pair_density = max(len(driver.values) - best_lag, 0)
    return LagRun(
        object_uid=object_uid,
        pair_id=build_pair_id(driver, response),
        driver_channel=driver.channel,
        response_channel=response.channel,
        method="pyzdcf",
        lag_median=float(best_lag),
        lag_lo=float(max(0, best_lag - 1)),
        lag_hi=float(min(config.max_lag, best_lag + 1)),
        significance=round(lag_scores[best_lag], 3),
        alias_score=round(1.0 / max(pair_density, 1), 3),
        quality_score=0.85,
        diagnostics={
            "sparse_sampling_pairs": pair_density,
            "zdcf_bins": tuple(sorted(lag_scores)),
            "min_pairs": config.min_pairs,
        },
        runtime_metadata={
            "config": {
                "max_lag": config.max_lag,
                "min_pairs": config.min_pairs,
            }
        },
    )
