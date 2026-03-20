from __future__ import annotations

from echorm.rm.base import LagRun
from echorm.rm.consensus import build_consensus
from echorm.rm.nulls import NullDiagnostic, evaluate_null_controls
from echorm.rm.serialize import serialize_lag_run


def _lag_run(
    method: str,
    lag_median: float,
    *,
    significance: float = 0.9,
    alias_score: float = 0.1,
    quality_score: float = 0.9,
) -> LagRun:
    return LagRun(
        object_uid="ngc5548",
        pair_id="continuum->hbeta",
        driver_channel="continuum",
        response_channel="hbeta",
        method=method,
        lag_median=lag_median,
        lag_lo=lag_median - 0.5,
        lag_hi=lag_median + 0.5,
        significance=significance,
        alias_score=alias_score,
        quality_score=quality_score,
        diagnostics={},
        runtime_metadata={"config": {"method": method}},
    )


def test_consensus_identifies_agreement_cluster() -> None:
    pyccf = serialize_lag_run(_lag_run("pyccf", 2.0))
    pyzdcf = serialize_lag_run(_lag_run("pyzdcf", 2.1))
    javelin = serialize_lag_run(_lag_run("javelin", 1.9))
    consensus = build_consensus(
        (pyccf, pyzdcf, javelin),
        null_diagnostic=NullDiagnostic(false_positive_rate=0.0, null_pair_count=3),
    )

    assert consensus.classification == "agreement_cluster"
    assert consensus.agreement_score >= 0.75


def test_consensus_identifies_contested_and_spurious_cases() -> None:
    low_significance = (
        serialize_lag_run(
            _lag_run("javelin", 1.2, significance=0.2, quality_score=0.4)
        ),
        serialize_lag_run(
            _lag_run("pyroa", 4.8, significance=0.1, quality_score=0.4)
        ),
    )
    nulls = evaluate_null_controls(low_significance)
    spurious = build_consensus(low_significance, null_diagnostic=nulls)

    assert spurious.classification == "likely_spurious"
    assert spurious.null_false_positive_rate >= 0.5


def test_consensus_identifies_candidate_anomaly() -> None:
    results = (
        serialize_lag_run(_lag_run("javelin", 1.0, quality_score=0.95)),
        serialize_lag_run(_lag_run("pyroa", 6.4, quality_score=0.95)),
    )
    anomaly = build_consensus(
        results,
        null_diagnostic=NullDiagnostic(false_positive_rate=0.0, null_pair_count=2),
    )

    assert anomaly.classification == "candidate_anomaly"
