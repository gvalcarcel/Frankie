from __future__ import annotations

import json
import re

from frankie.core.models import AuditReport, DoctorReport, InventoryReport, StatusReport
from frankie.evidence.models import EvidenceLoadResult, EvidenceSummary, StructuredEvidence


SCHEMA_VERSION = "1.0"
DATA_SOURCE = "documented_evidence"


def render_status_json(report: StatusReport, structured: EvidenceLoadResult | None = None) -> str:
    return _render_json(status_payload(report, structured))


def render_audit_json(
    report: AuditReport,
    structured: EvidenceLoadResult | None = None,
    verbose: bool = False,
) -> str:
    return _render_json(audit_payload(report, structured, verbose=verbose))


def render_inventory_json(report: InventoryReport, structured: EvidenceLoadResult | None = None) -> str:
    return _render_json(inventory_payload(report, structured))


def render_doctor_json(
    report: DoctorReport,
    structured: EvidenceLoadResult | None = None,
    verbose: bool = False,
) -> str:
    return _render_json(doctor_payload(report, structured, verbose=verbose))


def render_evidence_json(evidence: StructuredEvidence) -> str:
    return _render_json(evidence_payload(evidence))


def render_evidence_summary_json(summary: EvidenceSummary) -> str:
    return _render_json(evidence_summary_payload(summary))


def status_payload(
    report: StatusReport, structured: EvidenceLoadResult | None = None
) -> dict[str, object]:
    components: list[dict[str, object]] = []
    for section in report.sections:
        for item in section.items:
            component: dict[str, object] = {
                "id": _identifier(item.name),
                "section": _identifier(section.title),
                "name": item.name,
                "status": item.state,
                "severity": _status_severity(item.state),
                "message": item.detail or f"Documented status for {item.name}: {item.state}.",
            }
            components.append(component)

    return {
        "schema_version": SCHEMA_VERSION,
        "command": "status",
        "frankie_core_version": report.version,
        "mode": "offline",
        "data_source": _data_source(structured),
        "structured_evidence": _structured_metadata(structured),
        "overall_status": report.overall_status,
        "summary": f"Frankie documented status is {report.overall_status}.",
        "components": components,
    }


def audit_payload(
    report: AuditReport,
    structured: EvidenceLoadResult | None = None,
    verbose: bool = False,
) -> dict[str, object]:
    counts = {status.lower(): 0 for status in ("PASS", "WARN", "PENDING", "FAIL", "UNKNOWN", "MISSING_EVIDENCE")}
    checks: list[dict[str, object]] = []

    for finding in report.findings:
        counts[finding.status.lower()] = counts.get(finding.status.lower(), 0) + 1
        check: dict[str, object] = {
            "id": finding.id,
            "status": finding.status,
            "severity": finding.severity,
            "title": finding.name,
            "message": finding.message,
            "evidence": list(finding.evidence),
            "recommendation": finding.recommendation,
        }
        if verbose:
            check.update(
                {
                    "category": finding.category,
                    "description": finding.description,
                    "limitation": finding.limitation or None,
                }
            )
        checks.append(check)

    return {
        "schema_version": SCHEMA_VERSION,
        "command": "audit",
        "frankie_core_version": report.version,
        "mode": "offline",
        "data_source": _data_source(structured),
        "structured_evidence": _structured_metadata(structured),
        "overall_result": report.overall_result,
        "counts": {"total": len(report.findings), **counts},
        "checks": checks,
    }


def inventory_payload(
    report: InventoryReport, structured: EvidenceLoadResult | None = None
) -> dict[str, object]:
    items: list[dict[str, object]] = []
    for section in report.sections:
        for item in section.items:
            items.append(
                {
                    "id": _identifier(f"{section.title}_{item.name}"),
                    "section": _identifier(section.title),
                    "name": item.name,
                    "value": item.value,
                    "state": item.state,
                }
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "command": "inventory",
        "frankie_core_version": report.version,
        "mode": "offline",
        "data_source": _data_source(structured),
        "structured_evidence": _structured_metadata(structured),
        "items": items,
    }


def doctor_payload(
    report: DoctorReport,
    structured: EvidenceLoadResult | None = None,
    verbose: bool = False,
) -> dict[str, object]:
    issues: list[dict[str, object]] = []
    for finding in report.findings:
        advice = finding.advice
        issue: dict[str, object] = {
            "issue_id": advice.issue_id,
            "title": advice.title,
            "status": finding.status,
            "severity": advice.severity,
            "urgency": advice.urgency,
            "impact": advice.impact,
            "why_it_matters": advice.why_it_matters,
            "recommended_action": advice.recommended_action,
            "safe_next_steps": [step.text for step in advice.safe_next_steps],
            "do_not": [step.text for step in advice.do_not],
            "student_explanation": advice.student_explanation,
            "evidence": list(advice.evidence),
        }
        if verbose:
            issue.update(
                {
                    "result": advice.result,
                    "limitation": advice.limitation or None,
                }
            )
        issues.append(issue)

    payload: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "command": "doctor",
        "frankie_core_version": report.version,
        "mode": "offline",
        "data_source": _data_source(structured),
        "structured_evidence": _structured_metadata(structured),
        "overall_diagnosis": report.overall_result,
        "audit_result": report.audit_result,
        "issues_reviewed": len(report.findings),
        "issues": issues,
    }
    if verbose:
        payload["resolved_checks"] = list(report.resolved_checks)
    return payload


def evidence_payload(evidence: StructuredEvidence) -> dict[str, object]:
    return {
        "schema_version": evidence.schema_version,
        "evidence_id": evidence.evidence_id,
        "evidence_type": evidence.evidence_type,
        "component": {"id": evidence.component_id, "name": evidence.component_name},
        "status": evidence.status,
        "severity": evidence.severity,
        "mode": evidence.mode,
        "data_source": evidence.data_source,
        "summary": evidence.summary,
        "details": evidence.details,
        "references": list(evidence.references),
        "server_impact": evidence.server_impact,
        "security": evidence.security,
        "recommendation": evidence.recommendation,
        "created_at": evidence.created_at,
        "updated_at": evidence.updated_at,
        "source_files": list(evidence.source_files),
        "related_checks": list(evidence.related_checks),
    }


def evidence_summary_payload(summary: EvidenceSummary) -> dict[str, object]:
    live = summary.live_evidence
    return {
        "schema_version": SCHEMA_VERSION,
        "command": "evidence summary",
        "mode": "offline",
        "total": summary.total,
        "invalid": summary.invalid,
        "by_status": summary.by_status,
        "by_severity": summary.by_severity,
        "by_component": summary.by_component,
        "by_evidence_type": summary.by_evidence_type,
        "by_data_source": summary.by_data_source,
        "by_mode": summary.by_mode,
        "live_evidence": {
            "total": live.total,
            "readonly_captures": live.readonly_captures,
            "access_cleanup": live.access_cleanup,
            "server_contacted": live.server_contacted,
            "changes_made": live.changes_made,
            "temporary_access_removed": live.temporary_access_removed,
            "evidence_ids": list(live.evidence_ids),
        },
    }


def _render_json(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _data_source(structured: EvidenceLoadResult | None) -> str:
    if structured and structured.available:
        return "structured_and_documented_evidence"
    return DATA_SOURCE


def _structured_metadata(structured: EvidenceLoadResult | None) -> dict[str, object]:
    if structured is None:
        return {"available": False, "path": None, "loaded": 0, "issues": 0}
    return {
        "available": structured.available,
        "path": structured.directory,
        "loaded": len(structured.evidence),
        "issues": len(structured.issues),
    }


def _identifier(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return normalized or "unknown"


def _status_severity(status: str) -> str:
    return {
        "OK": "INFO",
        "WARNING": "LOW",
        "PENDING": "MEDIUM",
        "UNKNOWN": "MEDIUM",
        "MISSING EVIDENCE": "MEDIUM",
        "ERROR": "HIGH",
    }.get(status, "MEDIUM")
