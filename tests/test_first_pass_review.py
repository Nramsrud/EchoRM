from __future__ import annotations

import json
import shutil
from pathlib import Path

from echorm.eval.discovery_snapshot import materialize_discovery_snapshot_package
from echorm.eval.first_pass import materialize_first_pass_review_package
from echorm.eval.readiness import ToolStatus, VerificationCheck

ROOT = Path(__file__).resolve().parent.parent


def _copy_run(src_root: Path, dst_root: Path, run_id: str) -> None:
    shutil.copytree(src_root / run_id, dst_root / run_id)


def test_first_pass_review_materializes_deterministic_waves(tmp_path: Path) -> None:
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
        verification=(
            VerificationCheck("pytest", ("python3", "-m", "pytest"), True, "ok"),
        ),
        tools=(
            ToolStatus("python3", True, "/usr/bin/python3"),
            ToolStatus("git", True, "/usr/bin/git"),
        ),
    )

    index_path = materialize_first_pass_review_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=(
            VerificationCheck("pytest", ("python3", "-m", "pytest"), True, "ok"),
        ),
        tools=(
            ToolStatus("python3", True, "/usr/bin/python3"),
            ToolStatus("git", True, "/usr/bin/git"),
        ),
    )

    payload = json.loads(index_path.read_text(encoding="utf-8"))
    assert payload["package_type"] == "first_pass_review"
    assert payload["summary"]["anchor_count"] == 6
    assert payload["summary"]["candidate_count"] == 5
    assert payload["summary"]["primary_wave_count"] == 3
    assert payload["summary"]["deferred_wave_count"] == 2
    assert payload["summary"]["real_data_rerun_required_count"] == 5
    assert payload["promoted_snapshot"]["snapshot_run_id"] == "discovery_snapshot"
    assert payload["promoted_snapshot"]["promoted_snapshot_id"] == (
        "discovery_analysis-discovery_snapshot"
    )
    assert len(payload["promoted_snapshot"]["candidate_inventory_digest"]) == 16

    candidates = payload["candidates"]
    assert isinstance(candidates, list)
    primary_ids = [
        item["object_uid"] for item in candidates if item["review_wave"] == "primary"
    ]
    deferred_ids = [
        item["object_uid"] for item in candidates if item["review_wave"] == "deferred"
    ]
    assert primary_ids == ["ztf-holdout-001", "ztf-holdout-003", "ztf-holdout-005"]
    assert deferred_ids == ["ztf-holdout-004", "ztf-holdout-002"]
    assert all(item["real_data_rerun_required"] is True for item in candidates)

    report = (tmp_path / "first_pass_review" / "report.md").read_text(
        encoding="utf-8"
    )
    assert "real-data rerun" in report
    assert "Promoted snapshot id" in report
    assert "fixture-bounded" in report

    candidate_summary = (
        tmp_path / "first_pass_review" / "candidates" / "ztf-holdout-001" / "memo.md"
    ).read_text(encoding="utf-8")
    assert "Review wave: primary" in candidate_summary
    assert "manual_review_then_real_data_rerun" in candidate_summary
