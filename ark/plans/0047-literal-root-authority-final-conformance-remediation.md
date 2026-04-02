# 0047 Literal Root Authority Final Conformance Remediation

## Goal

Execute the final remediation pass required to close the current adversarial findings and reach literal root-authority compliance in implementation, deliverables, and readiness.

## Governing Rule

Completion is allowed only when the implementation satisfies the root project plan and root agent specification without relying on proxy scope labels, synthetic substitutions, scalarized optimization summaries, or placeholder publication artifacts.

## Workstreams

### W1. Time and Normalization Conformance

Packages:
- `0040`
- `0041`
- `0045`

Required implementation:
1. Add documented per-object `t0` support to the canonical time model.
2. Recompute rest-frame times using the root-authority conversion rule.
3. Materialize `R0`, `R1`, and `R2` products and store their transform metadata explicitly.
4. Extend manifests, schemas, and release outputs to expose these parallel representations.
5. Extend the final audit to reject raw-only compliance claims.

Acceptance criteria:
- all root-closeout evidence records `t0` and uses the correct rest-frame transform
- `R0`, `R1`, and `R2` products are all present in tracked form
- audit checks validate both the transform and the representation set

### W2. Corpus Scope and Raw-Product Closure

Packages:
- `0040`
- `0045`

Required implementation:
1. Replace curated-slice silver and discovery scope with authority-aligned frozen scope.
2. Preserve SDSS-RM and ZTF raw products exactly as downloaded.
3. Materialize normalized derivative products in parallel.
4. Record release identifiers, exclusions, and scope counts in freeze manifests.
5. Expose scope labels clearly in review and release artifacts.

Acceptance criteria:
- freeze manifests enumerate included and excluded scope explicitly
- raw-product manifests exist for AGN Watch, SDSS-RM, and ZTF
- no artifact implies full-scope compliance from a curated slice

### W3. Real-Data Continuum Validation

Packages:
- `0041`
- `0045`

Required implementation:
1. Add real-data continuum benchmark cases sourced from tracked public data.
2. Keep synthetic families as support tasks only.
3. Report real-data continuum metrics separately from synthetic support metrics.
4. Wire the review surface to expose the real-data continuum cases clearly.

Acceptance criteria:
- continuum validation includes tracked real-data cases
- readiness claims distinguish real-data validation from synthetic support
- audit rejects synthetic-only continuum closure

### W4. Pareto Optimization Completion

Packages:
- `0042`
- `0045`

Required implementation:
1. Replace single-scalar optimization with explicit `M1` through `M7` objective handling.
2. Materialize Pareto-front outputs for `Ray Tune`, `Optuna`, and `Ax`.
3. Preserve keep-discard decisions and trade-off summaries in tracked artifacts.
4. Extend review surfaces to show objective trade-offs directly.

Acceptance criteria:
- optimizer outputs expose the full required metric family
- Pareto-front artifacts exist for all three backends
- audit rejects scalar-only promotion logic

### W5. Discovery and CLAGN Scientific Output Completion

Packages:
- `0043`
- `0045`

Required implementation:
1. Replace heuristic-only ranking with line-aware discovery products.
2. Materialize per-line anomaly scores, response asymmetry tables, and transition-aligned lag timelines.
3. Add pre/post sonification comparisons and precursor outputs to candidate bundles.
4. Ensure discovery evidence is tied to validated hold-out pipeline products.

Acceptance criteria:
- candidate bundles include the required line-aware scientific outputs
- CLAGN transition artifacts include aligned temporal evidence
- audit rejects discovery bundles that omit the required outputs

### W6. Publication and Release Completion

Packages:
- `0044`
- `0045`

Required implementation:
1. Replace draft markdown stubs with publication-grade methods and catalog bundles.
2. Materialize all required figures, tables, catalogs, leaderboards, and archives.
3. Extend release bundles and the analyst workbench to expose those outputs directly.
4. Preserve provenance and inventories for publication and archive artifacts.

Acceptance criteria:
- publication bundles are content-complete
- required catalog-level outputs exist in tracked form
- audit rejects placeholder publication artifacts

### W7. Final Adversarial Conformance Re-Run

Packages:
- `0045`

Required implementation:
1. Map each current adversarial finding to a direct conformance check.
2. Re-run the full root-authority audit on the remediated implementation.
3. Re-run repository quality gates and root-closeout materialization.
4. Produce a final findings-free adversarial review packet tied to the root authority documents.

Acceptance criteria:
- no adversarial finding remains against the root authority documents
- the final root-authority audit passes on literal evidence
- repository quality gates pass on the remediated implementation

## Sequencing

1. Implement `W1` before any further closeout or validation run.
2. Implement `W2` in parallel where feasible, but do not claim scope closure until both `W1` and `W2` are complete.
3. Implement `W3` before reassessing scientific readiness for continuum or full benchmark validation.
4. Implement `W4`, `W5`, and `W6` after the data-model and corpus corrections are in place.
5. Run `W7` only after all earlier workstreams have materialized tracked evidence.

## Verification

Repository gates:
- `python3 -m pytest`
- `python3 -m ruff check .`
- `python3 -m mypy src tests`
- `snakemake --snakefile workflows/Snakefile --dry-run`

Conformance checkpoints:
1. data-model verification for `t0`, rest-frame conversion, and `R0` / `R1` / `R2`
2. corpus verification for AGN Watch, SDSS-RM, and ZTF raw-preservation and freeze manifests
3. continuum verification for real-data continuum benchmark cases
4. optimization verification for literal Pareto outputs
5. discovery verification for line-aware and transition-aware outputs
6. publication verification for content-complete release bundles
7. final adversarial re-review against the root authority documents

## Exit Criteria

This remediation plan is complete only when:

- the current adversarial findings are closed in tracked implementation and artifacts
- the final root-authority audit passes on literal evidence
- repository quality gates pass
- a renewed adversarial review finds no remaining mismatch between the implementation and the root authority documents
