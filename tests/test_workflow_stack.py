from __future__ import annotations

from pathlib import Path

from echorm.cli.workflow import main

ROOT = Path(__file__).resolve().parent.parent


def test_hydra_config_has_defaults() -> None:
    config_text = (ROOT / "configs" / "hydra" / "config.yaml").read_text(
        encoding="utf-8"
    )
    assert "defaults:" in config_text
    assert "project:" in config_text
    experiment_text = (ROOT / "configs" / "experiments" / "default.yaml").read_text(
        encoding="utf-8"
    )
    assert "tracking_backend: mlflow" in experiment_text
    assert "tracking_uri: mlruns" in experiment_text


def test_workflow_files_exist() -> None:
    snakefile = ROOT / "workflows" / "Snakefile"
    common_rules = ROOT / "workflows" / "rules" / "common.smk"
    assert snakefile.exists()
    assert common_rules.exists()


def test_dvc_metadata_exists() -> None:
    dvc_text = (ROOT / "dvc.yaml").read_text(encoding="utf-8")
    assert "stages:" in dvc_text
    assert "benchmark_manifest:" in dvc_text
    assert "bootstrap-manifest.txt" in dvc_text


def test_workflow_cli_materializes_bootstrap_manifest(tmp_path: Path) -> None:
    assert main(["--root", str(tmp_path), "manifest"]) == 0
    marker = tmp_path / "artifacts" / "manifests" / "bootstrap-manifest.txt"
    assert marker.exists()
    assert "dataset_manifest=manifests/datasets.yaml" in marker.read_text(
        encoding="utf-8"
    )
