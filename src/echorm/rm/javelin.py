"""JAVELIN adapter backed by the upstream implementation."""

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
class JavelinConfig:
    """Configuration for a JAVELIN fit."""

    nwalkers: int = 24
    n_burnin: int = 20
    n_chain: int = 24
    timeout_sec: int = 240


def run_javelin(
    *,
    object_uid: str,
    pair_id: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: JavelinConfig | None = None,
) -> LagRun:
    """Run JAVELIN on one continuum/response pair."""
    config = config or JavelinConfig()
    python_path = rm_literal_python()
    if not python_path.exists():
        return _unavailable_run(
            object_uid=object_uid,
            pair_id=pair_id,
            driver=driver,
            response=response,
            detail="missing rm-literal runtime for JAVELIN",
        )
    try:
        payload = run_json_backend(
            python_path=python_path,
            code=_JAVELIN_CODE,
            payload={
                "driver": series_payload(driver),
                "response": series_payload(response),
                "nwalkers": config.nwalkers,
                "n_burnin": config.n_burnin,
                "n_chain": config.n_chain,
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
        method="javelin",
        lag_median=lag_median,
        lag_lo=lag_lo,
        lag_hi=lag_hi,
        significance=float(payload["significance"]),
        alias_score=float(payload["alias_score"]),
        quality_score=float(payload["quality_score"]),
        diagnostics={
            "backend_mode": "official_package_subprocess",
            "evidence_level": "official_package_execution",
            "package_name": "javelin",
            "package_version": str(payload.get("package_version", "unknown")),
            "lag_hpd": list(payload.get("lag_hpd", [])),
            "continuum_hpd": list(payload.get("continuum_hpd", [])),
        },
        runtime_metadata={
            "config": {
                "nwalkers": config.nwalkers,
                "n_burnin": config.n_burnin,
                "n_chain": config.n_chain,
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
        method="javelin",
        lag_median=0.0,
        lag_lo=0.0,
        lag_hi=0.0,
        significance=0.0,
        alias_score=1.0,
        quality_score=0.0,
        diagnostics={
            "backend_mode": "unavailable_external_dep",
            "evidence_level": "no_execution",
            "package_name": "javelin",
            "detail": detail,
        },
        runtime_metadata={"config": {}},
    )


_JAVELIN_CODE = r"""
import importlib.metadata
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
from javelin.lcmodel import Cont_Model, Rmap_Model
from javelin.zylc import get_data

payload = json.loads(Path(sys.argv[1]).read_text())
driver = payload["driver"]
response = payload["response"]
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
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
with tempfile.TemporaryDirectory() as tmpdir:
    tmp = Path(tmpdir)
    driver_path = tmp / "driver.dat"
    response_path = tmp / "response.dat"
    np.savetxt(driver_path, driver_rows)
    np.savetxt(response_path, response_rows)

    cont_data = get_data([str(driver_path)], names=["continuum"])
    cont = Cont_Model(cont_data)
    cont.do_mcmc(
        nwalkers=int(payload["nwalkers"]),
        nburn=int(payload["n_burnin"]),
        nchain=int(payload["n_chain"]),
        fburn=None,
        fchain=None,
        threads=1,
        set_verbose=False,
    )
    conthpd = np.array(cont.hpd, dtype=float)

    lag_data = get_data(
        [str(driver_path), str(response_path)],
        names=["continuum", response["channel"]],
    )
    rmap = Rmap_Model(lag_data)
    baseline = float(max(driver["mjd_obs"]) - min(driver["mjd_obs"]))
    rmap.do_mcmc(
        conthpd=conthpd,
        lagtobaseline=0.5,
        laglimit=[[0.0, max(1.0, baseline)]],
        nwalkers=int(payload["nwalkers"]),
        nburn=int(payload["n_burnin"]),
        nchain=int(payload["n_chain"]),
        fburn=None,
        fchain=None,
        threads=1,
        set_verbose=False,
    )
    lag_samples = np.array(rmap.flatchain, dtype=float)[:, 2]
    lag_hpd = np.array(rmap.hpd, dtype=float)[:, 2]
    lag_width = float(lag_hpd[2] - lag_hpd[0])
    quality_score = max(0.0, min(1.0, 1.0 - (lag_width / max(baseline, 1.0))))
    out = {
        "lag_median": float(lag_hpd[1]),
        "lag_samples": lag_samples.tolist(),
        "lag_hpd": lag_hpd.tolist(),
        "continuum_hpd": conthpd.tolist(),
        "significance": 1.0 if lag_samples.size >= int(payload["nwalkers"]) else 0.5,
        "alias_score": round(min(1.0, lag_width / max(baseline, 1.0)), 3),
        "quality_score": round(quality_score, 3),
        "package_version": importlib.metadata.version("javelin"),
    }
    print(json.dumps(out))
"""
