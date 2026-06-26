from __future__ import annotations

from frankie.core.constants import MODE, VERSION
from frankie.core.models import StatusItem, StatusReport, StatusSection
from frankie.core.paths import (
    EVIDENCE_AUDIT_REPORT,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_SRV_SERVICIOS,
    FrankiePaths,
)


def build_status_report(paths: FrankiePaths | None = None) -> StatusReport:
    repo_paths = paths or FrankiePaths.discover()
    audit_report = repo_paths.read_text(EVIDENCE_AUDIT_REPORT)
    audit_report_normalized = _normalize(audit_report or "")

    servicios_evidence = _evidence_state(repo_paths, EVIDENCE_SRV_SERVICIOS)
    recursos_evidence = _evidence_state(repo_paths, EVIDENCE_SRV_RECURSOS)
    report_evidence = _evidence_state(repo_paths, EVIDENCE_AUDIT_REPORT)

    audit_report_state = _audit_report_state(audit_report_normalized, report_evidence.state)
    portainer_state = _portainer_state(audit_report_normalized)
    samba_state = _samba_state(audit_report_normalized, recursos_evidence.state)
    smb_validation_state = _windows_smb_validation_state(audit_report_normalized)
    postgres_exposure_state = _postgres_exposure_state(audit_report_normalized)

    sections = (
        StatusSection(
            "Physical server",
            (
                StatusItem("Frankie", _documented_state(repo_paths, "docs/arquitectura.md")),
            ),
        ),
        StatusSection(
            "Virtual machines",
            (
                StatusItem("srv-servicios", _vm_state(servicios_evidence.state, audit_report_state)),
                StatusItem("srv-recursos", _vm_state(recursos_evidence.state, samba_state)),
            ),
        ),
        StatusSection(
            "Core services",
            (
                StatusItem("Docker", _ok_if_evidence(servicios_evidence.state)),
                StatusItem("Portainer", portainer_state),
                StatusItem("PostgreSQL", _ok_if_evidence(servicios_evidence.state)),
                StatusItem("n8n", _ok_if_evidence(servicios_evidence.state)),
                StatusItem("Samba", samba_state),
            ),
        ),
        StatusSection(
            "Security",
            (
                StatusItem("UFW", _security_state(servicios_evidence.state, recursos_evidence.state)),
                StatusItem("Fail2ban", _ok_if_evidence(servicios_evidence.state)),
                StatusItem("PostgreSQL exposure", postgres_exposure_state),
            ),
        ),
        StatusSection(
            "Backups",
            (
                StatusItem("srv-servicios backups", _services_backup_state(audit_report_normalized)),
                StatusItem("srv-recursos backups", "UNKNOWN"),
            ),
        ),
        StatusSection(
            "Evidence",
            (
                StatusItem("srv-servicios audit", servicios_evidence.state),
                StatusItem("srv-recursos audit", recursos_evidence.state),
                StatusItem("Audit report", audit_report_state),
                StatusItem("Windows/SMB validation", smb_validation_state),
            ),
        ),
    )

    return StatusReport(
        version=VERSION,
        mode=MODE,
        sections=sections,
        overall_status=_overall_status(sections),
    )


def _normalize(value: str) -> str:
    return value.lower()


def _evidence_state(paths: FrankiePaths, relative_path: str) -> StatusItem:
    if paths.exists(relative_path):
        return StatusItem(relative_path, "OK")
    return StatusItem(relative_path, "MISSING EVIDENCE")


def _documented_state(paths: FrankiePaths, relative_path: str) -> str:
    return "OK" if paths.exists(relative_path) else "UNKNOWN"


def _audit_report_state(report: str, evidence_state: str) -> str:
    if evidence_state == "MISSING EVIDENCE":
        return "MISSING EVIDENCE"
    if "requiere correcciones" in report:
        return "WARNING"
    if "apto para dry-run" in report:
        return "OK"
    return "UNKNOWN"


def _portainer_state(report: str) -> str:
    if "portainer" in report and "8000" in report:
        return "WARNING"
    return "OK" if "portainer" in report else "UNKNOWN"


def _samba_state(report: str, recursos_evidence_state: str) -> str:
    if _has_pending_windows_smb_validation(report):
        return "WARNING"
    return _ok_if_evidence(recursos_evidence_state)


def _windows_smb_validation_state(report: str) -> str:
    if _has_pending_windows_smb_validation(report):
        return "PENDING"
    return "UNKNOWN"


def _has_pending_windows_smb_validation(report: str) -> bool:
    return (
        ("windows" in report and "smb" in report and "pendiente" in report)
        or ("cliente windows" in report and "samba" in report)
        or ("validacion smb" in report and "pendiente" in report)
        or ("validación smb" in report and "pendiente" in report)
    )


def _postgres_exposure_state(report: str) -> str:
    if "postgresql no expone" in report or "5432 no escucha" in report or "sin 5432" in report:
        return "OK"
    if "5432" in report and "expuesto" in report:
        return "ERROR"
    return "UNKNOWN"


def _services_backup_state(report: str) -> str:
    if "backups existentes" in report or "cron diario" in report or "cron 02:00" in report:
        return "OK"
    return "UNKNOWN"


def _security_state(servicios_state: str, recursos_state: str) -> str:
    if servicios_state == "OK" and recursos_state == "OK":
        return "OK"
    if "MISSING EVIDENCE" in (servicios_state, recursos_state):
        return "MISSING EVIDENCE"
    return "UNKNOWN"


def _ok_if_evidence(evidence_state: str) -> str:
    if evidence_state == "OK":
        return "OK"
    if evidence_state == "MISSING EVIDENCE":
        return "MISSING EVIDENCE"
    return "UNKNOWN"


def _vm_state(evidence_state: str, related_state: str) -> str:
    if evidence_state == "MISSING EVIDENCE":
        return "MISSING EVIDENCE"
    if related_state in ("WARNING", "PENDING"):
        return "WARNING"
    if related_state == "ERROR":
        return "ERROR"
    return "OK"


def _overall_status(sections: tuple[StatusSection, ...]) -> str:
    states = [item.state for section in sections for item in section.items]
    for state in ("ERROR", "WARNING", "MISSING EVIDENCE", "UNKNOWN", "PENDING"):
        if state in states:
            return state
    return "OK"
