from __future__ import annotations

from frankie.core.models import AuditReport, DoctorReport, InventoryReport, StatusReport


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


def render_doctor(report: DoctorReport, verbose: bool = False) -> str:
    lines = [
        "Frankie Doctor",
        f"Version: {report.version}",
        f"Mode: {report.mode}",
        "",
        "Scope:",
    ]

    for item in report.scope:
        lines.append(f"  {_format_item(item.name, item.value)}")

    lines.extend(
        [
            "",
            "Diagnosis summary:",
            f"  {_format_item('Audit result', report.audit_result)}",
            f"  {_format_item('Issues reviewed', str(len(report.findings)))}",
            f"  {_format_item('Critical issues', str(sum(1 for f in report.findings if f.severity in {'HIGH', 'CRITICAL'} and f.status == 'FAIL')))}",
            f"  {_format_item('Safe to continue', 'yes' if report.overall_result != 'CRITICAL' else 'no')}",
            "",
            "Findings explained:",
        ]
    )

    if not report.findings:
        lines.extend(
            [
                "",
                "No non-pass findings require explanation.",
                "",
                f"Overall doctor result: {report.overall_result}",
            ]
        )
        return "\n".join(lines).rstrip()

    for finding in report.findings:
        advice = finding.advice
        lines.append("")
        lines.append(f"Issue: {advice.issue_id}")
        lines.append(f"  Title: {advice.title}")
        lines.append(f"  Severity: {advice.severity}")
        lines.append(f"  Urgency: {advice.urgency}")
        lines.append("")
        lines.append("  Impact:")
        lines.append(f"    {advice.impact}")
        lines.append("")
        lines.append("  Why it matters:")
        lines.append(f"    {advice.why_it_matters}")
        lines.append("")
        lines.append("  Recommended action:")
        lines.append(f"    {advice.recommended_action}")
        lines.append("")
        lines.append("  Safe next steps:")
        for idx, step in enumerate(advice.safe_next_steps, start=1):
            lines.append(f"    {idx}. {step.text}")
        lines.append("")
        lines.append("  Do not:")
        for step in advice.do_not:
            lines.append(f"    - {step.text}")
        lines.append("")
        lines.append("  Student explanation:")
        lines.append(f"    {advice.student_explanation}")
        lines.append("")
        lines.append("  Evidence:")
        for evidence in advice.evidence:
            lines.append(f"    {evidence}")

        if verbose:
            lines.append("")
            lines.append("  Audit check:")
            lines.append(f"    {advice.issue_id}")
            lines.append("  Status and severity:")
            lines.append(f"    {finding.status} / {finding.severity}")
            lines.append("  Result:")
            lines.append(f"    {advice.result}")
            lines.append("  Why no automatic repair:")
            lines.append("    Frankie Doctor MVP is diagnostic only and does not modify systems.")
            if advice.limitation:
                lines.append("  Limitation:")
                lines.append(f"    {advice.limitation}")

    if verbose and report.resolved_checks:
        lines.extend(["", "Resolved checks not requiring action:"])
        for check in report.resolved_checks:
            lines.append(f"  - {check}")

    lines.extend(["", f"Overall doctor result: {report.overall_result}"])
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
