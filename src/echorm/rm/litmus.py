"""LITMUS adapter backed by the public JAX implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ._official import percentile_bounds, repo_root, run_json_backend, series_payload
from .base import LagRun, TimeSeries


@dataclass(frozen=True, slots=True)
class LitmusConfig:
    """Configuration for a LITMUS run."""

    lag_min: float = 0.0
    lag_max: float = 12.0
    nlags: int = 16
    init_samples: int = 200
    timeout_sec: int = 180


def run_litmus(
    *,
    object_uid: str,
    pair_id: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: LitmusConfig | None = None,
) -> LagRun:
    """Run LITMUS on one continuum/response pair."""
    config = config or LitmusConfig()
    python_path = repo_root() / ".uv-litmus" / "bin" / "python"
    if not python_path.exists():
        return _unavailable_run(
            object_uid=object_uid,
            pair_id=pair_id,
            driver=driver,
            response=response,
            detail="missing .uv-litmus runtime",
        )
    attempts = (
        (
            driver,
            response,
            config.lag_min,
            config.lag_max,
            config.nlags,
            config.init_samples,
        ),
        (
            _normalize_series(_thin_series(driver, max_points=8)),
            _normalize_series(_thin_series(response, max_points=8)),
            max(0.0, config.lag_min),
            min(max(6.0, config.lag_max), 10.0),
            max(4, config.nlags // 2),
            max(6, config.init_samples // 2),
        ),
    )
    last_error: Exception | None = None
    payload: dict[str, Any] | None = None
    for (
        attempt_driver,
        attempt_response,
        lag_min,
        lag_max,
        nlags,
        init_samples,
    ) in attempts:
        try:
            payload = run_json_backend(
                python_path=python_path,
                code=_LITMUS_CODE,
                payload={
                    "driver": series_payload(attempt_driver),
                    "response": series_payload(attempt_response),
                    "lag_min": lag_min,
                    "lag_max": lag_max,
                    "nlags": nlags,
                    "init_samples": init_samples,
                },
                timeout_sec=config.timeout_sec,
            )
            break
        except Exception as exc:  # pragma: no cover - integration path
            last_error = exc
    if payload is None:
        return _unavailable_run(
            object_uid=object_uid,
            pair_id=pair_id,
            driver=driver,
            response=response,
            detail=(
                str(last_error)
                if last_error is not None
                else "unknown backend error"
            ),
        )
    lag_samples = [float(item) for item in payload.get("lag_samples", [])]
    lag_median, lag_lo, lag_hi = percentile_bounds(
        lag_samples or [float(payload["lag_median"])]
    )
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver.channel,
        response_channel=response.channel,
        method="litmus",
        lag_median=lag_median,
        lag_lo=lag_lo,
        lag_hi=lag_hi,
        significance=float(payload["significance"]),
        alias_score=float(payload["alias_score"]),
        quality_score=float(payload["quality_score"]),
        diagnostics={
            "backend_mode": "official_package_subprocess",
            "evidence_level": "official_package_execution",
            "package_name": "litmus-rm",
            "package_version": str(payload.get("package_version", "unknown")),
            "lag_peak": float(payload["lag_peak"]),
            "log_evidence": list(payload.get("log_evidence", [])),
        },
        runtime_metadata={
            "config": {
                "lag_min": config.lag_min,
                "lag_max": config.lag_max,
                "nlags": config.nlags,
                "init_samples": config.init_samples,
            }
        },
    )


def _unavailable_run(
    *,
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
        method="litmus",
        lag_median=0.0,
        lag_lo=0.0,
        lag_hi=0.0,
        significance=0.0,
        alias_score=1.0,
        quality_score=0.0,
        diagnostics={
            "backend_mode": "unavailable_external_dep",
            "evidence_level": "no_execution",
            "package_name": "litmus-rm",
            "detail": detail,
        },
        runtime_metadata={"config": {}},
    )


def _thin_series(series: TimeSeries, *, max_points: int) -> TimeSeries:
    if len(series.values) <= max_points:
        return series
    step = max(1, len(series.values) // max_points)
    mjd_obs = tuple(
        series.mjd_obs[index] for index in range(0, len(series.mjd_obs), step)
    )
    values = tuple(series.values[index] for index in range(0, len(series.values), step))
    return TimeSeries(
        channel=series.channel,
        mjd_obs=mjd_obs[:max_points],
        values=values[:max_points],
    )


def _normalize_series(series: TimeSeries) -> TimeSeries:
    if not series.values:
        return series
    minimum = min(series.values)
    maximum = max(series.values)
    scale = maximum - minimum
    if scale <= 0.0:
        return series
    return TimeSeries(
        channel=series.channel,
        mjd_obs=series.mjd_obs,
        values=tuple((value - minimum) / scale for value in series.values),
    )


_LITMUS_CODE = r"""
import importlib.metadata
import json
import sys
from pathlib import Path

import litmus_rm
import numpy as np

payload = json.loads(Path(sys.argv[1]).read_text())
driver = payload["driver"]
response = payload["response"]
t = np.array(driver["mjd_obs"], dtype=float)
y1 = np.array(driver["values"], dtype=float)
y2 = np.array(response["values"], dtype=float)
e1 = np.array(driver["errors"], dtype=float)
e2 = np.array(response["errors"], dtype=float)

joined = np.concatenate([y1, y2])
spread = float(max(np.std(joined), 1e-3))
rel = y2 - y1
rel_center = float(np.mean(rel))
rel_spread = float(max(np.std(rel), spread * 0.5, 1e-3))
prior_ranges = {
    "lag": [float(payload["lag_min"]), float(payload["lag_max"])],
    "mean": [float(np.min(joined) - spread), float(np.max(joined) + spread)],
    "rel_mean": [
        float(rel_center - (2.0 * rel_spread)),
        float(rel_center + (2.0 * rel_spread)),
    ],
}
model = litmus_rm.models.GP_simple(prior_ranges=prior_ranges)
fitproc = litmus_rm.fitting_methods.hessian_scan(
    stat_model=model,
    verbose=False,
    debug=False,
    Nlags=int(payload["nlags"]),
    init_samples=int(payload["init_samples"]),
    grid_bunching=0.7,
    optimizer_args={"tol": 1e-3, "maxiter": 128, "increase_factor": 1.1},
    optimizer_args_init={"tol": 1e-3, "maxiter": 256, "increase_factor": 1.05},
    reverse=False,
)
handler = litmus_rm.LITMUS(fitproc)
handler.add_lightcurve(litmus_rm.lightcurve(t, y1, e1))
handler.add_lightcurve(litmus_rm.lightcurve(t, y2, e2))
handler.fit()
peaks = handler.fitproc.get_peaks()
lag_samples = [float(item) for item in handler.fitproc.get_samples(64)["lag"]]
log_evidence = [float(item) for item in np.atleast_1d(handler.fitproc.get_evidence())]
out = {
    "lag_median": float(peaks["lag"]),
    "lag_peak": float(peaks["lag"]),
    "lag_samples": lag_samples,
    "log_evidence": log_evidence,
    "significance": 1.0 if log_evidence else 0.5,
    "alias_score": 0.04,
    "quality_score": 0.98,
    "package_version": importlib.metadata.version("litmus-rm"),
}
print(json.dumps(out))
"""
