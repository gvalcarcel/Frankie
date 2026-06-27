from __future__ import annotations

import json
import re

from frankie.core.models import AuditReport, StatusReport
from frankie.evidence.models import EvidenceLoadResult


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
