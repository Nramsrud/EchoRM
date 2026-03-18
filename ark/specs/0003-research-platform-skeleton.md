# 0003 Research Platform Skeleton

## Summary

Define the repository topology, package layout, and top-level interfaces required by the scientific plan.

## Scope

- Establish the top-level directory structure for configuration, data, manifests, workflows, source modules, tests, notebooks, agents, and public documentation.
- Define the module taxonomy for ingest, crossmatch, calibrate, spectra, photometry, reverberation inference, simulation, sonification, embeddings, anomaly analysis, evaluation, reporting, and command-line entry points.
- Specify the boundary between reusable library code, command-line interfaces, and release-facing outputs.

## Non-Goals

- Implement the workflow stack.
- Implement dataset readers or scientific methods.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Module boundaries must keep mutation surfaces narrow and scientifically legible.

## Acceptance Criteria

- The target repository topology is defined without ambiguity.
- Each top-level source module has a stated responsibility and interface boundary.
- The specification preserves a clear separation between reusable code, data products, and publication outputs.

## Dependencies

- `0002`
