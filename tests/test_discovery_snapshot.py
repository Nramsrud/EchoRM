from __future__ import annotations

import json
import shutil
from pathlib import Path

from echorm.eval.discovery_snapshot import (
    materialize_discovery_snapshot_package,
    validate_promoted_discovery_snapshot,
)
from echorm.eval.first_pass import materialize_first_pass_review_package
from echorm.eval.readiness import ToolStatus, VerificationCheck

ROOT = Path(__file__).resolve().parent.parent


def _copy_run(src_root: Path, dst_root: Path, run_id: str) -> None:
    shutil.copytree(src_root / run_id, dst_root / run_id)


def test_discovery_snapshot_promotion_is_complete_and_deterministic(
    tmp_path: Path,
) -> None:
    source_root = ROOT / "artifacts" / "benchmark_runs"
    for run_id in ("corpus_scaleout", "discovery_analysis"):
        _copy_run(source_root, tmp_path, run_id)

    index_path = materialize_discovery_snapshot_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=(
            VerificationCheck("pytest", ("python3", "-m", "pytest"), True, "ok"),
        ),
        tools=(ToolStatus("python3", True, "/usr/bin/python3"),),
    )

    payload = json.loads(index_path.read_text(encoding="utf-8"))
    assert payload["package_type"] == "discovery_snapshot"
    assert payload["summary"]["source_candidate_count"] == 5
    assert payload["candidate_count"] == 5
    assert payload["summary"]["excluded_incomplete_candidate_count"] == 0
    assert payload["source_run_id"] == "discovery_analysis"
    assert payload["corpus_reference"]["run_id"] == "corpus_scaleout"
    assert len(payload["candidate_inventory"]) == 5
    assert len(payload["candidate_inventory_digest"]) == 16
    assert len(payload["candidate_order_digest"]) == 16
    assert payload["candidate_order"] == [
        "ztf-holdout-001",
        "ztf-holdout-002",
        "ztf-holdout-003",
        "ztf-holdout-004",
        "ztf-holdout-005",
    ]

    validated = validate_promoted_discovery_snapshot(
        artifact_root=tmp_path,
        snapshot_run_id="discovery_snapshot",
    )
    assert (
        validated["candidate_inventory_digest"]
        == payload["candidate_inventory_digest"]
    )


def test_discovery_snapshot_excludes_incomplete_candidates(tmp_path: Path) -> None:
    source_root = ROOT / "artifacts" / "benchmark_runs"
    for run_id in ("corpus_scaleout", "discovery_analysis"):
        _copy_run(source_root, tmp_path, run_id)

    discovery_path = tmp_path / "discovery_analysis" / "index.json"
    discovery_payload = json.loads(discovery_path.read_text(encoding="utf-8"))
    for index, candidate in enumerate(discovery_payload["candidates"]):
        candidate["dataset_completeness"] = {
            "complete": index < 2,
            "alignment_eligible": index < 2,
            "state_transition_supported": index == 0,
            "state_window_alignment": (
                "changing_state_supported"
                if index == 0
                else (
                    "same_state_supported"
                    if index == 1
                    else "changing_state_incomplete"
                )
            ),
        }
    discovery_path.write_text(
        json.dumps(discovery_payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    index_path = materialize_discovery_snapshot_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
    )
    payload = json.loads(index_path.read_text(encoding="utf-8"))

    assert payload["summary"]["source_candidate_count"] == 5
    assert payload["candidate_count"] == 2
    assert payload["summary"]["excluded_incomplete_candidate_count"] == 3
    assert payload["candidate_order"] == ["ztf-holdout-001", "ztf-holdout-002"]
    assert "incomplete_candidates_excluded_from_promotion" in payload["warnings"]
    assert payload["candidate_inventory"][1]["state_transition_supported"] is False


def test_first_pass_rejects_unpromoted_discovery_divergence(tmp_path: Path) -> None:
    source_root = ROOT / "artifacts" / "benchmark_runs"
    for run_id in (
        "gold_validation",
        "silver_validation",
        "continuum_validation",
        "efficacy_benchmark",
        "corpus_scaleout",
        "discovery_analysis",
        "root_authority_audit",
    ):
        _copy_run(source_root, tmp_path, run_id)

    materialize_discovery_snapshot_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
    )

    discovery_path = tmp_path / "discovery_analysis" / "index.json"
    discovery_payload = json.loads(discovery_path.read_text(encoding="utf-8"))
    discovery_payload["candidates"] = list(discovery_payload["candidates"])[::-1]
    discovery_payload["summary"]["candidate_count"] = len(
        discovery_payload["candidates"]
    )
    discovery_path.write_text(
        json.dumps(discovery_payload, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    try:
        materialize_first_pass_review_package(
            repo_root=ROOT,
            artifact_root=tmp_path,
        )
    except ValueError as error:
        assert "promoted discovery snapshot diverged" in str(error)
    else:
        raise AssertionError("expected promoted snapshot divergence to fail")
