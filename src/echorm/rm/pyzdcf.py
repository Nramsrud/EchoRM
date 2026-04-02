"""pyZDCF adapter backed by the upstream package."""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .base import LagRun, TimeSeries, build_pair_id

try:
    from pyzdcf import pyzdcf
except ImportError:  # pragma: no cover - runtime dependent
    pyzdcf = None


@dataclass(frozen=True, slots=True)
class PyzdcfConfig:
    """Configuration for the pyZDCF adapter."""

    num_mc: int = 50


def run_pyzdcf(
    *,
    object_uid: str,
    driver: TimeSeries,
    response: TimeSeries,
    config: PyzdcfConfig | None = None,
) -> LagRun:
    """Run pyZDCF on one continuum/response pair."""
    config = config or PyzdcfConfig()
    if pyzdcf is None:
        return _unavailable_run(object_uid, driver, response, "pyzdcf missing")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            input_dir = root / "input"
            output_dir = root / "output"
            input_dir.mkdir(parents=True, exist_ok=True)
            output_dir.mkdir(parents=True, exist_ok=True)
            lc1_name = "continuum.csv"
            lc2_name = f"{response.channel}.csv"
            _write_series(input_dir / lc1_name, driver)
            _write_series(input_dir / lc2_name, response)
            dcf = pyzdcf(
                str(input_dir) + "/",
                str(output_dir) + "/",
                intr=False,
                sep=",",
                verbose=False,
                parameters={
                    "autocf": False,
                    "prefix": "ccf",
                    "uniform_sampling": False,
                    "omit_zero_lags": True,
                    "minpts": 0,
                    "num_MC": config.num_mc,
                    "lc1_name": lc1_name,
                    "lc2_name": lc2_name,
                },
            )
            best_row = dcf.iloc[dcf["dcf"].astype(float).idxmax()]
            lag_median = float(best_row["tau"])
            lag_lo = float(lag_median - abs(float(best_row["-sig(tau)"])))
            lag_hi = float(lag_median + abs(float(best_row["+sig(tau)"])))
            significance = float(best_row["dcf"])
            return LagRun(
                object_uid=object_uid,
                pair_id=build_pair_id(driver, response),
                driver_channel=driver.channel,
                response_channel=response.channel,
                method="pyzdcf",
                lag_median=lag_median,
                lag_lo=lag_lo,
                lag_hi=lag_hi,
                significance=significance,
                alias_score=float(1.0 / max(int(best_row["#bin"]), 1)),
                quality_score=0.88,
                diagnostics={
                    "backend_mode": "official_package_native",
                    "evidence_level": "official_package_execution",
                    "sparse_sampling_pairs": int(best_row["#bin"]),
                    "zdcf_bins": int(len(dcf)),
                    "num_mc": config.num_mc,
                },
                runtime_metadata={"config": {"num_mc": config.num_mc}},
            )
    except Exception as exc:  # pragma: no cover - integration path
        return _unavailable_run(object_uid, driver, response, str(exc))


def _write_series(path: Path, series: TimeSeries) -> None:
    y = np.array(series.values, dtype=float)
    yerr = np.full_like(y, max(np.std(y) * 0.05, 1e-6))
    payload = np.column_stack([np.array(series.mjd_obs, dtype=float), y, yerr])
    np.savetxt(path, payload, delimiter=",")


def _unavailable_run(
    object_uid: str,
    driver: TimeSeries,
    response: TimeSeries,
    detail: str,
) -> LagRun:
    return LagRun(
        object_uid=object_uid,
        pair_id=build_pair_id(driver, response),
        driver_channel=driver.channel,
        response_channel=response.channel,
        method="pyzdcf",
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
