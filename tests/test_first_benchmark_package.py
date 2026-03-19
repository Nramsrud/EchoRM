from __future__ import annotations

import json
from pathlib import Path

from echorm.eval.first_benchmark import materialize_first_benchmark_package
from echorm.eval.readiness import ToolStatus, VerificationCheck

ROOT = Path(__file__).resolve().parent.parent


def test_first_benchmark_package_materializes_explicit_evidence_levels(
    tmp_path: Path,
) -> None:
    index_path = materialize_first_benchmark_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="first_benchmark",
        verification=(
            VerificationCheck("pytest", ("python3", "-m", "pytest"), True, "ok"),
            VerificationCheck(
                "ruff",
                ("python3", "-m", "ruff", "check", "."),
                True,
                "ok",
            ),
            VerificationCheck(
                "mypy",
                ("python3", "-m", "mypy", "src", "tests"),
                True,
                "ok",
            ),
            VerificationCheck(
                "snakemake_dry_run",
                ("snakemake", "--snakefile", "workflows/Snakefile", "--dry-run"),
                True,
                "ok",
            ),
        ),
        tools=(
            ToolStatus("python3", True, "/usr/bin/python3"),
            ToolStatus("git", True, "/usr/bin/git"),
            ToolStatus("snakemake", True, "/usr/bin/snakemake"),
        ),
    )

    payload = json.loads(index_path.read_text(encoding="utf-8"))
    dossier_text = (tmp_path / "first_benchmark" / "dossier.md").read_text(
        encoding="utf-8"
    )
    root_index = json.loads((tmp_path / "index.json").read_text(encoding="utf-8"))

    assert payload["package_type"] == "first_benchmark"
    assert payload["summary"]["real_fixture_case_count"] == 3
    assert payload["summary"]["synthetic_case_count"] == 4
    assert payload["readiness"] == "ready_with_warnings"
    assert "Fixture-backed AGN Watch ingestion" in dossier_text
    assert "Not Yet Demonstrated" in dossier_text
    assert root_index["runs"][0]["package_type"] == "first_benchmark"
