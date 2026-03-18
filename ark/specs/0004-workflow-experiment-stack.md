# 0004 Workflow and Experiment Stack

## Summary

Define the reproducible workflow, configuration, data-versioning, and experiment-tracking substrate for the project.

## Scope

- Define the workflow layer around Snakemake.
- Define the configuration layer around Hydra.
- Define the data-versioning boundary around DVC.
- Define the experiment-tracking boundary around MLflow.
- Specify how tracked metadata and large generated state remain separate.

## Non-Goals

- Implement survey-specific readers.
- Optimize experiments or search spaces.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Large generated state must remain outside normal versioned content.

## Acceptance Criteria

- The workflow entry points, configuration tree, experiment records, and data-versioning boundary are explicitly defined.
- The specification states which artifacts are versioned directly and which remain external or generated.
- The resulting stack can support staged execution without conflating data lineage, configuration, and experiment metrics.

## Dependencies

- `0002`
- `0003`
