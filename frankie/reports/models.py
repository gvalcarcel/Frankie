from __future__ import annotations

from dataclasses import dataclass

from frankie.core.models import AuditReport, DoctorReport, InventoryReport, StatusReport
from frankie.evidence.models import EvidenceLoadResult, EvidenceSummary, LiveEvidenceSummary


@dataclass(frozen=True)
class ConsolidatedReport:
    version: str
    mode: str
    generated_at: str
    executive_summary: str
    overall_status: str
    status: StatusReport
    inventory: InventoryReport
    audit: AuditReport
    doctor: DoctorReport
    evidence: EvidenceLoadResult
    evidence_summary: EvidenceSummary
    live_evidence: LiveEvidenceSummary
    smb_state: str
    portainer_state: str
    known_risks: tuple[str, ...]
    limitations: tuple[str, ...]
    recommended_next_steps: tuple[str, ...]
