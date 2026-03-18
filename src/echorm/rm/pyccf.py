"""PyCCF-style adapter."""

from __future__ import annotations

from dataclasses import dataclass

from .base import LagRun, TimeSeries, build_pair_id


@dataclass(frozen=True, slots=True)
class PyccfConfig:
    """Configuration for the PyCCF-style adapter."""

    max_lag: int = 5
    fr_rss_samples: int = 4


def _lag_correlation(driver: TimeSeries, response: TimeSeries, lag: int) -> float:
    paired = zip(driver.values, response.values[lag:], strict=False)
    products = [left * right for left, right in paired]
    return sum(products) / max(len(products), 1)


def run_pyccf(
    *,
    object_uid: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: PyccfConfig | None = None,
) -> LagRun:
    """Run a thin PyCCF-style adapter over sampled series."""
    config = config or PyccfConfig()
    lag_scores = {
        lag: _lag_correlation(driver, response, lag)
        for lag in range(0, min(config.max_lag + 1, len(response.values)))
    }
    peak_lag = max(lag_scores, key=lag_scores.__getitem__)
    fr_rss_distribution = tuple(
        max(0, min(config.max_lag, peak_lag + offset))
        for offset in range(-(config.fr_rss_samples // 2), config.fr_rss_samples // 2)
    )
    lag_lo = float(min(fr_rss_distribution, default=peak_lag))
    lag_hi = float(max(fr_rss_distribution, default=peak_lag))
    return LagRun(
        object_uid=object_uid,
        pair_id=build_pair_id(driver, response),
        driver_channel=driver.channel,
        response_channel=response.channel,
        method="pyccf",
        lag_median=float(peak_lag),
        lag_lo=lag_lo,
        lag_hi=lag_hi,
        significance=round(lag_scores[peak_lag], 3),
        alias_score=round(1.0 / (1.0 + peak_lag), 3),
        quality_score=0.9,
        diagnostics={
            "centroid_lag": float(peak_lag),
            "peak_lag": float(peak_lag),
            "fr_rss_distribution": fr_rss_distribution,
        },
        runtime_metadata={
            "config": {
                "max_lag": config.max_lag,
                "fr_rss_samples": config.fr_rss_samples,
            }
        },
    )
