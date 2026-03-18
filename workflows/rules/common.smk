rule benchmark_manifest:
    output:
        "artifacts/manifests/bootstrap-manifest.txt"
    shell:
        "python3 -m echorm.cli.workflow --root . manifest"
