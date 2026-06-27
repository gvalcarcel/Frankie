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


@dataclass(frozen=True)
class EvidenceLoadIssue:
    path: str
    message: str


@dataclass(frozen=True)
class EvidenceLoadResult:
    directory_available: bool
    directory: str
    evidence: tuple[StructuredEvidence, ...]
    issues: tuple[EvidenceLoadIssue, ...]

    @property
    def available(self) -> bool:
        return self.directory_available and bool(self.evidence)
