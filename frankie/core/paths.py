from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_MARKERS = ("README.md", "ROADMAP.md", "knowledge", "docs")


@dataclass(frozen=True)
class FrankiePaths:
    repo_root: Path | None

    @classmethod
    def discover(cls, start: Path | None = None) -> "FrankiePaths":
        current = (start or Path.cwd()).resolve()
        for candidate in (current, *current.parents):
            if all((candidate / marker).exists() for marker in REPO_MARKERS):
                return cls(candidate)
        return cls(None)

    def resolve(self, relative_path: str) -> Path | None:
        if self.repo_root is None:
            return None
        return self.repo_root / relative_path

    def exists(self, relative_path: str) -> bool:
        path = self.resolve(relative_path)
        return bool(path and path.exists())

    def read_text(self, relative_path: str) -> str | None:
        path = self.resolve(relative_path)
        if path is None or not path.exists() or not path.is_file():
            return None
        return path.read_text(encoding="utf-8", errors="replace")


EVIDENCE_SRV_SERVICIOS = "docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt"
EVIDENCE_SRV_RECURSOS = "docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt"
EVIDENCE_AUDIT_REPORT = "docs/evidencias/paso-5-auditorias/informe_auditoria.md"

STATUS_SOURCE_PATHS = (
    EVIDENCE_SRV_SERVICIOS,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_AUDIT_REPORT,
    "knowledge/SERVIDORES.md",
    "knowledge/SERVICIOS.md",
    "knowledge/DOCKER.md",
    "knowledge/SAMBA.md",
    "knowledge/BACKUPS.md",
    "docs/arquitectura.md",
)

INVENTORY_SOURCE_PATHS = (
    "knowledge/SERVIDORES.md",
    "knowledge/SERVICIOS.md",
    "knowledge/DOCKER.md",
    "knowledge/SAMBA.md",
    "knowledge/BACKUPS.md",
    "knowledge/RED.md",
    "docs/arquitectura.md",
    "docs/DOC-SRV-001_Servidor_Aula_n8n.md",
    EVIDENCE_SRV_SERVICIOS,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_AUDIT_REPORT,
    "samba/smb.conf.example",
    "samba/estructura-recursos.example.txt",
)

AUDIT_SOURCE_PATHS = (
    EVIDENCE_SRV_SERVICIOS,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_AUDIT_REPORT,
    "docs/evidencias/frankie-core-v0.6.0/status_mvp_audit.md",
    "docs/evidencias/frankie-core-v0.6.0/status_mvp_architecture_review.md",
    "docs/evidencias/frankie-core-v0.6.0/inventory_mvp_audit.md",
    "docs/evidencias/frankie-core-v0.6.0/inventory_mvp_architecture_review.md",
    "docs/frankie-core/status.md",
    "docs/frankie-core/inventory.md",
    "knowledge/SERVIDORES.md",
    "knowledge/SERVICIOS.md",
    "knowledge/DOCKER.md",
    "knowledge/SAMBA.md",
    "knowledge/BACKUPS.md",
    "knowledge/RED.md",
)
