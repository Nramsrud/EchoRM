from __future__ import annotations

import json
import shutil
from pathlib import Path

from echorm.eval.broad_validation import (
    materialize_continuum_validation_package,
    materialize_efficacy_benchmark_package,
    materialize_gold_validation_package,
    materialize_silver_validation_package,
)
from echorm.eval.claims_audit import materialize_claims_audit
from echorm.eval.discovery_snapshot import materialize_discovery_snapshot_package
from echorm.eval.first_pass import materialize_first_pass_review_package
from echorm.eval.readiness import ToolStatus, VerificationCheck
from echorm.eval.root_closeout import (
    materialize_advanced_rigor_package,
    materialize_corpus_scaleout_package,
    materialize_discovery_analysis_package,
    materialize_optimization_closeout_package,
    materialize_release_closeout_package,
    materialize_root_authority_audit,
)

ROOT = Path(__file__).resolve().parent.parent


def test_root_closeout_packages_materialize_and_audit() -> None:
    artifact_root = ROOT / "artifacts" / "test_root_closeout"
    if artifact_root.exists():
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True, exist_ok=True)
    verification = (
        VerificationCheck("pytest", ("python3", "-m", "pytest"), True, "ok"),
    )
    tools = (
        ToolStatus("python3", True, "/usr/bin/python3"),
        ToolStatus("git", True, "/usr/bin/git"),
        ToolStatus("snakemake", True, "/usr/bin/snakemake"),
    )

    materialize_gold_validation_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_silver_validation_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_continuum_validation_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_efficacy_benchmark_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_claims_audit(artifact_root=artifact_root)
    materialize_advanced_rigor_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_corpus_scaleout_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_discovery_analysis_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    snapshot_path = materialize_discovery_snapshot_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )
    materialize_optimization_closeout_package(artifact_root=artifact_root)
    materialize_release_closeout_package(artifact_root=artifact_root)
    audit_path = materialize_root_authority_audit(artifact_root=artifact_root)
    first_pass_path = materialize_first_pass_review_package(
        repo_root=ROOT,
        artifact_root=artifact_root,
        verification=verification,
        tools=tools,
    )

    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    summary = payload["summary"]
    assert summary["promotion_allowed"] is True
    assert summary["condition_count"] >= 7

    snapshot_payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
    assert snapshot_payload["source_run_id"] == "discovery_analysis"
    assert snapshot_payload["candidate_count"] >= 5
    assert snapshot_payload["summary"]["source_candidate_count"] >= 5
    assert (
        snapshot_payload["summary"]["excluded_incomplete_candidate_count"]
        + snapshot_payload["candidate_count"]
        == snapshot_payload["summary"]["source_candidate_count"]
    )

    first_pass_payload = json.loads(first_pass_path.read_text(encoding="utf-8"))
    promoted_snapshot = first_pass_payload["promoted_snapshot"]
    assert promoted_snapshot["snapshot_run_id"] == "discovery_snapshot"
    assert promoted_snapshot["source_run_id"] == "discovery_analysis"
    first_pass_candidates = first_pass_payload["candidates"]
    assert isinstance(first_pass_candidates, list)
    assert (
        first_pass_payload["summary"]["candidate_count"]
        == snapshot_payload["candidate_count"]
    )
    assert (
        first_pass_payload["summary"]["primary_wave_count"]
        + first_pass_payload["summary"]["deferred_wave_count"]
        == first_pass_payload["summary"]["candidate_count"]
    )
    primary_candidates = [
        candidate
        for candidate in first_pass_candidates
        if candidate["review_wave"] == "primary"
    ]
    deferred_candidates = [
        candidate
        for candidate in first_pass_candidates
        if candidate["review_wave"] == "deferred"
    ]
    assert first_pass_payload["strategy"]["primary_wave_rule"] == {
        "state_transition_supported": True,
        "transition_detected": True,
    }
    assert first_pass_payload["strategy"]["ordering_fields"] == [
        "review_priority",
        "rank_score",
        "benchmark_links",
        "object_uid",
    ]
    assert all(
        candidate["state_transition_supported"] is True
        and candidate["transition_detected"] is True
        for candidate in primary_candidates
    )
    assert all(
        candidate["state_transition_supported"] is False
        or candidate["transition_detected"] is False
        for candidate in deferred_candidates
    )
    assert (
        first_pass_payload["summary"]["primary_wave_count"]
        == len(primary_candidates)
    )
    assert (
        first_pass_payload["summary"]["deferred_wave_count"]
        == len(deferred_candidates)
    )
    assert all(
        candidate["real_data_rerun_required"] is True
        for candidate in first_pass_candidates
    )
    assert all(
        "transition_alignment_status" in candidate
        for candidate in first_pass_candidates
    )

    advanced_payload = json.loads(
        (artifact_root / "advanced_rigor" / "index.json").read_text(encoding="utf-8")
    )
    corpus_payload = json.loads(
        (artifact_root / "corpus_scaleout" / "index.json").read_text(encoding="utf-8")
    )
    optimization_payload = json.loads(
        (artifact_root / "optimization_closeout" / "index.json").read_text(
            encoding="utf-8"
        )
    )
    assert advanced_payload["summary"]["advanced_method_count"] >= 5
    assert advanced_payload["summary"]["advanced_object_count"] >= 1
    assert advanced_payload["summary"]["pyqsofit_coverage_rate"] >= 1.0
    assert corpus_payload["summary"]["silver_catalog_object_count"] >= 800
    assert corpus_payload["summary"]["discovery_complete_object_count"] >= 5
    assert corpus_payload["summary"]["discovery_transition_supported_object_count"] >= 1
    assert (
        corpus_payload["summary"]["discovery_complete_object_count"]
        >= corpus_payload["summary"]["discovery_transition_supported_object_count"]
    )
    assert optimization_payload["objective_metrics"]["anomaly_candidate_count"] >= 5
