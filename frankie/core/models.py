from __future__ import annotations

from dataclasses import dataclass


ALLOWED_STATES = ("OK", "WARNING", "ERROR", "UNKNOWN", "PENDING", "MISSING EVIDENCE")
ALLOWED_INVENTORY_STATES = ("KNOWN", "UNKNOWN", "PARTIAL", "PENDING", "MISSING EVIDENCE")
ALLOWED_AUDIT_STATUSES = ("PASS", "WARN", "FAIL", "UNKNOWN", "PENDING", "MISSING_EVIDENCE")
ALLOWED_AUDIT_SEVERITIES = ("INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL")
ALLOWED_DOCTOR_RESULTS = ("HEALTHY", "ACTIONS_RECOMMENDED", "ATTENTION_REQUIRED", "INSUFFICIENT_EVIDENCE", "CRITICAL")


@dataclass(frozen=True)
class StatusItem:
    name: str
    state: str
    detail: str = ""

    def __post_init__(self) -> None:
        if self.state not in ALLOWED_STATES:
            raise ValueError(f"Unsupported status state: {self.state}")


@dataclass(frozen=True)
class StatusSection:
    title: str
    items: tuple[StatusItem, ...]


@dataclass(frozen=True)
class StatusReport:
    version: str
    mode: str
    sections: tuple[StatusSection, ...]
    overall_status: str


@dataclass(frozen=True)
class InventoryItem:
    name: str
    value: str
    state: str = "KNOWN"

    def __post_init__(self) -> None:
        if self.state not in ALLOWED_INVENTORY_STATES:
            raise ValueError(f"Unsupported inventory state: {self.state}")


@dataclass(frozen=True)
class InventorySection:
    title: str
    items: tuple[InventoryItem, ...]


@dataclass(frozen=True)
class InventoryReport:
    version: str
    mode: str
    sections: tuple[InventorySection, ...]


@dataclass(frozen=True)
class AuditSource:
    path: str
    available: bool


@dataclass(frozen=True)
class AuditFinding:
    id: str
    name: str
    description: str
    category: str
    status: str
    severity: str
    evidence: tuple[str, ...]
    message: str
    recommendation: str
    limitation: str = ""

    def __post_init__(self) -> None:
        if self.status not in ALLOWED_AUDIT_STATUSES:
            raise ValueError(f"Unsupported audit status: {self.status}")
        if self.severity not in ALLOWED_AUDIT_SEVERITIES:
            raise ValueError(f"Unsupported audit severity: {self.severity}")


@dataclass(frozen=True)
class AuditCheck:
    id: str
    name: str
    description: str
    category: str


@dataclass(frozen=True)
class AuditReport:
    version: str
    mode: str
    scope: tuple[InventoryItem, ...]
    sources: tuple[AuditSource, ...]
    findings: tuple[AuditFinding, ...]
    overall_result: str


@dataclass(frozen=True)
class DiagnosticStep:
    text: str


@dataclass(frozen=True)
class DoctorAdvice:
    source_check_id: str
    status: str
    severity: str
    problem: str
    meaning: str
    possible_impact: str
    evidence: tuple[str, ...]
    safe_next_steps: tuple[DiagnosticStep, ...]
    do_not: tuple[DiagnosticStep, ...]
    result: str
    limitation: str = ""

    def __post_init__(self) -> None:
        if self.result not in ALLOWED_DOCTOR_RESULTS:
            raise ValueError(f"Unsupported doctor result: {self.result}")
        if self.status not in ALLOWED_AUDIT_STATUSES:
            raise ValueError(f"Unsupported doctor source status: {self.status}")
        if self.severity not in ALLOWED_AUDIT_SEVERITIES:
            raise ValueError(f"Unsupported doctor source severity: {self.severity}")


@dataclass(frozen=True)
class DoctorFinding:
    source_check_id: str
    status: str
    severity: str
    advice: DoctorAdvice


@dataclass(frozen=True)
class DoctorReport:
    version: str
    mode: str
    scope: tuple[InventoryItem, ...]
    audit_result: str
    findings: tuple[DoctorFinding, ...]
    overall_result: str
