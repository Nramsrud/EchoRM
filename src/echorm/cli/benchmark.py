"""Benchmark readiness CLI entry point."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ..eval.first_benchmark import materialize_first_benchmark_package
from ..eval.readiness import materialize_benchmark_readiness_run


def build_parser() -> argparse.ArgumentParser:
    """Build the benchmark readiness CLI parser."""
    parser = argparse.ArgumentParser(prog="python -m echorm.cli.benchmark")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root used for fixture and command resolution.",
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        default=Path("artifacts/benchmark_runs"),
        help="Artifact root used for benchmark readiness bundles.",
    )
    parser.add_argument(
        "--run-id",
        default="default",
        help="Run identifier written under the artifact root.",
    )
    parser.add_argument(
        "--profile",
        default="baseline",
        help="Benchmark readiness profile label.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=7,
        help="Base seed used for deterministic synthetic benchmark families.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("readiness", help="Materialize a benchmark readiness bundle.")
    subparsers.add_parser(
        "first-benchmark",
        help="Materialize the first bounded benchmark package.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the benchmark readiness CLI."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    repo_root = args.repo_root.resolve()
    artifact_root = (
        args.artifact_root
        if args.artifact_root.is_absolute()
        else (repo_root / args.artifact_root)
    ).resolve()
    if args.command == "readiness":
        index_path = materialize_benchmark_readiness_run(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=args.profile,
            seed=args.seed,
        )
        print(index_path)
        return 0
    if args.command == "first-benchmark":
        profile = args.profile
        if profile == "baseline":
            profile = "first_benchmark"
        index_path = materialize_first_benchmark_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=profile,
            seed=args.seed,
        )
        print(index_path)
        return 0
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
