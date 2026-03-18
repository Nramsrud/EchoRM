from __future__ import annotations

from echorm.rm.base import TimeSeries
from echorm.rm.consensus import build_consensus
from echorm.rm.javelin import run_javelin
from echorm.rm.nulls import NullDiagnostic, evaluate_null_controls
from echorm.rm.posteriors import ConvergenceDiagnostics, build_posterior_summary
from echorm.rm.pyccf import run_pyccf
from echorm.rm.pyzdcf import run_pyzdcf
from echorm.rm.serialize import serialize_lag_run


def test_consensus_identifies_agreement_cluster() -> None:
    driver = TimeSeries("continuum", (1, 2, 3, 4, 5), (0.1, 1.0, 0.2, 1.1, 0.3))
    response = TimeSeries("hbeta", (1, 2, 3, 4, 5), (0.0, 0.0, 0.1, 1.0, 0.2))
    pyccf = serialize_lag_run(
        run_pyccf(object_uid="ngc5548", driver=driver, response=response)
    )
    pyzdcf = serialize_lag_run(
        run_pyzdcf(object_uid="ngc5548", driver=driver, response=response)
    )
    javelin = serialize_lag_run(
        run_javelin(
            object_uid="ngc5548",
            pair_id="continuum->hbeta",
            driver_channel="continuum",
            response_channel="hbeta",
            posterior=build_posterior_summary(
                samples=(1.8, 2.0, 2.1, 2.2, 2.4),
                posterior_path="artifacts/posteriors/javelin.nc",
            ),
            diagnostics=ConvergenceDiagnostics(
                r_hat=1.01,
                effective_sample_size=1000,
                passed=True,
            ),
        )
    )
    consensus = build_consensus(
        (pyccf, pyzdcf, javelin),
        null_diagnostic=NullDiagnostic(false_positive_rate=0.0, null_pair_count=3),
    )

    assert consensus.classification == "agreement_cluster"
    assert consensus.agreement_score >= 0.75


def test_consensus_identifies_contested_and_spurious_cases() -> None:
    low_significance = (
        serialize_lag_run(
            run_javelin(
                object_uid="ngc5548",
                pair_id="continuum->hbeta",
                driver_channel="continuum",
                response_channel="hbeta",
                posterior=build_posterior_summary(
                    samples=(1.0, 1.2, 1.4, 1.6, 1.8),
                    posterior_path="artifacts/posteriors/javelin-null.nc",
                ),
                diagnostics=ConvergenceDiagnostics(
                    r_hat=1.4,
                    effective_sample_size=50,
                    passed=False,
                ),
            )
        ),
        serialize_lag_run(
            run_javelin(
                object_uid="ngc5548",
                pair_id="continuum->hbeta",
                driver_channel="continuum",
                response_channel="hbeta",
                posterior=build_posterior_summary(
                    samples=(4.0, 4.2, 4.5, 4.8, 5.0),
                    posterior_path="artifacts/posteriors/javelin-alt.nc",
                ),
                diagnostics=ConvergenceDiagnostics(
                    r_hat=1.3,
                    effective_sample_size=60,
                    passed=False,
                ),
            )
        ),
    )
    nulls = evaluate_null_controls(low_significance)
    spurious = build_consensus(low_significance, null_diagnostic=nulls)

    assert spurious.classification == "likely_spurious"
    assert spurious.null_false_positive_rate >= 0.5


def test_consensus_identifies_candidate_anomaly() -> None:
    results = (
        serialize_lag_run(
            run_javelin(
                object_uid="ngc5548",
                pair_id="continuum->hbeta",
                driver_channel="continuum",
                response_channel="hbeta",
                posterior=build_posterior_summary(
                    samples=(1.0, 1.1, 1.2, 1.3, 1.4),
                    posterior_path="artifacts/posteriors/a.nc",
                ),
                diagnostics=ConvergenceDiagnostics(
                    r_hat=1.01,
                    effective_sample_size=1000,
                    passed=True,
                ),
            )
        ),
        serialize_lag_run(
            run_javelin(
                object_uid="ngc5548",
                pair_id="continuum->hbeta",
                driver_channel="continuum",
                response_channel="hbeta",
                posterior=build_posterior_summary(
                    samples=(6.0, 6.2, 6.3, 6.4, 6.5),
                    posterior_path="artifacts/posteriors/b.nc",
                ),
                diagnostics=ConvergenceDiagnostics(
                    r_hat=1.01,
                    effective_sample_size=1000,
                    passed=True,
                ),
            )
        ),
    )
    anomaly = build_consensus(
        results,
        null_diagnostic=NullDiagnostic(false_positive_rate=0.0, null_pair_count=2),
    )

    assert anomaly.classification == "candidate_anomaly"
