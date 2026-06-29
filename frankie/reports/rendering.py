from __future__ import annotations

import json

from frankie.output.json_output import (
    audit_payload,
    doctor_payload,
    evidence_summary_payload,
    inventory_payload,
    status_payload,
)
from frankie.reports.models import ConsolidatedReport


def render_report_json(report: ConsolidatedReport) -> str:
    payload = {
        "schema_version": "1.0",
        "command": "report",
        "title": "Frankie Core Consolidated Report",
        "frankie_core_version": report.version,
        "mode": report.mode,
        "generated_at": report.generated_at,
        "data_source": "documented_evidence",
        "executive_summary": report.executive_summary,
        "overall_status": report.overall_status,
        "status": status_payload(report.status, report.evidence),
        "inventory": inventory_payload(report.inventory, report.evidence),
        "audit": audit_payload(report.audit, report.evidence),
        "doctor": doctor_payload(report.doctor, report.evidence),
        "evidence": evidence_summary_payload(report.evidence_summary),
        "live_evidence": _live_evidence_payload(report),
        "known_state": {"smb": report.smb_state, "portainer": report.portainer_state},
        "known_risks": list(report.known_risks),
        "limitations": list(report.limitations),
        "recommended_next_steps": list(report.recommended_next_steps),
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_report_markdown(report: ConsolidatedReport) -> str:
    lines = [
        "# Frankie Core Consolidated Report",
        "",
        f"- Frankie Core version: `{report.version}`",
        f"- Mode: `{report.mode}`",
        f"- Generated at: `{report.generated_at}`",
        "- Data source: `documented_evidence`",
        "",
        "## Executive summary",
        "",
        report.executive_summary,
        "",
        "## Overall status",
        "",
        f"- Status: `{report.overall_status}`",
        f"- Audit: `{report.audit.overall_result}`",
        f"- Doctor: `{report.doctor.overall_result}`",
        "",
        "## Inventory summary",
        "",
    ]
    for section in report.inventory.sections:
        lines.append(f"### {section.title}")
        lines.append("")
        for item in section.items:
            lines.append(f"- **{item.name}:** {item.value} (`{item.state}`)")
        lines.append("")

    lines.extend(["## Audit findings", ""])
    for finding in report.audit.findings:
        lines.append(f"- **{finding.id}:** {finding.name} (`{finding.status} / {finding.severity}`)")
        lines.append(f"  - {finding.message}")

    lines.extend(["", "## Doctor diagnosis", ""])
    if report.doctor.findings:
        for finding in report.doctor.findings:
            lines.append(f"- **{finding.advice.issue_id}:** {finding.advice.title}")
            lines.append(f"  - Impact: {finding.advice.impact}")
            lines.append(f"  - Recommended action: {finding.advice.recommended_action}")
    else:
        lines.append("- No active diagnosis requires action.")

    summary = report.evidence_summary
    lines.extend(
        [
            "",
            "## Evidence summary",
            "",
            f"- Valid evidence: `{summary.total}`",
            f"- Invalid evidence: `{summary.invalid}`",
            f"- By status: {_inline_counts(summary.by_status)}",
            f"- By severity: {_inline_counts(summary.by_severity)}",
            f"- By mode: {_inline_counts(summary.by_mode)}",
            "",
            "## Live evidence status",
            "",
            f"- Sanitized LIVE evidence: `{report.live_evidence.total}`",
            f"- Read-only captures: `{report.live_evidence.readonly_captures}`",
            f"- Access cleanup records: `{report.live_evidence.access_cleanup}`",
            "- The LIVE capture was sanitized and made no changes.",
            "- The temporary access used for capture was removed afterwards.",
            "- No active temporary LIVE access is documented.",
            "- This report generation did not reconnect to Frankie.",
            "",
            "## Known state",
            "",
            f"- SMB: `{report.smb_state}`",
            f"- Portainer: `{report.portainer_state}`",
            "",
            "## Known risks",
            "",
        ]
    )
    lines.extend(f"- {risk}" for risk in report.known_risks)
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {limitation}" for limitation in report.limitations)
    lines.extend(["", "## Recommended next steps", ""])
    lines.extend(f"- {step}" for step in report.recommended_next_steps)
    return "\n".join(lines).rstrip()


def _inline_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"`{key}: {value}`" for key, value in counts.items())


def _live_evidence_payload(report: ConsolidatedReport) -> dict[str, object]:
    live = report.live_evidence
    return {
        "total": live.total,
        "readonly_captures": live.readonly_captures,
        "access_cleanup": live.access_cleanup,
        "server_contacted": live.server_contacted,
        "changes_made": live.changes_made,
        "changes_scope": "temporary_access_removal_only" if live.changes_made else "none",
        "capture_changes_made": False,
        "capture_sanitized": live.readonly_captures > 0,
        "temporary_access_removed": live.temporary_access_removed,
        "temporary_access_active_documented": False,
        "new_live_connection": False,
        "evidence_ids": list(live.evidence_ids),
    }
