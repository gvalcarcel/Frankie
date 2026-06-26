from __future__ import annotations

from frankie.audit.checks import run_checks
from frankie.core.constants import MODE, VERSION
from frankie.core.models import AuditReport, AuditSource, InventoryItem
from frankie.core.paths import AUDIT_SOURCE_PATHS, FrankiePaths


AUDIT_RESULT_PRIORITY = ("FAIL", "WARN", "PENDING", "UNKNOWN", "MISSING_EVIDENCE", "PASS")


def run_audit(paths: FrankiePaths | None = None) -> AuditReport:
    repository = paths or FrankiePaths.discover()
    sources = tuple(AuditSource(path=relative_path, available=repository.exists(relative_path)) for relative_path in AUDIT_SOURCE_PATHS)
    sources_text = _read_sources(repository)
    findings = run_checks(repository, sources_text)

    return AuditReport(
        version=VERSION,
        mode=MODE,
        scope=(
            InventoryItem("Source", "repository evidence"),
            InventoryItem("Live connection", "no"),
            InventoryItem("Writes files", "no"),
            InventoryItem("Executes commands", "no"),
        ),
        sources=sources,
        findings=findings,
        overall_result=_overall_result(findings),
    )


def _read_sources(paths: FrankiePaths) -> str:
    contents: list[str] = []
    for relative_path in AUDIT_SOURCE_PATHS:
        text = paths.read_text(relative_path)
        if text:
            contents.append(text.lower())
    return "\n".join(contents)


def _overall_result(findings) -> str:
    statuses = {finding.status for finding in findings}
    for status in AUDIT_RESULT_PRIORITY:
        if status in statuses:
            return status
    return "UNKNOWN"
