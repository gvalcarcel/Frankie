from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from frankie.core.paths import FrankiePaths
from frankie.evidence.models import EvidenceLoadIssue, EvidenceLoadResult, StructuredEvidence


STRUCTURED_EVIDENCE_DIRECTORY = "docs/evidencias/structured"
REQUIRED_FIELDS = (
    "schema_version",
    "evidence_id",
    "evidence_type",
    "component",
    "status",
    "severity",
    "mode",
    "data_source",
    "summary",
    "references",
    "server_impact",
    "security",
    "recommendation",
)
REQUIRED_SERVER_IMPACT_FIELDS = (
    "touches_physical_server",
    "requires_live_connection",
    "changes_configuration",
)
REQUIRED_SECURITY_FIELDS = (
    "contains_secrets",
    "contains_credentials",
    "contains_internal_ips",
)


def load_structured_evidence(paths: FrankiePaths | None = None) -> EvidenceLoadResult:
    repository = paths or FrankiePaths.discover()
    directory = repository.resolve(STRUCTURED_EVIDENCE_DIRECTORY)
    if directory is None or not directory.is_dir():
        return EvidenceLoadResult(False, STRUCTURED_EVIDENCE_DIRECTORY, (), ())

    evidence: list[StructuredEvidence] = []
    issues: list[EvidenceLoadIssue] = []
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            evidence.append(_parse_evidence(payload))
        except (json.JSONDecodeError, OSError, TypeError, ValueError) as exc:
            issues.append(EvidenceLoadIssue(_relative_path(path, repository), str(exc)))

    return EvidenceLoadResult(
        directory_available=True,
        directory=STRUCTURED_EVIDENCE_DIRECTORY,
        evidence=tuple(evidence),
        issues=tuple(issues),
    )


def _parse_evidence(payload: Any) -> StructuredEvidence:
    if not isinstance(payload, dict):
        raise ValueError("evidence root must be an object")
    missing = [field for field in REQUIRED_FIELDS if field not in payload]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    component = _required_object(payload, "component")
    component_id = _required_string(component, "id")
    component_name = _required_string(component, "name")
    references = payload["references"]
    if not isinstance(references, list) or not all(isinstance(item, str) and item for item in references):
        raise ValueError("references must be a list of non-empty strings")

    server_impact = _required_boolean_map(payload, "server_impact", REQUIRED_SERVER_IMPACT_FIELDS)
    security = _required_boolean_map(payload, "security", REQUIRED_SECURITY_FIELDS)
    if any(security.values()):
        raise ValueError("public structured evidence must not contain sensitive data")

    details = payload.get("details", {})
    if not isinstance(details, dict):
        raise ValueError("details must be an object")

    return StructuredEvidence(
        schema_version=_required_string(payload, "schema_version"),
        evidence_id=_required_string(payload, "evidence_id"),
        evidence_type=_required_string(payload, "evidence_type"),
        component_id=component_id,
        component_name=component_name,
        status=_required_string(payload, "status"),
        severity=_required_string(payload, "severity"),
        mode=_required_string(payload, "mode"),
        data_source=_required_string(payload, "data_source"),
        summary=_required_string(payload, "summary"),
        details=details,
        references=tuple(references),
        server_impact=server_impact,
        security=security,
        recommendation=_required_string(payload, "recommendation"),
    )


def _required_object(payload: dict[str, Any], field: str) -> dict[str, Any]:
    value = payload[field]
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    return value


def _required_string(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _required_boolean_map(
    payload: dict[str, Any], field: str, required_fields: tuple[str, ...]
) -> dict[str, bool]:
    value = _required_object(payload, field)
    missing = [name for name in required_fields if name not in value]
    if missing:
        raise ValueError(f"{field} missing fields: {', '.join(missing)}")
    if not all(isinstance(value[name], bool) for name in required_fields):
        raise ValueError(f"{field} fields must be boolean")
    return {name: value[name] for name in required_fields}


def _relative_path(path: Path, repository: FrankiePaths) -> str:
    if repository.repo_root is None:
        return path.name
    return path.relative_to(repository.repo_root).as_posix()
