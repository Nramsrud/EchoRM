# 0005 Canonical Schemas and Manifest Layer

## Summary

Define the canonical schemas and manifests that standardize objects, photometry, spectra, line metrics, lag results, and sonifications.

## Scope

- Define the object manifest.
- Define the photometry schema.
- Define the spectral-epoch index.
- Define the derived line-metric schema.
- Define the lag-result schema.
- Define the sonification manifest and dataset-level manifests.

## Non-Goals

- Implement survey readers.
- Implement reverberation methods or audio rendering.

## Global Constraints

- All committed outputs must remain formal, concise, precise, and limited to essential content.
- Downstream code must target canonical schemas rather than survey-specific raw formats.

## Acceptance Criteria

- Each canonical schema has a stable column contract and provenance policy.
- Required metadata for quality control, provenance, and downstream comparison are included.
- Schema definitions preserve raw-source traceability and support cross-survey analysis.

## Dependencies

- `0002`
- `0003`
