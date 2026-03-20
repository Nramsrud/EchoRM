from __future__ import annotations

from echorm.rm.base import TimeSeries
from echorm.rm.javelin import JavelinConfig, run_javelin
from echorm.rm.pyroa import PyroaConfig, run_pyroa
from echorm.rm.serialize import serialize_lag_run
from echorm.schemas import LAG_RESULT_SCHEMA


def _driver() -> TimeSeries:
    return TimeSeries(
        channel="continuum",
        mjd_obs=(0.0, 1.0, 2.0, 3.0, 4.0, 5.0),
        values=(1.0, 1.1, 0.9, 1.2, 1.15, 1.05),
    )


def _response() -> TimeSeries:
    return TimeSeries(
        channel="hbeta",
        mjd_obs=(0.0, 1.0, 2.0, 3.0, 4.0, 5.0),
        values=(0.8, 0.82, 0.79, 0.88, 0.86, 0.83),
    )


def test_javelin_adapter_reports_execution_evidence_or_unavailability() -> None:
    run = run_javelin(
        object_uid="ngc5548",
        pair_id="continuum->hbeta",
        driver=_driver(),
        response=_response(),
        config=JavelinConfig(nwalkers=12, n_burnin=10, n_chain=12, timeout_sec=60),
    )
    serialized = serialize_lag_run(run)

    assert LAG_RESULT_SCHEMA.validate_record(serialized.record) == ()
    assert serialized.record["method"] == "javelin"
    assert serialized.diagnostics["backend_mode"] in {
        "official_package_subprocess",
        "unavailable_external_dep",
    }


def test_pyroa_adapter_reports_execution_evidence_or_unavailability() -> None:
    run = run_pyroa(
        object_uid="ngc5548",
        pair_id="continuum->hbeta",
        driver=_driver(),
        response=_response(),
        config=PyroaConfig(n_samples=20, n_burnin=10, init_tau=1.0, timeout_sec=30),
    )
    serialized = serialize_lag_run(run)

    assert LAG_RESULT_SCHEMA.validate_record(serialized.record) == ()
    assert serialized.record["method"] == "pyroa"
    assert serialized.diagnostics["backend_mode"] in {
        "official_package_subprocess",
        "unavailable_external_dep",
    }
