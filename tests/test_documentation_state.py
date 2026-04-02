from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_status_documents_reflect_main_integration() -> None:
    projectlist = _read("ark/projectlist.md")

    assert "not yet integrated into main" not in projectlist
    assert "implemented on the active branch" not in projectlist
    assert "integrated on main" in projectlist
    assert "repository-local" in projectlist


def test_claims_boundary_documents_are_explicit() -> None:
    readme = _read("README.md")
    releases = _read("docs/releases/index.md")
    playbook_0031 = _read("ark/playbooks/0031-root-authority-closeout-playbook.md")
    playbook_0038 = _read(
        "ark/playbooks/0038-literal-root-authority-remediation-playbook.md"
    )
    playbook_0046 = _read(
        "ark/playbooks/0046-adversarial-root-authority-gap-closure-plan.md"
    )
    playbook_0047 = _read(
        "ark/playbooks/0047-literal-root-authority-final-conformance-remediation.md"
    )

    assert "evidence labels" in readme
    assert "does not by itself mark an external release" in releases
    assert "repository-local" in playbook_0031
    assert "external peer review" in playbook_0031
    assert "claims-boundary checklist" in playbook_0038
    assert "repository-local" in playbook_0046
    assert "repository-local" in playbook_0047


def test_repository_local_package_specs_preserve_bounded_scope() -> None:
    for path in (
        "ark/specs/0039-real-backend-spectral-backend-integration.md",
        "ark/specs/0040-full-corpus-acquisition-raw-preservation-freeze.md",
        "ark/specs/0041-real-data-benchmark-execution-validation-closure.md",
        "ark/specs/0042-root-optimization-orchestration-objective-completion.md",
        "ark/specs/0043-holdout-discovery-clagn-real-data-analysis.md",
        "ark/specs/0044-publication-grade-release-analyst-workbench-archive-assembly.md",
        "ark/specs/0045-literal-root-authority-conformance-audit-final-readiness-gate.md",
        "ark/specs/0048-benchmark-governed-first-pass-review.md",
        "ark/specs/0049-canonical-discovery-snapshot-promotion-freeze.md",
    ):
        assert "repository-local" in _read(path)


def test_first_pass_project_entry_has_spec_plan_and_review() -> None:
    projectlist = _read("ark/projectlist.md")

    assert 'id: "0048"' in projectlist
    assert "ark/specs/0048-benchmark-governed-first-pass-review.md" in projectlist
    assert "ark/plans/0048-benchmark-governed-first-pass-review.md" in projectlist
    assert "ark/playbooks/0048-benchmark-governed-first-pass-review.md" in projectlist


def test_canonical_snapshot_project_entry_has_spec_and_review() -> None:
    projectlist = _read("ark/projectlist.md")
    review_0049 = _read(
        "ark/playbooks/0049-canonical-discovery-snapshot-promotion-freeze.md"
    )
    plan_0049 = _read("ark/plans/0049-canonical-discovery-snapshot-promotion-freeze.md")

    assert 'id: "0049"' in projectlist
    assert "ark/specs/0049-canonical-discovery-snapshot-promotion-freeze.md" in projectlist
    assert "ark/plans/0049-canonical-discovery-snapshot-promotion-freeze.md" in projectlist
    assert "ark/playbooks/0049-canonical-discovery-snapshot-promotion-freeze.md" in projectlist
    assert "Blocking Findings" in review_0049
    assert "divergence" in plan_0049
