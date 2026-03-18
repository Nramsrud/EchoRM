from __future__ import annotations

from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_DIRECTORIES = (
    ROOT / "agents",
    ROOT / "configs",
    ROOT / "configs" / "datasets",
    ROOT / "configs" / "experiments",
    ROOT / "configs" / "hydra",
    ROOT / "data",
    ROOT / "docs" / "references",
    ROOT / "environment",
    ROOT / "manifests",
    ROOT / "notebooks" / "exploratory",
    ROOT / "notebooks" / "validation",
    ROOT / "workflows" / "rules",
)
REQUIRED_MODULES = (
    "echorm.ingest",
    "echorm.crossmatch",
    "echorm.calibrate",
    "echorm.spectra",
    "echorm.photometry",
    "echorm.rm",
    "echorm.simulate",
    "echorm.sonify",
    "echorm.embeddings",
    "echorm.anomaly",
    "echorm.eval",
    "echorm.reports",
    "echorm.cli",
)


def test_required_directories_exist() -> None:
    missing = [
        path.relative_to(ROOT)
        for path in REQUIRED_DIRECTORIES
        if not path.exists()
    ]
    assert missing == []


def test_required_modules_are_importable() -> None:
    for module in REQUIRED_MODULES:
        imported = import_module(module)
        assert imported.__doc__
