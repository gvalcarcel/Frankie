from __future__ import annotations

from frankie.core.models import AuditFinding, DiagnosticStep, DoctorAdvice


def explain_finding(finding: AuditFinding) -> DoctorAdvice:
    if finding.id == "AUD-SERVICES-PORTAINER-001":
        return DoctorAdvice(
            issue_id=finding.id,
            title="Portainer port 8000 remains published",
            status=finding.status,
            severity=finding.severity,
            urgency="LOW",
            impact="Portainer is documented as exposing port 8000 in addition to its main access port.",
            why_it_matters="Published ports increase the surface that should be reviewed, even when the documented risk is low.",
            recommended_action="Review the port exposure in a future explicitly authorized LIVE Work Order.",
            evidence=finding.evidence,
            safe_next_steps=(
                DiagnosticStep("Confirm the current Docker port mapping in a read-only LIVE check."),
                DiagnosticStep("Review the documented UFW and firewall rules before changing anything."),
                DiagnosticStep("Document the decision to keep or close the port, including rollback steps."),
            ),
            do_not=(
                DiagnosticStep("Do not stop or restart Portainer from an offline Work Order."),
                DiagnosticStep("Do not remove Docker port mappings without a backup and rollback plan."),
                DiagnosticStep("Do not change firewall rules without explicit authorization."),
            ),
            student_explanation="It is like finding an extra open door in a computer room. It may be intentional, but we should check why it is open before changing it.",
            result="ACTIONS_RECOMMENDED",
        )

    if finding.id == "AUD-SAMBA-001":
        return DoctorAdvice(
            issue_id=finding.id,
            title="SMB client validation is pending",
            status=finding.status,
            severity=finding.severity,
            urgency="MEDIUM",
            impact="Students or teachers may encounter access or permission issues when they use classroom shares.",
            why_it_matters="A server-side configuration is not fully validated until a real classroom client can use it with the expected permissions.",
            recommended_action="Validate the documented shares from a classroom client during an authorized LIVE Work Order.",
            evidence=finding.evidence,
            safe_next_steps=(
                DiagnosticStep("Test access from a Windows classroom computer."),
                DiagnosticStep("Validate alumno and profesor permissions."),
                DiagnosticStep("Record the result as new evidence."),
            ),
            do_not=(
                DiagnosticStep("Do not change Samba configuration before testing from a real client."),
                DiagnosticStep("Do not treat this pending validation as a confirmed technical failure."),
            ),
            student_explanation="A shared folder is only ready when both the server and a classroom computer agree that access works as expected.",
            result="ACTIONS_RECOMMENDED",
        )

    if finding.status in {"UNKNOWN", "MISSING_EVIDENCE"}:
        return DoctorAdvice(
            issue_id=finding.id,
            title="Insufficient documented evidence",
            status=finding.status,
            severity=finding.severity,
            urgency="MEDIUM",
            impact="Operational decisions could be made with incomplete information if the evidence gap is ignored.",
            why_it_matters="Missing evidence is not the same as a broken service, but it prevents a confident technical conclusion.",
            recommended_action="Obtain or update the missing evidence before proposing a configuration change.",
            evidence=finding.evidence,
            safe_next_steps=(
                DiagnosticStep("Locate the missing evidence or generate it through the documented audit process."),
                DiagnosticStep("Update the repository evidence before escalating the issue."),
                DiagnosticStep("Re-run the read-only commands after evidence is available."),
            ),
            do_not=(
                DiagnosticStep("Do not conclude that the service is broken only because evidence is missing."),
                DiagnosticStep("Do not apply corrective changes without confirming the real state first."),
            ),
            student_explanation="If a worksheet has an empty answer, we cannot assume the answer is wrong. We first need the missing information.",
            result="INSUFFICIENT_EVIDENCE",
            limitation="The diagnosis depends on repository evidence and may remain incomplete until documentation catches up.",
        )

    return DoctorAdvice(
        issue_id=finding.id,
        title=finding.name,
        status=finding.status,
        severity=finding.severity,
        urgency=_urgency(finding),
        impact="The documented deviation should be understood before acting on the system.",
        why_it_matters="An audit finding is evidence to review, not permission to change a server.",
        recommended_action=finding.recommendation or "Review the evidence before deciding whether action is needed.",
        evidence=finding.evidence,
        safe_next_steps=(
            DiagnosticStep("Review the referenced evidence in the repository."),
            DiagnosticStep("Confirm whether the finding is still current."),
            DiagnosticStep("Document any additional evidence before proposing changes."),
        ),
        do_not=(
            DiagnosticStep("Do not jump directly from finding to repair."),
            DiagnosticStep("Do not treat repository evidence as live telemetry."),
        ),
        student_explanation="Think of an audit finding as a warning note: read the evidence and understand it before touching the system.",
        result="ACTIONS_RECOMMENDED" if finding.status in {"WARN", "PENDING"} else "HEALTHY",
        limitation=finding.limitation,
    )


def _urgency(finding: AuditFinding) -> str:
    if finding.severity == "CRITICAL":
        return "IMMEDIATE"
    if finding.severity == "HIGH" or finding.status == "FAIL":
        return "HIGH"
    if finding.severity == "MEDIUM" or finding.status in {"PENDING", "UNKNOWN", "MISSING_EVIDENCE"}:
        return "MEDIUM"
    if finding.severity == "LOW" or finding.status == "WARN":
        return "LOW"
    return "INFO"
