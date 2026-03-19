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
