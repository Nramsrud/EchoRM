from __future__ import annotations

import json
import subprocess
import threading
from pathlib import Path
from urllib.request import urlopen

from echorm.cli.review_app import resolve_bind_host
from echorm.eval.broad_validation import (
    materialize_continuum_validation_package,
    materialize_efficacy_benchmark_package,
    materialize_gold_validation_package,
    materialize_silver_validation_package,
)
from echorm.eval.claims_audit import materialize_claims_audit
from echorm.eval.first_benchmark import materialize_first_benchmark_package
from echorm.eval.readiness import (
    ToolStatus,
    VerificationCheck,
    materialize_benchmark_readiness_run,
)
from echorm.eval.root_closeout import (
    materialize_advanced_rigor_package,
    materialize_corpus_scaleout_package,
    materialize_discovery_analysis_package,
    materialize_optimization_closeout_package,
    materialize_release_closeout_package,
)
from echorm.reports.review_app import create_review_server

ROOT = Path(__file__).resolve().parent.parent


def _fake_verification_runner(
    command: tuple[str, ...],
    repo_root: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=command,
        returncode=0,
        stdout=f"ok: {repo_root.name}:{' '.join(command)}",
        stderr="",
    )


def _materialize_run(tmp_path: Path) -> None:
    materialize_benchmark_readiness_run(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="testrun",
        tools=(
            ToolStatus("python3", True, "/usr/bin/python3"),
            ToolStatus("git", True, "/usr/bin/git"),
            ToolStatus("snakemake", True, "/usr/bin/snakemake"),
        ),
        command_runner=_fake_verification_runner,
    )


def _materialize_first_benchmark_run(tmp_path: Path) -> None:
    materialize_first_benchmark_package(
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


def _materialize_root_closeout_runs(tmp_path: Path) -> None:
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
        artifact_root=tmp_path,
        run_id="gold_validation",
        verification=verification,
        tools=tools,
    )
    materialize_silver_validation_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="silver_validation",
        verification=verification,
        tools=tools,
    )
    materialize_continuum_validation_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="continuum_validation",
        verification=verification,
        tools=tools,
    )
    materialize_efficacy_benchmark_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="efficacy_benchmark",
        verification=verification,
        tools=tools,
    )
    materialize_claims_audit(artifact_root=tmp_path, run_id="claims_audit")
    materialize_advanced_rigor_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="advanced_rigor",
        verification=verification,
        tools=tools,
    )
    materialize_corpus_scaleout_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="corpus_scaleout",
        verification=verification,
        tools=tools,
    )
    materialize_optimization_closeout_package(
        artifact_root=tmp_path,
        run_id="optimization_closeout",
    )
    materialize_discovery_analysis_package(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="discovery_analysis",
        verification=verification,
        tools=tools,
    )
    materialize_release_closeout_package(
        artifact_root=tmp_path,
        run_id="release_closeout",
    )


def test_bind_host_prefers_tailscale_and_supports_localhost_override() -> None:
    assert resolve_bind_host(localhost=True) == "127.0.0.1"
    assert resolve_bind_host(
        localhost=False,
        run_command=(
            lambda command: "100.101.102.103"
            if command[0] == "tailscale"
            else None
        ),
    ) == "100.101.102.103"


def test_bind_host_requires_explicit_localhost_when_tailscale_is_missing() -> None:
    try:
        resolve_bind_host(localhost=False, run_command=lambda command: None)
    except RuntimeError as error:
        assert "Tailscale" in str(error)
    else:
        raise AssertionError("expected Tailscale-first host resolution to fail")


def test_review_app_serves_html_and_json_views(tmp_path: Path) -> None:
    _materialize_run(tmp_path)
    server = create_review_server(
        artifact_root=tmp_path,
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        index_text = urlopen(f"http://127.0.0.1:{port}/").read().decode("utf-8")
        runs_payload = json.loads(
            urlopen(f"http://127.0.0.1:{port}/api/runs").read().decode("utf-8")
        )
        run_text = urlopen(f"http://127.0.0.1:{port}/runs/testrun").read().decode(
            "utf-8"
        )
        case_payload = json.loads(
            urlopen(
                f"http://127.0.0.1:{port}/api/runs/testrun/cases/clean-seed-7"
            )
            .read()
            .decode("utf-8")
        )
        file_text = urlopen(
            f"http://127.0.0.1:{port}/files/testrun/summary.md"
        ).read().decode("utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert "Benchmark Review" in index_text
    assert runs_payload["runs"][0]["run_id"] == "testrun"
    assert "Run testrun" in run_text
    assert case_payload["case_id"] == "clean-seed-7"
    assert "# Benchmark Readiness testrun" in file_text


def test_review_app_renders_first_benchmark_package_metadata(
    tmp_path: Path,
) -> None:
    _materialize_first_benchmark_run(tmp_path)
    server = create_review_server(
        artifact_root=tmp_path,
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        index_text = urlopen(f"http://127.0.0.1:{port}/").read().decode("utf-8")
        run_text = urlopen(
            f"http://127.0.0.1:{port}/runs/first_benchmark"
        ).read().decode("utf-8")
        dossier_text = urlopen(
            f"http://127.0.0.1:{port}/files/first_benchmark/dossier.md"
        ).read().decode("utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert "first_benchmark" in index_text
    assert "first_benchmark" in run_text
    assert "Package type: first_benchmark" in run_text
    assert "Scope:" in run_text
    assert "First Benchmark Dossier first_benchmark" in dossier_text


def test_review_app_serves_root_closeout_routes(tmp_path: Path) -> None:
    _materialize_run(tmp_path)
    _materialize_first_benchmark_run(tmp_path)
    _materialize_root_closeout_runs(tmp_path)
    discovery_payload = json.loads(
        (tmp_path / "discovery_analysis" / "index.json").read_text(encoding="utf-8")
    )
    candidates = discovery_payload.get("candidates", [])
    assert isinstance(candidates, list) and candidates
    candidate_id = str(candidates[0]["object_uid"])
    server = create_review_server(
        artifact_root=tmp_path,
        host="127.0.0.1",
        port=0,
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_port
        advanced_text = urlopen(
            f"http://127.0.0.1:{port}/runs/advanced_rigor"
        ).read().decode("utf-8")
        candidate_payload = json.loads(
            urlopen(
                f"http://127.0.0.1:{port}/api/runs/discovery_analysis/candidates/{candidate_id}"
            ).read().decode("utf-8")
        )
        experiment_text = urlopen(
            f"http://127.0.0.1:{port}/runs/optimization_closeout/experiments/optuna"
        ).read().decode("utf-8")
        bundle_text = urlopen(
            f"http://127.0.0.1:{port}/runs/release_closeout/bundles/v1.0.0-rc1"
        ).read().decode("utf-8")
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()

    assert "advanced_rigor" in advanced_text
    assert candidate_payload["object_uid"] == candidate_id
    assert "Experiment optuna" in experiment_text
    assert "Bundle v1.0.0-rc1" in bundle_text
