rule optimization_plan:
    output:
        "artifacts/optimization/plan.ok"
    shell:
        "mkdir -p artifacts/optimization && touch {output}"
