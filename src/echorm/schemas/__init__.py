"""Canonical schema exports."""

from ._base import TableSchema
from .lags import LAG_RESULT_SCHEMA
from .line_metrics import LINE_METRICS_SCHEMA
from .objects import OBJECT_MANIFEST_SCHEMA
from .photometry import PHOTOMETRY_SCHEMA
from .sonifications import SONIFICATION_SCHEMA
from .spectra import SPECTRAL_EPOCH_SCHEMA

__all__ = [
    "LAG_RESULT_SCHEMA",
    "LINE_METRICS_SCHEMA",
    "OBJECT_MANIFEST_SCHEMA",
    "PHOTOMETRY_SCHEMA",
    "SONIFICATION_SCHEMA",
    "SPECTRAL_EPOCH_SCHEMA",
    "TableSchema",
]
