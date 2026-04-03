from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from echorm.eval.benchmark_corpus import DiscoveryHoldoutRecord
from echorm.eval.discovery_snapshot import materialize_discovery_snapshot_package
from echorm.eval.primary_wave_rerun import materialize_primary_wave_rerun_package
from echorm.eval.readiness import _write_json
from echorm.eval.root_closeout import materialize_discovery_candidate_bundle

ROOT = Path(__file__).resolve().parent.parent


def _write_lightcurve(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=("mjd", "mag", "magerr", "filtercode")
        )
        writer.writeheader()
        writer.writerows(
            [
                {"mjd": 1.0, "mag": 20.1, "magerr": 0.1, "filtercode": "ztfg"},
                {"mjd": 2.0, "mag": 20.3, "magerr": 0.1, "filtercode": "ztfr"},
                {"mjd": 5.0, "mag": 19.4, "magerr": 0.1, "filtercode": "ztfg"},
                {"mjd": 6.0, "mag": 19.2, "magerr": 0.1, "filtercode": "ztfr"},
            ]
        )


def _build_record(
    tmp_path: Path,
    *,
    object_uid: str,
    canonical_name: str,
    raw_lightcurve_source: str,
    evidence_level: str,
) -> DiscoveryHoldoutRecord:
    raw_path = tmp_path / "raw" / f"{object_uid}.csv"
    _write_lightcurve(raw_path)
    return DiscoveryHoldoutRecord(
        object_uid=object_uid,
        canonical_name=canonical_name,
        release_id="J/ApJ/933/180",
        crossmatch_key=canonical_name,
        anomaly_category="changing_look_quasar",
        evidence_level=evidence_level,
        holdout_policy="holdout_only_no_optimization",
        benchmark_links=("gold_validation", "silver_validation"),
        lag_outlier=1.2,
        line_response_outlier=0.8,
        sonification_outlier=0.4,
        pre_state_lag=1.0,
        post_state_lag=2.6,
        pre_line_flux=2.0,
        post_line_flux=3.6,
        query_params={
            "raw_lightcurve_path": str(raw_path),
            "split_mjd": 3.0,
            "dataset_complete": True,
            "alignment_eligible": True,
            "state_transition_supported": True,
            "state_window_alignment": "changing_state_supported",
            "alignment_exclusion_reason": "",
            "state_transition_exclusion_reason": "",
            "state_sequence": [
                {"mjd": 2, "state": "D"},
                {"mjd": 4, "state": "B"},
            ],
            "selected_pair": {
                "pre_epoch": {"mjd": 2, "state": "D"},
                "post_epoch": {"mjd": 4, "state": "B"},
                "split_mjd": 3.0,
                "changing_state": True,
                "alignment_eligible": True,
                "state_transition_supported": True,
                "alignment_status": "changing_state_supported",
                "support_score": 1,
                "complete": True,
                "status": "complete",
                "pre_window_row_count": 2,
                "post_window_row_count": 2,
                "lightcurve_min_mjd": 1.0,
                "lightcurve_max_mjd": 6.0,
                "split_within_lightcurve_span": True,
                "pre_window_gap_days": 0.0,
                "post_window_gap_days": 0.0,
                "pre_window_g_row_count": 1,
                "pre_window_r_row_count": 1,
                "post_window_g_row_count": 1,
                "post_window_r_row_count": 1,
                "state_window_support_score": 1,
                "exclusion_reason": "",
            },
            "lightcurve_min_mjd": 1.0,
            "lightcurve_max_mjd": 6.0,
            "pre_window_row_count": 2,
            "post_window_row_count": 2,
            "pre_window_g_row_count": 1,
            "pre_window_r_row_count": 1,
            "post_window_g_row_count": 1,
            "post_window_r_row_count": 1,
            "state_window_support_score": 1,
            "pre_window_gap_days": 0.0,
            "post_window_gap_days": 0.0,
            "raw_lightcurve_source": raw_lightcurve_source,
        },
        notes=("synthetic test record",),
    )


def _write_corpus_scaleout_index(artifact_root: Path, object_uids: list[str]) -> None:
    run_dir = artifact_root / "corpus_scaleout"
    run_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        run_dir / "index.json",
        {
            "run_id": "corpus_scaleout",
            "package_type": "corpus_scaleout",
            "discovery_manifest": {
                "corpus_id": "discovery_holdout",
                "manifest_hash": "manifest-hash",
                "holdout_policy": "holdout_only_no_optimization",
                "release_ids": ["J/ApJ/933/180"],
                "object_uids": object_uids,
            },
        },
    )


def _write_first_pass_index(
    artifact_root: Path,
    *,
    promoted_snapshot_id: str,
    primary_ids: list[str],
    deferred_ids: list[str],
) -> None:
    run_dir = artifact_root / "first_pass_review"
    run_dir.mkdir(parents=True, exist_ok=True)
    candidates = [
        {"object_uid": object_uid, "review_wave": "primary"}
        for object_uid in primary_ids
    ] + [
        {"object_uid": object_uid, "review_wave": "deferred"}
        for object_uid in deferred_ids
    ]
    _write_json(
        run_dir / "index.json",
        {
            "run_id": "first_pass_review",
            "package_type": "first_pass_review",
            "promoted_snapshot": {
                "promoted_snapshot_id": promoted_snapshot_id,
            },
            "candidates": candidates,
        },
    )


def _write_manual_review_index(
    artifact_root: Path,
    *,
    promoted_snapshot_id: str,
    recommended_ids: list[str],
    reviewed: list[dict[str, object]],
) -> None:
    run_dir = artifact_root / "primary_wave_manual_review"
    run_dir.mkdir(parents=True, exist_ok=True)
    _write_json(
        run_dir / "index.json",
        {
            "promoted_snapshot_id": promoted_snapshot_id,
            "reviewed_candidate_count": len(reviewed),
            "recommended_rerun_candidates": recommended_ids,
            "primary_wave_reviewed": reviewed,
            "summary": {
                "advance_count": sum(
                    str(item.get("disposition", "")) == "advance" for item in reviewed
                ),
                "hold_count": sum(
                    str(item.get("disposition", "")) == "hold" for item in reviewed
                ),
                "drop_count": 0,
            },
        },
    )


def test_primary_wave_rerun_materializes_reviewed_subset_with_comparisons(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline_record = _build_record(
        tmp_path,
        object_uid="clq-a",
        canonical_name="J000000.00+000000.0",
        raw_lightcurve_source="live_irsa_download",
        evidence_level="real_raw_photometry_plus_catalog_transition",
    )
    deferred_record = _build_record(
        tmp_path,
        object_uid="clq-b",
        canonical_name="J000000.00+000000.1",
        raw_lightcurve_source="live_irsa_download",
        evidence_level="real_raw_photometry_plus_catalog_transition",
    )
    discovery_run_dir = tmp_path / "discovery_analysis"
    discovery_run_dir.mkdir(parents=True, exist_ok=True)
    baseline_candidate = materialize_discovery_candidate_bundle(
        record=baseline_record,
        run_id="discovery_analysis",
        run_dir=discovery_run_dir,
    )
    deferred_candidate = materialize_discovery_candidate_bundle(
        record=deferred_record,
        run_id="discovery_analysis",
        run_dir=discovery_run_dir,
    )
    _write_json(
        discovery_run_dir / "index.json",
        {
            "run_id": "discovery_analysis",
            "package_type": "discovery_analysis",
            "summary": {"candidate_count": 2},
            "candidates": [baseline_candidate, deferred_candidate],
        },
    )
    _write_corpus_scaleout_index(tmp_path, ["clq-a", "clq-b"])
    materialize_discovery_snapshot_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
    )
    _write_first_pass_index(
        tmp_path,
        promoted_snapshot_id="discovery_analysis-discovery_snapshot",
        primary_ids=["clq-a"],
        deferred_ids=["clq-b"],
    )
    _write_manual_review_index(
        tmp_path,
        promoted_snapshot_id="discovery_analysis-discovery_snapshot",
        recommended_ids=["clq-a"],
        reviewed=[
            {
                "object_uid": "clq-a",
                "canonical_name": "J000000.00+000000.0",
                "disposition": "advance",
                "reason": "Rerun the strongest reviewed candidate.",
                "key_caveat": "Synthetic test caveat.",
            }
        ],
    )

    rerun_record = _build_record(
        tmp_path,
        object_uid="clq-a",
        canonical_name="J000000.00+000000.0",
        raw_lightcurve_source="offline_ci_fallback",
        evidence_level="real_catalog_transition_with_offline_ztf_fallback",
    )

    def _fake_loader(
        repo_root: Path,
        *,
        selected_object_uids: tuple[str, ...] | None = None,
    ) -> tuple[DiscoveryHoldoutRecord, ...]:
        assert repo_root == ROOT
        requested = tuple(selected_object_uids or ())
        if requested == ("clq-a",):
            return (rerun_record,)
        raise AssertionError(f"unexpected rerun request: {requested}")

    monkeypatch.setattr(
        "echorm.eval.primary_wave_rerun.load_literal_discovery_holdout_records",
        _fake_loader,
    )

    index_path = materialize_primary_wave_rerun_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
    )
    payload = json.loads(index_path.read_text(encoding="utf-8"))

    assert payload["package_type"] == "primary_wave_rerun"
    assert payload["summary"]["recommended_rerun_candidate_count"] == 1
    assert payload["summary"]["rerun_candidate_count"] == 1
    assert payload["summary"]["degraded_candidate_count"] == 1
    assert payload["summary"]["offline_fallback_count"] == 1
    assert payload["manual_review_artifact"]["recommended_rerun_candidates"] == [
        "clq-a"
    ]
    assert (
        payload["claims_boundary"]["claims_scope"] == "repository_local_reviewed_rerun"
    )
    assert "offline_photometry_fallback_present" in payload["warnings"]

    candidates = payload["candidates"]
    assert [candidate["object_uid"] for candidate in candidates] == ["clq-a"]
    comparison = candidates[0]["comparison"]
    assert "baseline_promoted_payload" in candidates[0]
    assert "rerun_candidate_payload" in candidates[0]
    assert comparison["status"] == "raw_lightcurve_source_changed"
    assert comparison["transition_support_preserved"] is True
    assert comparison["transition_detected_preserved"] is True
    assert comparison["offline_fallback_present"] is True

    report = (tmp_path / "primary_wave_rerun" / "report.md").read_text(encoding="utf-8")
    assert "Promoted snapshot id" in report
    assert "Only candidates explicitly advanced by manual review are rerun." in report


def test_primary_wave_rerun_rejects_candidates_outside_primary_wave(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    baseline_record = _build_record(
        tmp_path,
        object_uid="clq-a",
        canonical_name="J000000.00+000000.0",
        raw_lightcurve_source="live_irsa_download",
        evidence_level="real_raw_photometry_plus_catalog_transition",
    )
    discovery_run_dir = tmp_path / "discovery_analysis"
    discovery_run_dir.mkdir(parents=True, exist_ok=True)
    baseline_candidate = materialize_discovery_candidate_bundle(
        record=baseline_record,
        run_id="discovery_analysis",
        run_dir=discovery_run_dir,
    )
    _write_json(
        discovery_run_dir / "index.json",
        {
            "run_id": "discovery_analysis",
            "package_type": "discovery_analysis",
            "summary": {"candidate_count": 1},
            "candidates": [baseline_candidate],
        },
    )
    _write_corpus_scaleout_index(tmp_path, ["clq-a"])
    materialize_discovery_snapshot_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
    )
    _write_first_pass_index(
        tmp_path,
        promoted_snapshot_id="discovery_analysis-discovery_snapshot",
        primary_ids=[],
        deferred_ids=["clq-a"],
    )
    _write_manual_review_index(
        tmp_path,
        promoted_snapshot_id="discovery_analysis-discovery_snapshot",
        recommended_ids=["clq-a"],
        reviewed=[
            {
                "object_uid": "clq-a",
                "canonical_name": "J000000.00+000000.0",
                "disposition": "advance",
                "reason": "Invalid recommendation for the test.",
                "key_caveat": "Synthetic test caveat.",
            }
        ],
    )

    monkeypatch.setattr(
        "echorm.eval.primary_wave_rerun.load_literal_discovery_holdout_records",
        lambda *args, **kwargs: (baseline_record,),
    )

    with pytest.raises(ValueError, match="subset of the first-pass primary wave"):
        materialize_primary_wave_rerun_package(
            repo_root=ROOT,
            artifact_root=tmp_path,
        )
