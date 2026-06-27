from __future__ import annotations

from frankie.audit.audit_engine import run_audit
from frankie.core.models import DoctorReport, InventoryItem
from frankie.doctor.advice import build_doctor_findings
from frankie.evidence.loader import load_structured_evidence


def run_doctor() -> DoctorReport:
    audit_report = run_audit()
    structured = load_structured_evidence()
    findings = build_doctor_findings(audit_report.findings)
    return DoctorReport(
        version=audit_report.version,
        mode=audit_report.mode,
        scope=(
            InventoryItem("Source", "audit engine"),
            InventoryItem("Live connection", "no"),
            InventoryItem("Repairs", "no"),
            InventoryItem("Writes files", "no"),
            InventoryItem("Executes commands", "no"),
            InventoryItem("Structured evidence", f"{len(structured.evidence)} loaded" if structured.available else "unavailable"),
            InventoryItem("Evidence issues", str(len(structured.issues))),
        ),
        audit_result=audit_report.overall_result,
        findings=findings,
        overall_result=_overall_result(findings, audit_report.overall_result),
        resolved_checks=tuple(f"{finding.id} (PASS; no active action)" for finding in audit_report.findings if finding.status == "PASS"),
    )


def _overall_result(findings, audit_result: str) -> str:
    if any(f.status == "FAIL" and f.severity in {"HIGH", "CRITICAL"} for f in findings):
        return "CRITICAL"
    if all(f.status == "PASS" for f in findings) and audit_result == "PASS":
        return "HEALTHY"
    insufficient = sum(1 for f in findings if f.status in {"UNKNOWN", "MISSING_EVIDENCE"})
    if findings and insufficient > len(findings) / 2:
        return "INSUFFICIENT_EVIDENCE"
    if any(f.status in {"FAIL", "WARN"} for f in findings):
        return "ACTIONS_RECOMMENDED"
    if any(f.status in {"PENDING", "UNKNOWN", "MISSING_EVIDENCE"} for f in findings):
        return "ACTIONS_RECOMMENDED"
    return "HEALTHY"
