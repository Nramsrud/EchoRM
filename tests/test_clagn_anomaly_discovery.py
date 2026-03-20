from __future__ import annotations

from echorm.anomaly.candidates import build_candidate
from echorm.anomaly.clagn import analyze_clagn_transition
from echorm.anomaly.rank import rank_anomaly
from echorm.reports.candidate_memos import build_candidate_memo


def test_holdout_guard_blocks_non_holdout_inputs() -> None:
    try:
        rank_anomaly(
            object_uid="ztf-target-001",
            lag_outlier=0.9,
            line_response_outlier=0.8,
            sonification_outlier=0.7,
            is_holdout=False,
        )
    except ValueError as error:
        assert "hold-out" in str(error)
    else:
        raise AssertionError("expected hold-out guard to fail")


def test_anomaly_scores_remain_traceable_to_explicit_components() -> None:
    score = rank_anomaly(
        object_uid="ztf-target-001",
        lag_outlier=0.9,
        line_response_outlier=0.8,
        sonification_outlier=0.7,
        is_holdout=True,
    )
    assert score.total_score == 0.8
    assert score.components["lag_outlier"] == 0.9


def test_candidate_outputs_include_rank_category_and_evidence() -> None:
    score = rank_anomaly(
        object_uid="ztf-target-001",
        lag_outlier=0.9,
        line_response_outlier=0.8,
        sonification_outlier=0.7,
        is_holdout=True,
    )
    transition = analyze_clagn_transition(
        object_uid="ztf-target-001",
        pre_state_lag=1.0,
        post_state_lag=2.5,
        pre_line_flux=10.0,
        post_line_flux=4.0,
    )
    candidate = build_candidate(score=score, transition=transition)
    memo = build_candidate_memo(candidate)

    assert candidate.anomaly_category == "clagn_transition"
    assert "score_components" in candidate.evidence_bundle
    assert "Category: clagn_transition" in memo
    assert candidate.review_priority == "medium"


def test_candidate_records_preserve_method_support_and_transition_metadata() -> None:
    score = rank_anomaly(
        object_uid="ztf-target-002",
        lag_outlier=0.85,
        line_response_outlier=0.75,
        sonification_outlier=0.7,
        is_holdout=True,
        evidence_level="real_fixture",
        method_support_count=3,
        review_priority="high",
    )
    transition = analyze_clagn_transition(
        object_uid="ztf-target-002",
        pre_state_lag=1.2,
        post_state_lag=2.7,
        pre_line_flux=8.0,
        post_line_flux=4.5,
        evidence_level="real_fixture",
    )
    candidate = build_candidate(
        score=score,
        transition=transition,
        canonical_name="ZTF Target 002",
        benchmark_links=("gold_validation",),
        limitations=("fixture-backed hold-out evidence",),
    )
    payload = candidate.to_dict()
    evidence_bundle = payload["evidence_bundle"]
    assert isinstance(evidence_bundle, dict)
    benchmark_links = evidence_bundle["benchmark_links"]
    assert isinstance(benchmark_links, list)

    assert payload["method_support_count"] == 3
    assert payload["review_priority"] == "high"
    assert "gold_validation" in benchmark_links
