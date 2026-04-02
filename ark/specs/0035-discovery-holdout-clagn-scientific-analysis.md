# 0035 Discovery Hold-Out and CLAGN Scientific Analysis

## Summary

Execute the root discovery program on hold-out ZTF and CLAGN corpora with interpretable anomaly ranking, transition timelines, and candidate evidence bundles.

## Scope

- Build interpretable anomaly scoring across continuum-lag, line-response, and sonification evidence.
- Add CLAGN transition and precursor analysis with aligned state evidence and timing.
- Materialize ranked candidate bundles, candidate memos, and taxonomy summaries for the hold-out pool.
- Record method support, evidence level, limitations, and review priority directly in discovery outputs.

## Non-Goals

- Benchmark optimization.
- Public release assembly.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Discovery analysis must operate only on the frozen hold-out corpus.
- Candidate ranking must remain traceable to explicit features and method support rather than opaque aggregate scores alone.

## Acceptance Criteria

- Discovery outputs include ranked candidates, anomaly categories, CLAGN transition records, and follow-up memos.
- Every candidate record preserves component scores, method-support metadata, and evidence boundaries.
- The discovery package is integrated into the review surface and the root closeout audit.
- Tests verify hold-out enforcement, score traceability, and candidate-output completeness.

## Dependencies

- `0019`
- `0032`
- `0033`
- `0034`
