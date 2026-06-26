from __future__ import annotations

from frankie.core.models import AuditFinding, DoctorFinding
from frankie.doctor.rules import explain_finding


RELEVANT_STATUSES = {"FAIL", "WARN", "PENDING", "UNKNOWN", "MISSING_EVIDENCE"}


def build_doctor_findings(audit_findings: tuple[AuditFinding, ...]) -> tuple[DoctorFinding, ...]:
    findings: list[DoctorFinding] = []
    for finding in audit_findings:
        if finding.status not in RELEVANT_STATUSES:
            continue
        advice = explain_finding(finding)
        findings.append(
            DoctorFinding(
                source_check_id=finding.id,
                status=finding.status,
                severity=finding.severity,
                advice=advice,
            )
        )
    return tuple(findings)
