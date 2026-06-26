from __future__ import annotations

from frankie.core.models import AuditFinding, DiagnosticStep, DoctorAdvice


def explain_finding(finding: AuditFinding) -> DoctorAdvice:
    if finding.id == "AUD-SERVICES-PORTAINER-001":
        return DoctorAdvice(
            source_check_id=finding.id,
            status=finding.status,
            severity=finding.severity,
            problem="Portainer publishes port 8000 although UFW does not allow it.",
            meaning="Docker is exposing a port that may be unnecessary or not reachable because the documented firewall policy does not allow it.",
            possible_impact="Low. This may simply be an unnecessary published port, but it should be reviewed before assuming it is harmless.",
            evidence=finding.evidence,
            safe_next_steps=(
                DiagnosticStep("Review the compose template or documented Portainer configuration."),
                DiagnosticStep("Confirm whether port 8000 is actually required."),
                DiagnosticStep("Document the decision before changing anything."),
            ),
            do_not=(
                DiagnosticStep("Do not remove the port without confirming its purpose."),
                DiagnosticStep("Do not restart Portainer during class time."),
            ),
            result="ACTIONS_RECOMMENDED",
        )

    if finding.id == "AUD-SAMBA-001":
        return DoctorAdvice(
            source_check_id=finding.id,
            status=finding.status,
            severity=finding.severity,
            problem="SMB validation from a Windows client is still pending.",
            meaning="Samba may be configured correctly, but it has not yet been validated from a real classroom client.",
            possible_impact="Students or teachers may still encounter access or permission issues when they try to use classroom shares.",
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
            result="ACTIONS_RECOMMENDED",
        )

    if finding.status in {"UNKNOWN", "MISSING_EVIDENCE"}:
        return DoctorAdvice(
            source_check_id=finding.id,
            status=finding.status,
            severity=finding.severity,
            problem="The available documentation does not provide enough evidence for a confident conclusion.",
            meaning="This may indicate missing documentation or missing evidence rather than a confirmed service failure.",
            possible_impact="Operational decisions could be made with incomplete information if the evidence gap is ignored.",
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
            result="INSUFFICIENT_EVIDENCE",
            limitation="The diagnosis depends on repository evidence and may remain incomplete until documentation catches up.",
        )

    return DoctorAdvice(
        source_check_id=finding.id,
        status=finding.status,
        severity=finding.severity,
        problem=finding.message,
        meaning="The audit finding deserves interpretation before any change is considered.",
        possible_impact="The documented deviation should be understood before acting on the system.",
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
        result="ACTIONS_RECOMMENDED" if finding.status in {"WARN", "PENDING"} else "HEALTHY",
        limitation=finding.limitation,
    )
