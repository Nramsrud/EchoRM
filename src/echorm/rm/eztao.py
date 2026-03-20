"""EzTao-backed lag adapter."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .base import LagRun, TimeSeries

try:
    from eztao.ts.carma_fit import drw_fit  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - import availability depends on runtime
    drw_fit = None


@dataclass(frozen=True, slots=True)
class EztaoConfig:
    """Configuration for an EzTao run."""

    lag_grid_size: int = 48


def run_eztao(
    *,
    object_uid: str,
    pair_id: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: EztaoConfig | None = None,
) -> LagRun:
    """Run a DRW-assisted lag estimate with EzTao."""
    config = config or EztaoConfig()
    if drw_fit is None:
        return _unavailable_run(object_uid, pair_id, driver, response, "EzTao missing")
    try:
        driver_tau, driver_amp = _fit_drw(driver)
        response_tau, response_amp = _fit_drw(response)
        lag_grid = np.linspace(
            0.0,
            max(float(response.mjd_obs[-1] - response.mjd_obs[0]), 1.0),
            config.lag_grid_size,
        )
        scores = [
            _lag_score(driver, response, lag, driver_tau, response_tau)
            for lag in lag_grid
        ]
        best_index = int(np.argmax(scores))
        lag_median = float(lag_grid[best_index])
        lo = float(max(0.0, lag_median - (lag_grid[1] - lag_grid[0])))
        hi = float(lag_median + (lag_grid[1] - lag_grid[0]))
        quality = float(
            max(0.0, min(1.0, 0.7 + (0.1 / max(driver_amp + response_amp, 1e-6))))
        )
        return LagRun(
            object_uid=object_uid,
            pair_id=pair_id,
            driver_channel=driver.channel,
            response_channel=response.channel,
            method="eztao",
            lag_median=lag_median,
            lag_lo=lo,
            lag_hi=hi,
            significance=float(max(scores)),
            alias_score=float(1.0 / max(best_index + 1, 1)),
            quality_score=quality,
            diagnostics={
                "backend_mode": "official_package_native",
                "evidence_level": "official_package_execution",
                "process_family": "drw",
                "driver_logamp": driver_amp,
                "driver_logtau": driver_tau,
                "response_logamp": response_amp,
                "response_logtau": response_tau,
            },
            runtime_metadata={
                "config": {
                    "lag_grid_size": config.lag_grid_size,
                }
            },
        )
    except Exception as exc:  # pragma: no cover - integration path
        return _unavailable_run(object_uid, pair_id, driver, response, str(exc))


def _fit_drw(series: TimeSeries) -> tuple[float, float]:
    t = np.array(series.mjd_obs, dtype=float)
    y = np.array(series.values, dtype=float)
    yerr = np.full_like(y, max(np.std(y) * 0.05, 1e-6))
    result = drw_fit(t, y, yerr, n_opt=4)
    params = np.array(result, dtype=float)
    return (float(params[1]), float(params[0]))


def _lag_score(
    driver: TimeSeries,
    response: TimeSeries,
    lag: float,
    driver_tau: float,
    response_tau: float,
) -> float:
    t = np.array(driver.mjd_obs, dtype=float)
    x = np.array(driver.values, dtype=float)
    y = np.array(response.values, dtype=float)
    shifted = np.interp(t - lag, t, y, left=y[0], right=y[-1])
    corr = np.corrcoef(x, shifted)[0, 1]
    scale_penalty = 1.0 / (1.0 + abs(driver_tau - response_tau))
    return float(np.nan_to_num(corr, nan=0.0) * scale_penalty)


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
        method="eztao",
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
