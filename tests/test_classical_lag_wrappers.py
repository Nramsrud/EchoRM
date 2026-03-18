from __future__ import annotations

from echorm.rm.base import TimeSeries
from echorm.rm.pyccf import PyccfConfig, run_pyccf
from echorm.rm.pyzdcf import PyzdcfConfig, run_pyzdcf
from echorm.rm.serialize import serialize_lag_run
from echorm.schemas import LAG_RESULT_SCHEMA


def test_pyccf_adapter_emits_canonical_lag_record() -> None:
    driver = TimeSeries(
        channel="continuum",
        mjd_obs=(1.0, 2.0, 3.0, 4.0, 5.0),
        values=(0.1, 1.0, 0.2, 1.1, 0.3),
    )
    response = TimeSeries(
        channel="hbeta",
        mjd_obs=(1.0, 2.0, 3.0, 4.0, 5.0),
        values=(0.0, 0.0, 0.1, 1.0, 0.2),
    )
    run = run_pyccf(
        object_uid="ngc5548",
        driver=driver,
        response=response,
        config=PyccfConfig(max_lag=3, fr_rss_samples=4),
    )
    serialized = serialize_lag_run(run)

    assert LAG_RESULT_SCHEMA.validate_record(serialized.record) == ()
    assert serialized.record["lag_median"] == 2.0
    assert "fr_rss_distribution" in serialized.diagnostics


def test_pyzdcf_adapter_preserves_sparse_sampling_diagnostics() -> None:
    driver = TimeSeries(
        channel="continuum",
        mjd_obs=(1.0, 2.5, 4.0, 7.0, 9.0),
        values=(0.2, 0.9, 0.1, 1.0, 0.2),
    )
    response = TimeSeries(
        channel="hbeta",
        mjd_obs=(1.0, 2.5, 4.0, 7.0, 9.0),
        values=(0.0, 0.2, 0.9, 0.1, 1.0),
    )
    run = run_pyzdcf(
        object_uid="ngc5548",
        driver=driver,
        response=response,
        config=PyzdcfConfig(max_lag=3, min_pairs=2),
    )
    serialized = serialize_lag_run(run)

    assert serialized.record["lag_median"] == 1.0
    assert serialized.diagnostics["sparse_sampling_pairs"] == 4
    config_text = str(serialized.runtime_metadata["config"])
    assert "max_lag" in config_text
    assert "min_pairs" in config_text
