from __future__ import annotations

import json
import subprocess
from pathlib import Path

from echorm.eval.readiness import (
    ToolStatus,
    build_fixture_summaries,
    materialize_benchmark_readiness_run,
)

ROOT = Path(__file__).resolve().parent.parent


def _fake_command_runner(
    command: tuple[str, ...],
    repo_root: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=command,
        returncode=0,
        stdout=f"ok: {repo_root.name}:{' '.join(command)}",
        stderr="",
    )


def test_fixture_summaries_cover_benchmark_inputs() -> None:
    summaries = build_fixture_summaries(ROOT)

    assert [summary.dataset for summary in summaries] == ["agn_watch", "sdss_rm", "ztf"]
    assert summaries[0].record_count >= 3
    assert summaries[1].object_count == 1


def test_benchmark_readiness_materialization_writes_structured_bundle(
    tmp_path: Path,
) -> None:
    index_path = materialize_benchmark_readiness_run(
        repo_root=ROOT,
        artifact_root=tmp_path,
        run_id="testrun",
        profile="baseline",
        tools=(
            ToolStatus("python3", True, "/usr/bin/python3"),
            ToolStatus("git", True, "/usr/bin/git"),
            ToolStatus("snakemake", True, "/usr/bin/snakemake"),
        ),
        command_runner=_fake_command_runner,
    )

    run_payload = json.loads(index_path.read_text(encoding="utf-8"))
    root_index = json.loads((tmp_path / "index.json").read_text(encoding="utf-8"))

    assert run_payload["run_id"] == "testrun"
    assert run_payload["readiness"] == "ready"
    assert run_payload["summary"]["case_count"] == 4
    assert run_payload["summary"]["verification_total"] == 4
    assert root_index["runs"][0]["run_id"] == "testrun"

    case_summary = tmp_path / "testrun" / "cases" / "clean-seed-7" / "summary.md"
    assert case_summary.exists()
    assert "# Case clean-seed-7" in case_summary.read_text(encoding="utf-8")
