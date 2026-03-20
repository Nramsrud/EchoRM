"""MICA2 adapter backed by the upstream implementation."""

from __future__ import annotations

from dataclasses import dataclass

from ._official import (
    percentile_bounds,
    rm_literal_python,
    run_json_backend,
    series_payload,
)
from .base import LagRun, TimeSeries


@dataclass(frozen=True, slots=True)
class Mica2Config:
    """Configuration for a MICA2 run."""

    transfer_family: str = "gaussian"
    component_count: int = 1
    max_num_saves: int = 20
    timeout_sec: int = 300


def run_mica2(
    *,
    object_uid: str,
    pair_id: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: Mica2Config | None = None,
) -> LagRun:
    """Run MICA2 on one continuum/response pair."""
    config = config or Mica2Config()
    python_path = rm_literal_python()
    if not python_path.exists():
        return _unavailable_run(
            object_uid=object_uid,
            pair_id=pair_id,
            driver=driver,
            response=response,
            detail="missing rm-literal runtime for MICA2",
            config=config,
        )
    try:
        payload = run_json_backend(
            python_path=python_path,
            code=_MICA2_CODE,
            payload={
                "driver": series_payload(driver),
                "response": series_payload(response),
                "transfer_family": config.transfer_family,
                "component_count": config.component_count,
                "max_num_saves": config.max_num_saves,
            },
            timeout_sec=config.timeout_sec,
        )
    except Exception as exc:  # pragma: no cover - integration path
        return _unavailable_run(
            object_uid=object_uid,
            pair_id=pair_id,
            driver=driver,
            response=response,
            detail=str(exc),
            config=config,
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
        method="mica2",
        lag_median=lag_median,
        lag_lo=lag_lo,
        lag_hi=lag_hi,
        significance=float(payload["significance"]),
        alias_score=float(payload["alias_score"]),
        quality_score=float(payload["quality_score"]),
        diagnostics={
            "backend_mode": "official_package_subprocess",
            "evidence_level": "official_package_execution",
            "package_name": "pymica",
            "package_version": str(payload.get("package_version", "unknown")),
            "sample_count": int(payload.get("sample_count", 0)),
            "transfer_family": config.transfer_family,
            "component_count": config.component_count,
        },
        runtime_metadata={
            "config": {
                "transfer_family": config.transfer_family,
                "component_count": config.component_count,
                "max_num_saves": config.max_num_saves,
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
    config: Mica2Config,
) -> LagRun:
    return LagRun(
        object_uid=object_uid,
        pair_id=pair_id,
        driver_channel=driver.channel,
        response_channel=response.channel,
        method="mica2",
        lag_median=0.0,
        lag_lo=0.0,
        lag_hi=0.0,
        significance=0.0,
        alias_score=1.0,
        quality_score=0.0,
        diagnostics={
            "backend_mode": "unavailable_external_dep",
            "evidence_level": "no_execution",
            "package_name": "pymica",
            "detail": detail,
            "transfer_family": config.transfer_family,
            "component_count": config.component_count,
        },
        runtime_metadata={
            "config": {
                "transfer_family": config.transfer_family,
                "component_count": config.component_count,
                "max_num_saves": config.max_num_saves,
            }
        },
    )


_MICA2_CODE = r"""
import importlib.metadata
import json
import os
import sys
from pathlib import Path

import numpy as np
import pymica
from mpi4py import MPI

payload = json.loads(Path(sys.argv[1]).read_text())
driver = payload["driver"]
response = payload["response"]
root = Path(sys.argv[1]).resolve().parent
os.chdir(root)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
driver_rows = np.column_stack(
    [
        np.array(driver["mjd_obs"], dtype=float),
        np.array(driver["values"], dtype=float),
        np.array(driver["errors"], dtype=float),
    ]
)
response_rows = np.column_stack(
    [
        np.array(response["mjd_obs"], dtype=float),
        np.array(response["values"], dtype=float),
        np.array(response["errors"], dtype=float),
    ]
)
data = {"set1": [driver_rows, response_rows]}
model = pymica.gmodel()
baseline = float(max(driver["mjd_obs"]) - min(driver["mjd_obs"]))
model.setup(
    data=data,
    type_tf=str(payload["transfer_family"]),
    lag_limit=[0.0, max(1.0, baseline)],
    number_component=[1, int(payload["component_count"])],
    max_num_saves=int(payload["max_num_saves"]),
)
model.run()
if rank == 0:
    timelag = model.get_posterior_sample_timelag(set=0, line=0)
    component_index = max(0, int(payload["component_count"]) - 1)
    lag_array = np.array(timelag[component_index], dtype=float)
    lag_samples = lag_array.reshape(-1).astype(float)
    lag_median = float(np.median(lag_samples))
    lag_lo = float(np.percentile(lag_samples, 16))
    lag_hi = float(np.percentile(lag_samples, 84))
    lag_width = float(max(0.0, lag_hi - lag_lo))
    quality_score = max(0.0, min(1.0, 1.0 - (lag_width / max(baseline, 1.0))))
    out = {
        "lag_median": lag_median,
        "lag_samples": lag_samples.tolist(),
        "lag_lo": lag_lo,
        "lag_hi": lag_hi,
        "significance": 1.0 if lag_samples.size > 0 else 0.0,
        "alias_score": round(min(1.0, lag_width / max(baseline, 1.0)), 3),
        "quality_score": round(quality_score, 3),
        "sample_count": int(lag_samples.size),
        "package_version": importlib.metadata.version("pymica"),
    }
    print(json.dumps(out))
"""
