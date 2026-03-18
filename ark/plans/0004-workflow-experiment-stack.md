# 0004 Workflow and Experiment Stack Plan

## Goal

Stand up the reproducible workflow substrate for configuration, execution, data-versioning boundaries, and experiment tracking.

## Implementation Approach

Create a minimal but operational stack around Snakemake, Hydra, DVC, and MLflow, with tracked configuration and workflow entry points separated from generated runtime state.

## Steps

1. Create the tracked directory structure for `configs/`, `workflows/`, and `environment/`, including baseline configuration composition and a top-level workflow entry point.
2. Define the initial workflow graph and rule partitioning for ingestion, normalization, benchmarks, and reporting without yet implementing the full science logic.
3. Add DVC-facing metadata and ignore boundaries for large data and generated state, and define the MLflow tracking boundary for experiment artifacts.
4. Add smoke tests or fixture-backed checks for configuration loading, workflow parseability, and basic dry-run behavior.

## Expected File Changes

### New Files

- `configs/hydra/config.yaml` - top-level configuration composition entry point
- `configs/datasets/default.yaml` - dataset defaults
- `configs/experiments/default.yaml` - experiment defaults
- `workflows/Snakefile` - workflow entry point
- `workflows/rules/` - rule modules for staged execution
- `dvc.yaml` - tracked data-pipeline metadata when appropriate
- `.dvcignore` - DVC ignore boundary
- `tests/test_workflow_stack.py` - configuration and workflow smoke tests

### Modified Files

- `.gitignore` - generated-state boundaries if additional paths are needed
- `README.md` - public workflow surfaces if needed

## Validation

- `python3 -m pytest tests/test_workflow_stack.py`
- `snakemake --snakefile workflows/Snakefile --dry-run`

## Exit Criteria

- The repository has a tracked workflow entry point and configuration tree.
- Generated workflow, tracking, and data-versioning state remain outside normal versioned content.
- The workflow stack is parseable and supports dry-run execution.

## Risks

| Risk | Mitigation |
|------|------------|
| Workflow scaffolding grows into a second source of truth | Keep configuration, workflow graph, and manifest interfaces explicitly separated |
| Tool setup creates non-portable local assumptions | Test the tracked entry points in a clean environment with dry-run checks |

## Dependencies

- `0002`
- `0003`
