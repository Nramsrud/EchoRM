"""Workflow-facing command helpers."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path


def manifest_output_path(root: Path) -> Path:
    """Return the bootstrap manifest artifact directory."""
    return root / "artifacts" / "manifests"


def write_manifest_marker(root: Path) -> Path:
    """Create the bootstrap manifest marker consumed by workflow dry runs."""
    output_dir = manifest_output_path(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    marker_path = output_dir / "bootstrap-manifest.txt"
    marker_path.write_text(
        "dataset_manifest=manifests/datasets.yaml\n",
        encoding="utf-8",
    )
    return marker_path


def build_parser() -> argparse.ArgumentParser:
    """Build the workflow CLI parser."""
    parser = argparse.ArgumentParser(prog="python -m echorm.cli.workflow")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root used for artifact output.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("manifest", help="Materialize the bootstrap manifest.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the workflow CLI."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    root = args.root.resolve()
    if args.command == "manifest":
        write_manifest_marker(root)
        return 0
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
