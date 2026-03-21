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
    materialize_optimization_closeout_package(artifact_root=artifact_root)
    materialize_release_closeout_package(artifact_root=artifact_root)
    audit_path = materialize_root_authority_audit(artifact_root=artifact_root)

    payload = json.loads(audit_path.read_text(encoding="utf-8"))
    summary = payload["summary"]
    assert summary["promotion_allowed"] is True
    assert summary["condition_count"] >= 7

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
    assert optimization_payload["objective_metrics"]["anomaly_candidate_count"] >= 5
