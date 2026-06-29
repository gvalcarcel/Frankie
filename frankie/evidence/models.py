from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StructuredEvidence:
    schema_version: str
    evidence_id: str
    evidence_type: str
    component_id: str
    component_name: str
    status: str
    severity: str
    mode: str
    data_source: str
    summary: str
    details: dict[str, Any]
    references: tuple[str, ...]
    server_impact: dict[str, bool]
    security: dict[str, bool]
    recommendation: str
    created_at: str | None = None
    updated_at: str | None = None
    source_files: tuple[str, ...] = ()
    related_checks: tuple[str, ...] = ()


@dataclass(frozen=True)
class EvidenceLoadIssue:
    path: str
    message: str


@dataclass(frozen=True)
class EvidenceLoadWarning:
    path: str
    message: str


@dataclass(frozen=True)
class EvidenceLoadResult:
    directory_available: bool
    directory: str
    evidence: tuple[StructuredEvidence, ...]
    issues: tuple[EvidenceLoadIssue, ...]
    warnings: tuple[EvidenceLoadWarning, ...] = ()

    @property
    def available(self) -> bool:
        return self.directory_available and bool(self.evidence)


@dataclass(frozen=True)
class EvidenceSummary:
    total: int
    invalid: int
    by_status: dict[str, int]
    by_severity: dict[str, int]
    by_component: dict[str, int]
    by_evidence_type: dict[str, int]
    by_data_source: dict[str, int]
    by_mode: dict[str, int]
    live_evidence: "LiveEvidenceSummary"


@dataclass(frozen=True)
class LiveEvidenceSummary:
    total: int
    readonly_captures: int
    access_cleanup: int
    server_contacted: bool
    changes_made: bool
    temporary_access_removed: bool
    evidence_ids: tuple[str, ...]
