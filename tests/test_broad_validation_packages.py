from __future__ import annotations

import json
import threading
from pathlib import Path
from urllib.request import urlopen

from echorm.eval.broad_validation import (
    materialize_continuum_validation_package,
    materialize_corpus_freeze_package,
    materialize_efficacy_benchmark_package,
    materialize_gold_validation_package,
    materialize_silver_validation_package,
)
from echorm.eval.claims_audit import materialize_claims_audit
from echorm.eval.readiness import ToolStatus, VerificationCheck
from echorm.reports.review_app import create_review_server

ROOT = Path(__file__).resolve().parent.parent

VERIFICATION = (
    VerificationCheck("pytest", ("python3", "-m", "pytest"), True, "ok"),
    VerificationCheck("ruff", ("python3", "-m", "ruff", "check", "."), True, "ok"),
    VerificationCheck("mypy", ("python3", "-m", "mypy", "src", "tests"), True, "ok"),
    VerificationCheck(
        "snakemake_dry_run",
        ("snakemake", "--snakefile", "workflows/Snakefile", "--dry-run"),
        True,
        "ok",
    ),
)

TOOLS = (
    ToolStatus("python3", True, "/usr/bin/python3"),
    ToolStatus("git", True, "/usr/bin/git"),
    ToolStatus("snakemake", True, "/usr/bin/snakemake"),
)


def _materialize_all(tmp_path: Path) -> None:
    materialize_corpus_freeze_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=VERIFICATION,
        tools=TOOLS,
    )
    materialize_gold_validation_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=VERIFICATION,
        tools=TOOLS,
    )
    materialize_silver_validation_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=VERIFICATION,
        tools=TOOLS,
    )
    materialize_continuum_validation_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=VERIFICATION,
        tools=TOOLS,
    )
    materialize_efficacy_benchmark_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        verification=VERIFICATION,
        tools=TOOLS,
    )
    materialize_claims_audit(
        artifact_root=tmp_path,
    )


def test_broad_validation_packages_materialize_and_claims_audit_passes(
    tmp_path: Path,
) -> None:
    _materialize_all(tmp_path)
    audit = json.loads(
        (tmp_path / "claims_audit" / "index.json").read_text(encoding="utf-8")
    )
    silver = json.loads(
        (tmp_path / "silver_validation" / "index.json").read_text(encoding="utf-8")
    )

    assert audit["package_type"] == "claims_audit"
    assert audit["summary"]["promotion_allowed"] is True
    assert audit["summary"]["conditions_passed"] == audit["summary"]["condition_count"]
    assert audit["summary"]["condition_count"] >= 16
    assert silver["summary"]["population_count"] == 4
    assert silver["summary"]["coverage_rate"] >= 0.75
    assert len(silver["comparisons"]) >= 2


def test_review_app_serves_broad_validation_object_task_and_audit_views(
    tmp_path: Path,
) -> None:
    _materialize_all(tmp_path)
    server = create_review_server(
        artifact_root=tmp_path,
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        gold_text = urlopen(
            f"http://127.0.0.1:{port}/runs/gold_validation"
        ).read().decode("utf-8")
        object_text = urlopen(
            f"http://127.0.0.1:{port}/runs/gold_validation/objects/ngc5548"
        ).read().decode("utf-8")
        method_text = urlopen(
            f"http://127.0.0.1:{port}/runs/gold_validation/methods/ngc5548-pyzdcf"
        ).read().decode("utf-8")
        rerun_text = urlopen(
            f"http://127.0.0.1:{port}/runs/gold_validation/reruns/gold_primary_metric_stability"
        ).read().decode("utf-8")
        task_text = urlopen(
            f"http://127.0.0.1:{port}/runs/efficacy_benchmark/tasks/lag_order_audio"
        ).read().decode("utf-8")
        cohort_payload = json.loads(
            urlopen(
                f"http://127.0.0.1:{port}/api/runs/efficacy_benchmark/cohorts/trained"
            )
            .read()
            .decode("utf-8")
        )
        audit_text = urlopen(
            f"http://127.0.0.1:{port}/runs/claims_audit"
        ).read().decode("utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert "gold_validation" in gold_text
    assert "Object ngc5548" in object_text
    assert "Method ngc5548-pyzdcf" in method_text
    assert "Rerun gold_primary_metric_stability" in rerun_text
    assert "Task lag_order_audio" in task_text
    assert cohort_payload["cohort_id"] == "trained"
    assert "Claims Audit" in audit_text
