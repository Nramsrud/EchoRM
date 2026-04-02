"""celerite2-backed lag adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .base import LagRun, TimeSeries

try:
    from celerite2 import GaussianProcess, terms
except ImportError:  # pragma: no cover - runtime dependent
    GaussianProcess = None
    terms = None


@dataclass(frozen=True, slots=True)
class Celerite2Config:
    """Configuration for a celerite2 run."""

    lag_grid_size: int = 64


def run_celerite2(
    *,
    object_uid: str,
    pair_id: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: Celerite2Config | None = None,
) -> LagRun:
    """Run a celerite2-smoothed lag estimate."""
    config = config or Celerite2Config()
    if GaussianProcess is None or terms is None:
        return _unavailable_run(
            object_uid,
            pair_id,
            driver,
            response,
            "celerite2 missing",
        )
    try:
        dense_t, driver_mu = _predict_dense(driver)
        _, response_mu = _predict_dense(response)
        lag_grid = np.linspace(
            0.0,
            max(float(driver.mjd_obs[-1] - driver.mjd_obs[0]), 1.0),
            config.lag_grid_size,
        )
        scores = []
        for lag in lag_grid:
            shifted = np.interp(
                dense_t,
                dense_t - lag,
                response_mu,
                left=response_mu[0],
                right=response_mu[-1],
            )
            corr = float(np.nan_to_num(np.corrcoef(driver_mu, shifted)[0, 1], nan=0.0))
            scores.append(corr)
        best_index = int(np.argmax(scores))
        lag_median = float(lag_grid[best_index])
        step = float(lag_grid[1] - lag_grid[0]) if len(lag_grid) > 1 else 0.5
        return LagRun(
            object_uid=object_uid,
            pair_id=pair_id,
            driver_channel=driver.channel,
            response_channel=response.channel,
            method="celerite2",
            lag_median=lag_median,
            lag_lo=max(0.0, lag_median - step),
            lag_hi=lag_median + step,
            significance=float(scores[best_index]),
            alias_score=float(1.0 / max(best_index + 1, 1)),
            quality_score=float(max(0.0, min(1.0, 0.9 + (scores[best_index] * 0.05)))),
            diagnostics={
                "backend_mode": "official_package_native",
                "evidence_level": "official_package_execution",
                "kernel_family": "real_term",
                "dense_grid_size": len(dense_t),
            },
            runtime_metadata={
                "config": {
                    "lag_grid_size": config.lag_grid_size,
                }
            },
        )
    except Exception as exc:  # pragma: no cover - integration path
        return _unavailable_run(object_uid, pair_id, driver, response, str(exc))


def _predict_dense(series: TimeSeries) -> tuple[Any, Any]:
    t = np.array(series.mjd_obs, dtype=float)
    y = np.array(series.values, dtype=float)
    yerr = np.full_like(y, max(np.std(y) * 0.05, 1e-6))
    amplitude = max(float(np.var(y)), 1e-6)
    width = 1.0 / max(float(np.ptp(t)), 1.0)
    kernel = terms.RealTerm(a=amplitude, c=width)
    gp = GaussianProcess(kernel, mean=float(np.mean(y)))
    gp.compute(t, yerr=yerr)
    dense_t = np.linspace(float(t[0]), float(t[-1]), max(len(t) * 4, 32))
    mu = gp.predict(y, t=dense_t, return_cov=False)
    return dense_t, np.array(mu, dtype=float)


def _unavailable_run(
    object_uid: str,
    pair_id: str,
    driver: TimeSeries,
    response: TimeSeries,
    detail: str,
) -> LagRun:
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver.channel,
        response_channel=response.channel,
        method="celerite2",
        lag_median=0.0,
        lag_lo=0.0,
        lag_hi=0.0,
        significance=0.0,
        alias_score=1.0,
        quality_score=0.0,
        diagnostics={
            "backend_mode": "unavailable_external_dep",
            "evidence_level": "no_execution",
            "detail": detail,
        },
        runtime_metadata={"config": {}},
    )
