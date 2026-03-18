from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC_GLOBS = ("README.md", "AGENTS.md", "ark/**/*.md", "docs/**/*.md")
FORBIDDEN_PATTERNS = {
    "local_standard": re.compile(r"\.ark/local/"),
    "dashboard_state": re.compile(r"\.agent-dashboard/"),
    "consult_state": re.compile(r"\.consult/"),
    "dashboard_command": re.compile(
        r"\bad\s+(?:start|status|send|open|cleanup|spawn|stop)\b"
    ),
    "consult_command": re.compile(r"\bconsult\b"),
    "evolve_command": re.compile(r"\bark evolve\b"),
    "internal_role_architect": re.compile(r"\bArchitect\b"),
    "internal_role_builder": re.compile(r"\bBuilder\b"),
    "internal_role_evolve": re.compile(r"\bEvolve\b"),
}


def public_documents() -> list[Path]:
    documents: set[Path] = set()
    for pattern in PUBLIC_GLOBS:
        documents.update(ROOT.glob(pattern))
    return sorted(path for path in documents if path.is_file())


def list_violations(text: str) -> list[str]:
    return [
        name
        for name, pattern in FORBIDDEN_PATTERNS.items()
        if pattern.search(text)
    ]


def test_violation_detection_rejects_private_references() -> None:
    sample = """
    Review the local checklist at .ark/local/documentation-standard.md.
    Use consult before publishing and inspect the .agent-dashboard/ state.
    """
    violations = list_violations(sample)
    assert "local_standard" in violations
    assert "consult_command" in violations
    assert "dashboard_state" in violations


def test_violation_detection_allows_committed_references() -> None:
    sample = """
    The repository authority files are README.md and ark/projectlist.md.
    Quality checks are python3 -m pytest and python3 -m mypy src tests.
    """
    assert list_violations(sample) == []


def test_public_documents_avoid_private_artifacts_and_roles() -> None:
    violations: list[str] = []
    for path in public_documents():
        text = path.read_text(encoding="utf-8")
        for name in list_violations(text):
            violations.append(f"{path.relative_to(ROOT)}: {name}")

    assert violations == []
