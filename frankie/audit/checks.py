from __future__ import annotations

from frankie.audit.rules import AUDIT_CHECKS
from frankie.core.models import AuditFinding
from frankie.core.paths import EVIDENCE_AUDIT_REPORT, EVIDENCE_SRV_RECURSOS, EVIDENCE_SRV_SERVICIOS, FrankiePaths


REQUIRED_STEP_5_EVIDENCE = (
    EVIDENCE_SRV_SERVICIOS,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_AUDIT_REPORT,
)


def run_checks(paths: FrankiePaths, sources_text: str) -> tuple[AuditFinding, ...]:
    checks = {check.id: check for check in AUDIT_CHECKS}
    report_text = paths.read_text(EVIDENCE_AUDIT_REPORT)
    report_normalized = (report_text or "").lower()

    return (
        _evidence_files_available(checks["AUD-EVIDENCE-001"], paths),
        _audit_report_dry_run(checks["AUD-REPORT-001"], report_text),
        _portainer_deviation(checks["AUD-SERVICES-PORTAINER-001"], report_normalized),
        _smb_validation_pending(checks["AUD-SAMBA-001"], report_normalized),
        _postgres_not_exposed(checks["AUD-POSTGRES-001"], sources_text),
        _core_read_only(checks["AUD-CORE-READONLY-001"], sources_text),
        _concepts_distinction(checks["AUD-CONCEPTS-001"], sources_text),
    )


def _evidence_files_available(check, paths: FrankiePaths) -> AuditFinding:
    missing = [relative_path for relative_path in REQUIRED_STEP_5_EVIDENCE if not paths.exists(relative_path)]
    if missing:
        return AuditFinding(
            id=check.id,
            name=check.name,
            description=check.description,
            category=check.category,
            status="MISSING_EVIDENCE",
            severity="MEDIUM",
            evidence=tuple(missing),
            message="One or more required step 5 audit evidence files are missing.",
            recommendation="Add the missing evidence files before treating repository audit data as complete.",
            limitation="This check only validates local repository files.",
        )
    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status="PASS",
        severity="INFO",
        evidence=REQUIRED_STEP_5_EVIDENCE,
        message="Required step 5 audit evidence files are available.",
        recommendation="Keep evidence files versioned only when they do not contain sensitive data.",
    )


def _audit_report_dry_run(check, report_text: str | None) -> AuditFinding:
    if report_text is None:
        return AuditFinding(
            id=check.id,
            name=check.name,
            description=check.description,
            category=check.category,
            status="UNKNOWN",
            severity="MEDIUM",
            evidence=(EVIDENCE_AUDIT_REPORT,),
            message="The audit report could not be read.",
            recommendation="Provide the documented audit report before using this check as evidence.",
        )

    normalized = report_text.lower()
    if "requiere correcciones" in normalized:
        status = "WARN"
        message = "The audit report indicates that corrections are required."
        recommendation = "Review and resolve the documented corrections before running real changes."
    elif "apto para dry-run" in normalized:
        status = "PASS"
        message = "The audit report indicates that the environment is apt for dry-run."
        recommendation = "Continue using dry-run validation before any real execution."
    else:
        status = "UNKNOWN"
        message = "The audit report does not contain a recognized decision."
        recommendation = "Add an explicit decision such as apto para dry-run or requiere correcciones."

    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status=status,
        severity="INFO" if status == "PASS" else "MEDIUM",
        evidence=(EVIDENCE_AUDIT_REPORT,),
        message=message,
        recommendation=recommendation,
    )


def _portainer_deviation(check, report_text: str) -> AuditFinding:
    if "portainer" in report_text and "8000" in report_text:
        return AuditFinding(
            id=check.id,
            name=check.name,
            description=check.description,
            category=check.category,
            status="WARN",
            severity="LOW",
            evidence=(EVIDENCE_AUDIT_REPORT,),
            message="Portainer publishes port 8000 although it is documented as not allowed by UFW.",
            recommendation="Revisar si el puerto 8000 debe mantenerse publicado o eliminarse del compose si no es necesario.",
        )
    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status="PASS",
        severity="INFO",
        evidence=(EVIDENCE_AUDIT_REPORT,),
        message="No Portainer port 8000 deviation was detected in the documented audit report.",
        recommendation="Keep Portainer exposure reviewed as Docker templates evolve.",
    )


def _smb_validation_pending(check, report_text: str) -> AuditFinding:
    windows_terms = ("windows", "smb")
    pending_terms = ("pendiente", "falta validar", "validacion smb desde cliente real pendiente")
    if any(term in report_text for term in windows_terms) and any(term in report_text for term in pending_terms):
        return AuditFinding(
            id=check.id,
            name=check.name,
            description=check.description,
            category=check.category,
            status="PENDING",
            severity="LOW",
            evidence=(EVIDENCE_AUDIT_REPORT,),
            message="SMB validation from a Windows client is still pending.",
            recommendation="Realizar validación desde un equipo Windows del aula antes de considerar Samba completamente verificado.",
        )
    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status="UNKNOWN",
        severity="LOW",
        evidence=(EVIDENCE_AUDIT_REPORT,),
        message="No explicit SMB Windows validation decision was found.",
        recommendation="Document whether Windows/SMB client validation is complete or still pending.",
    )


def _postgres_not_exposed(check, sources_text: str) -> AuditFinding:
    evidence_terms = (
        "postgresql no expone 5432",
        "5432 no escucha",
        "sin 5432",
        "not exposed on host port 5432",
    )
    if any(term in sources_text for term in evidence_terms):
        return AuditFinding(
            id=check.id,
            name=check.name,
            description=check.description,
            category=check.category,
            status="PASS",
            severity="INFO",
            evidence=(EVIDENCE_SRV_SERVICIOS, EVIDENCE_AUDIT_REPORT),
            message="Evidence indicates PostgreSQL is not exposed on host port 5432.",
            recommendation="Keep PostgreSQL reachable only through the internal Docker network unless requirements change.",
        )
    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status="UNKNOWN",
        severity="MEDIUM",
        evidence=(EVIDENCE_SRV_SERVICIOS, EVIDENCE_AUDIT_REPORT),
        message="No clear evidence was found for PostgreSQL host port 5432 exposure.",
        recommendation="Add explicit evidence about PostgreSQL port exposure.",
    )


def _core_read_only(check, sources_text: str) -> AuditFinding:
    required_terms = ("solo lectura", "read-only", "no ejecuta comandos externos", "no escribe ficheros")
    found = [term for term in required_terms if term in sources_text]
    status = "PASS" if len(found) >= 2 else "UNKNOWN"
    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status=status,
        severity="INFO" if status == "PASS" else "MEDIUM",
        evidence=("docs/frankie-core/status.md", "docs/frankie-core/inventory.md"),
        message="Frankie Core read-only behavior is documented." if status == "PASS" else "Read-only documentation evidence is incomplete.",
        recommendation="Keep read-only guarantees explicit in every command document.",
    )


def _concepts_distinction(check, sources_text: str) -> AuditFinding:
    required_terms = ("frankie core", "servidor físico", "repositorio frankie")
    found = [term for term in required_terms if term in sources_text]
    status = "PASS" if len(found) == len(required_terms) else "UNKNOWN"
    return AuditFinding(
        id=check.id,
        name=check.name,
        description=check.description,
        category=check.category,
        status=status,
        severity="INFO" if status == "PASS" else "LOW",
        evidence=("docs/frankie-core/inventory.md", "docs/evidencias/frankie-core-v0.6.0/inventory_mvp_architecture_review.md"),
        message="Documentation distinguishes Frankie, Frankie Core and the Frankie repository."
        if status == "PASS"
        else "Concept distinction is not fully documented in the local evidence.",
        recommendation="Maintain the distinction between physical server, software tool and repository in future docs.",
    )
