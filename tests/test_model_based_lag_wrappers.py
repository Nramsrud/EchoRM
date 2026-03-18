from __future__ import annotations

from echorm.rm.javelin import JavelinConfig, run_javelin
from echorm.rm.posteriors import (
    ConvergenceDiagnostics,
    build_posterior_summary,
)
from echorm.rm.pyroa import PyroaConfig, run_pyroa
from echorm.rm.serialize import serialize_lag_run
from echorm.schemas import LAG_RESULT_SCHEMA


def test_javelin_adapter_preserves_posterior_and_config_metadata() -> None:
    posterior = build_posterior_summary(
        samples=(1.8, 2.0, 2.1, 2.2, 2.4),
        posterior_path="artifacts/posteriors/javelin-ngc5548.nc",
    )
    diagnostics = ConvergenceDiagnostics(
        r_hat=1.01,
        effective_sample_size=1200,
        passed=True,
    )
    run = run_javelin(
        object_uid="ngc5548",
        pair_id="continuum->hbeta",
        driver_channel="continuum",
        response_channel="hbeta",
        posterior=posterior,
        diagnostics=diagnostics,
        config=JavelinConfig(chain_length=4000, burn_in=1000),
    )
    serialized = serialize_lag_run(run)

    assert LAG_RESULT_SCHEMA.validate_record(serialized.record) == ()
    assert serialized.record["posterior_path"] == posterior.posterior_path
    assert serialized.record["method_config_hash"] == "burn_in=1000|chain_length=4000"


def test_pyroa_adapter_preserves_latent_driver_context() -> None:
    posterior = build_posterior_summary(
        samples=(0.8, 0.9, 1.0, 1.2, 1.3),
        posterior_path="artifacts/posteriors/pyroa-ngc5548.nc",
        latent_driver="continuum+uv",
    )
    diagnostics = ConvergenceDiagnostics(
        r_hat=1.02,
        effective_sample_size=900,
        passed=True,
    )
    run = run_pyroa(
        object_uid="ngc5548",
        pair_id="continuum->hbeta",
        driver_channel="continuum",
        response_channel="hbeta",
        posterior=posterior,
        diagnostics=diagnostics,
        config=PyroaConfig(chain_length=5000, walkers=64),
    )
    serialized = serialize_lag_run(run)

    assert serialized.record["lag_median"] == posterior.median
    assert serialized.diagnostics["latent_driver"] == "continuum+uv"
    assert serialized.diagnostics["multi_light_curve_context"] is True
