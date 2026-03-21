"""Benchmark readiness CLI entry point."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from ..eval.broad_validation import (
    materialize_continuum_validation_package,
    materialize_corpus_freeze_package,
    materialize_efficacy_benchmark_package,
    materialize_gold_validation_package,
    materialize_silver_validation_package,
)
from ..eval.claims_audit import materialize_claims_audit
from ..eval.first_benchmark import materialize_first_benchmark_package
from ..eval.readiness import materialize_benchmark_readiness_run
from ..eval.root_closeout import (
    materialize_advanced_rigor_package,
    materialize_corpus_scaleout_package,
    materialize_discovery_analysis_package,
    materialize_optimization_closeout_package,
    materialize_release_closeout_package,
    materialize_root_authority_audit,
)


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
    subparsers.add_parser(
        "corpus-freeze",
        help="Materialize the frozen benchmark corpus and multi-method package.",
    )
    subparsers.add_parser(
        "gold-validation",
        help="Materialize the gold benchmark validation package.",
    )
    subparsers.add_parser(
        "silver-validation",
        help="Materialize the silver benchmark validation package.",
    )
    subparsers.add_parser(
        "continuum-validation",
        help="Materialize the continuum benchmark validation package.",
    )
    subparsers.add_parser(
        "efficacy-benchmark",
        help="Materialize the sonification efficacy benchmark package.",
    )
    subparsers.add_parser(
        "claims-audit",
        help="Materialize the cross-package broad-validation claims audit.",
    )
    subparsers.add_parser(
        "advanced-rigor",
        help="Materialize the advanced-method and spectral-rigor package.",
    )
    subparsers.add_parser(
        "corpus-scaleout",
        help="Materialize the corpus-scaleout and discovery hold-out package.",
    )
    subparsers.add_parser(
        "optimization-closeout",
        help="Materialize the benchmark-governed optimization package.",
    )
    subparsers.add_parser(
        "discovery-analysis",
        help="Materialize the hold-out discovery and CLAGN analysis package.",
    )
    subparsers.add_parser(
        "release-closeout",
        help="Materialize the integrated release closeout package.",
    )
    subparsers.add_parser(
        "root-authority-audit",
        help="Materialize the full root-authority closeout audit.",
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
    broad_validation_profile = (
        "broad_validation" if args.profile == "baseline" else args.profile
    )
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
    if args.command == "corpus-freeze":
        index_path = materialize_corpus_freeze_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=broad_validation_profile,
        )
        print(index_path)
        return 0
    if args.command == "gold-validation":
        index_path = materialize_gold_validation_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=broad_validation_profile,
        )
        print(index_path)
        return 0
    if args.command == "silver-validation":
        index_path = materialize_silver_validation_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=broad_validation_profile,
        )
        print(index_path)
        return 0
    if args.command == "continuum-validation":
        index_path = materialize_continuum_validation_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=broad_validation_profile,
        )
        print(index_path)
        return 0
    if args.command == "efficacy-benchmark":
        index_path = materialize_efficacy_benchmark_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=broad_validation_profile,
        )
        print(index_path)
        return 0
    if args.command == "claims-audit":
        index_path = materialize_claims_audit(
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile=broad_validation_profile,
        )
        print(index_path)
        return 0
    if args.command == "advanced-rigor":
        index_path = materialize_advanced_rigor_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile="root_closeout" if args.profile == "baseline" else args.profile,
        )
        print(index_path)
        return 0
    if args.command == "corpus-scaleout":
        index_path = materialize_corpus_scaleout_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile="root_closeout" if args.profile == "baseline" else args.profile,
        )
        print(index_path)
        return 0
    if args.command == "discovery-analysis":
        index_path = materialize_discovery_analysis_package(
            repo_root=repo_root,
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile="root_closeout" if args.profile == "baseline" else args.profile,
        )
        print(index_path)
        return 0
    if args.command == "optimization-closeout":
        index_path = materialize_optimization_closeout_package(
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile="root_closeout" if args.profile == "baseline" else args.profile,
        )
        print(index_path)
        return 0
    if args.command == "release-closeout":
        index_path = materialize_release_closeout_package(
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile="root_closeout" if args.profile == "baseline" else args.profile,
        )
        print(index_path)
        return 0
    if args.command == "root-authority-audit":
        index_path = materialize_root_authority_audit(
            artifact_root=artifact_root,
            run_id=args.run_id,
            profile="root_closeout" if args.profile == "baseline" else args.profile,
        )
        print(index_path)
        return 0
    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
