from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_ci_limits_pull_requests_to_essential_validation() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )

    assert "workflow_dispatch:" in workflow
    assert "pr-essentials:" in workflow
    assert "if: github.event_name == 'pull_request'" in workflow
    assert "if: github.event_name != 'pull_request'" in workflow
    assert "name: PR Essentials" in workflow
    assert "tests/test_local_validation_gate.py" in workflow


def test_local_scientific_validation_gate_is_committed() -> None:
    script = (ROOT / "scripts" / "ci" / "run_local_scientific_validation.sh")
    text = script.read_text(encoding="utf-8")

    assert script.exists()
    assert "python3 -m ruff check ." in text
    assert "python3 -m mypy src tests" in text
    assert "python3 -m pytest" in text
    assert "snakemake --snakefile workflows/Snakefile --dry-run" in text
    assert "setup_scientific_runtimes.sh" in text


def test_git_hooks_delegate_to_the_local_scientific_validation_gate() -> None:
    pre_commit = (ROOT / ".githooks" / "pre-commit").read_text(encoding="utf-8")
    pre_push = (ROOT / ".githooks" / "pre-push").read_text(encoding="utf-8")
    installer = (ROOT / "scripts" / "ci" / "install_git_hooks.sh").read_text(
        encoding="utf-8"
    )

    assert "run_local_scientific_validation.sh" in pre_commit
    assert "pre-commit" in pre_commit
    assert "run_local_scientific_validation.sh" in pre_push
    assert "pre-push" in pre_push
    assert "git config core.hooksPath .githooks" in installer
