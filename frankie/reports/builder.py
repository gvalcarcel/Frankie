from __future__ import annotations

from datetime import datetime

from frankie.audit.audit_engine import run_audit
from frankie.core.paths import FrankiePaths
from frankie.core.status import build_status_report
from frankie.doctor.doctor_engine import run_doctor
from frankie.evidence.loader import load_structured_evidence
from frankie.evidence.summary import summarize_evidence
from frankie.inventory.inventory_reader import build_inventory_report
from frankie.reports.models import ConsolidatedReport


def build_consolidated_report(
    paths: FrankiePaths | None = None,
    generated_at: str | None = None,
) -> ConsolidatedReport:
    repository = paths or FrankiePaths.discover()
    structured = load_structured_evidence(repository)
    status = build_status_report(repository)
    inventory = build_inventory_report(repository)
    audit = run_audit(repository)
    doctor = run_doctor(structured, paths=repository)
    evidence_summary = summarize_evidence(structured)
    smb_state = _status_for(status, "Samba")
    portainer_state = _status_for(status, "Portainer")
    risks = tuple(
        f"{finding.id}: {finding.name} ({finding.status} / {finding.severity})"
        for finding in audit.findings
        if finding.status != "PASS"
    )
    next_steps = tuple(
        finding.recommendation
        for finding in audit.findings
        if finding.status != "PASS" and finding.recommendation
    )

    return ConsolidatedReport(
        version=status.version,
        mode="offline",
        generated_at=generated_at or datetime.now().astimezone().isoformat(timespec="seconds"),
        executive_summary=(
            f"Frankie Core consolidated documented evidence with overall status {status.overall_status} "
            f"and audit result {audit.overall_result}."
        ),
        overall_status=status.overall_status,
        status=status,
        inventory=inventory,
        audit=audit,
        doctor=doctor,
        evidence=structured,
        evidence_summary=evidence_summary,
        live_evidence=evidence_summary.live_evidence,
        smb_state=f"{smb_state} / PASS / INFO" if smb_state == "OK" else smb_state,
        portainer_state=f"{portainer_state} / WARN / LOW" if portainer_state == "WARNING" else portainer_state,
        known_risks=risks or ("No active non-pass audit findings are documented.",),
        limitations=(
            "Frankie physical server was not consulted during this report generation.",
            "The report is based on documented repository evidence.",
            "Sanitized LIVE evidence is historical and does not constitute a new connection.",
            "No active temporary LIVE access is documented.",
            "Repair Mode is not implemented.",
        ),
        recommended_next_steps=next_steps or ("Keep structured evidence current and validated.",),
    )


def _status_for(report, name: str) -> str:
    for section in report.sections:
        for item in section.items:
            if item.name == name:
                return item.state
    return "UNKNOWN"
