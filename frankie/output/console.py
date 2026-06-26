from __future__ import annotations

from frankie.core.models import AuditReport, InventoryReport, StatusReport


def render_status(report: StatusReport) -> str:
    lines = [
        "Frankie Status",
        f"Version: {report.version}",
        f"Mode: {report.mode}",
        "",
    ]

    for section in report.sections:
        lines.append(f"{section.title}:")
        for item in section.items:
            lines.append(f"  {_format_item(item.name, item.state)}")
        lines.append("")

    lines.append(f"Overall status: {report.overall_status}")
    return "\n".join(lines).rstrip()


def render_inventory(report: InventoryReport) -> str:
    lines = [
        "Frankie Inventory",
        f"Version: {report.version}",
        f"Mode: {report.mode}",
        "",
    ]

    for section in report.sections:
        lines.append(f"{section.title}:")
        for item in section.items:
            lines.append(f"  {_format_item(item.name, item.value)}")
            if item.state != "KNOWN":
                lines.append(f"    State: {item.state}")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_audit(report: AuditReport, verbose: bool = False) -> str:
    lines = [
        "Frankie Audit",
        f"Version: {report.version}",
        f"Mode: {report.mode}",
        "",
        "Scope:",
    ]

    for item in report.scope:
        lines.append(f"  {_format_item(item.name, item.value)}")

    lines.extend(["", "Summary:"])
    summary = _audit_summary(report)
    lines.append(f"  {_format_item('Checks total', str(len(report.findings)))}")
    for status in ("PASS", "WARN", "PENDING", "UNKNOWN", "MISSING_EVIDENCE", "FAIL"):
        lines.append(f"  {_format_item(status, str(summary.get(status, 0)))}")

    lines.extend(["", "Findings:"])
    for finding in report.findings:
        lines.append("")
        lines.append(f"[{finding.status}] {finding.id}")
        lines.append(f"  {finding.name}")
        lines.append(f"  Severity: {finding.severity}")
        lines.append("  Message:")
        lines.append(f"    {finding.message}")

        if verbose:
            lines.append("  Category:")
            lines.append(f"    {finding.category}")
            lines.append("  Description:")
            lines.append(f"    {finding.description}")

        lines.append("  Evidence:")
        for evidence in finding.evidence:
            lines.append(f"    {evidence}")

        if verbose or finding.status != "PASS":
            lines.append("  Recommendation:")
            lines.append(f"    {finding.recommendation}")
            if finding.limitation:
                lines.append("  Limitation:")
                lines.append(f"    {finding.limitation}")

    lines.extend(["", f"Overall audit result: {report.overall_result}"])
    return "\n".join(lines).rstrip()


def _audit_summary(report: AuditReport) -> dict[str, int]:
    summary: dict[str, int] = {}
    for finding in report.findings:
        summary[finding.status] = summary.get(finding.status, 0) + 1
    return summary


def _format_item(name: str, state: str) -> str:
    width = 30
    if len(name) >= width:
        return f"{name} {state}"
    dots = "." * (width - len(name))
    return f"{name}{dots} {state}"
