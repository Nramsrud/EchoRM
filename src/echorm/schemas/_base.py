"""Shared schema helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TableSchema:
    """A tabular contract with explicit required, provenance, and quality fields."""

    name: str
    required_columns: tuple[str, ...]
    provenance_columns: tuple[str, ...] = ()
    quality_columns: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        all_columns = self.all_columns
        if len(all_columns) != len(set(all_columns)):
            raise ValueError(f"schema {self.name} contains duplicate column names")

    @property
    def all_columns(self) -> tuple[str, ...]:
        return (
            self.required_columns
            + self.provenance_columns
            + self.quality_columns
        )

    def missing_columns(self, columns: set[str]) -> tuple[str, ...]:
        return tuple(column for column in self.all_columns if column not in columns)

    def validate_record(self, record: Mapping[str, object]) -> tuple[str, ...]:
        """Return missing columns for a mapping-like record."""
        return self.missing_columns(set(record))

    def ordered_record(self, record: Mapping[str, object]) -> dict[str, object]:
        """Project a record into canonical schema order."""
        missing = self.validate_record(record)
        if missing:
            missing_columns = ", ".join(missing)
            raise ValueError(
                f"record for schema {self.name} is missing columns: "
                f"{missing_columns}"
            )
        return {column: record[column] for column in self.all_columns}
