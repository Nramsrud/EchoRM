rule benchmark_manifest:
    output:
        "artifacts/manifests/bootstrap-manifest.txt"
    shell:
        "python3 -m echorm.cli.workflow --root . manifest"

rule benchmark_readiness:
    output:
        "artifacts/benchmark_runs/default/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id default readiness"

rule first_benchmark_package:
    output:
        "artifacts/benchmark_runs/first_benchmark/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id first_benchmark first-benchmark"

rule benchmark_corpus_freeze:
    output:
        "artifacts/benchmark_runs/corpus_freeze/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id corpus_freeze corpus-freeze"

rule gold_validation_package:
    output:
        "artifacts/benchmark_runs/gold_validation/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id gold_validation gold-validation"

rule silver_validation_package:
    output:
        "artifacts/benchmark_runs/silver_validation/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id silver_validation silver-validation"

rule continuum_validation_package:
    output:
        "artifacts/benchmark_runs/continuum_validation/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id continuum_validation continuum-validation"

rule efficacy_benchmark_package:
    output:
        "artifacts/benchmark_runs/efficacy_benchmark/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id efficacy_benchmark efficacy-benchmark"

rule claims_audit_package:
    input:
        "artifacts/benchmark_runs/gold_validation/index.json",
        "artifacts/benchmark_runs/silver_validation/index.json",
        "artifacts/benchmark_runs/continuum_validation/index.json",
        "artifacts/benchmark_runs/efficacy_benchmark/index.json"
    output:
        "artifacts/benchmark_runs/claims_audit/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id claims_audit claims-audit"

rule advanced_rigor_package:
    output:
        "artifacts/benchmark_runs/advanced_rigor/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id advanced_rigor advanced-rigor"

rule corpus_scaleout_package:
    output:
        "artifacts/benchmark_runs/corpus_scaleout/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id corpus_scaleout corpus-scaleout"

rule optimization_closeout_package:
    output:
        "artifacts/benchmark_runs/optimization_closeout/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id optimization_closeout optimization-closeout"

rule discovery_analysis_package:
    input:
        "artifacts/benchmark_runs/corpus_scaleout/index.json",
        "artifacts/benchmark_runs/optimization_closeout/index.json"
    output:
        "artifacts/benchmark_runs/discovery_analysis/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id discovery_analysis discovery-analysis"

rule release_closeout_package:
    input:
        "artifacts/benchmark_runs/discovery_analysis/index.json",
        "artifacts/benchmark_runs/claims_audit/index.json"
    output:
        "artifacts/benchmark_runs/release_closeout/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id release_closeout release-closeout"

rule root_authority_audit_package:
    input:
        "artifacts/benchmark_runs/claims_audit/index.json",
        "artifacts/benchmark_runs/advanced_rigor/index.json",
        "artifacts/benchmark_runs/corpus_scaleout/index.json",
        "artifacts/benchmark_runs/optimization_closeout/index.json",
        "artifacts/benchmark_runs/discovery_analysis/index.json",
        "artifacts/benchmark_runs/release_closeout/index.json"
    output:
        "artifacts/benchmark_runs/root_authority_audit/index.json"
    shell:
        "python3 -m echorm.cli.benchmark --repo-root . --artifact-root artifacts/benchmark_runs --run-id root_authority_audit root-authority-audit"
