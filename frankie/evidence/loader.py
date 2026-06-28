from __future__ import annotations

import json
import re
from datetime import datetime
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
ALLOWED_STATUSES = {
    "ACTIVE",
    "ERROR",
    "FAIL",
    "OK",
    "PASS",
    "PENDING",
    "RELEASED",
    "UNKNOWN",
    "WARN",
    "WARNING",
}
ALLOWED_SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_MODES = {"offline", "live"}
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\b(?:password|secret|token|client_secret|smtp_password|private_key|credential)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\b10(?:\.\d{1,3}){3}\b"),
    re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b"),
)


def load_structured_evidence(paths: FrankiePaths | None = None) -> EvidenceLoadResult:
    repository = paths or FrankiePaths.discover()
    directory = repository.resolve(STRUCTURED_EVIDENCE_DIRECTORY)
    if directory is None or not directory.is_dir():
        return EvidenceLoadResult(False, STRUCTURED_EVIDENCE_DIRECTORY, (), ())

    evidence: list[StructuredEvidence] = []
    issues: list[EvidenceLoadIssue] = []
    evidence_paths: dict[str, str] = {}
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            parsed = _parse_evidence(payload)
            relative_path = _relative_path(path, repository)
            if parsed.evidence_id in evidence_paths:
                issues.append(
                    EvidenceLoadIssue(
                        relative_path,
                        f"duplicate evidence_id: {parsed.evidence_id} (first seen in {evidence_paths[parsed.evidence_id]})",
                    )
                )
                continue
            evidence_paths[parsed.evidence_id] = relative_path
            evidence.append(parsed)
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
    if not isinstance(references, list) or not references or not all(isinstance(item, str) and item for item in references):
        raise ValueError("references must be a non-empty list of non-empty strings")

    server_impact = _required_boolean_map(payload, "server_impact", REQUIRED_SERVER_IMPACT_FIELDS)
    security = _required_boolean_map(payload, "security", REQUIRED_SECURITY_FIELDS)
    if any(security.values()):
        raise ValueError("public structured evidence must not contain sensitive data")

    status = _required_string(payload, "status")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"unsupported status: {status}")
    severity = _required_string(payload, "severity")
    if severity not in ALLOWED_SEVERITIES:
        raise ValueError(f"unsupported severity: {severity}")
    mode = _required_string(payload, "mode")
    if mode not in ALLOWED_MODES:
        raise ValueError(f"unsupported mode: {mode}")

    created_at = _optional_timestamp(payload, "created_at")
    updated_at = _optional_timestamp(payload, "updated_at")
    source_files = _optional_string_list(payload, "source_files")
    related_checks = _optional_string_list(payload, "related_checks")

    if _contains_sensitive_value(payload):
        raise ValueError("possible sensitive data detected in evidence values")

    details = payload.get("details", {})
    if not isinstance(details, dict):
        raise ValueError("details must be an object")

    return StructuredEvidence(
        schema_version=_required_string(payload, "schema_version"),
        evidence_id=_required_string(payload, "evidence_id"),
        evidence_type=_required_string(payload, "evidence_type"),
        component_id=component_id,
        component_name=component_name,
        status=status,
        severity=severity,
        mode=mode,
        data_source=_required_string(payload, "data_source"),
        summary=_required_string(payload, "summary"),
        details=details,
        references=tuple(references),
        server_impact=server_impact,
        security=security,
        recommendation=_required_string(payload, "recommendation"),
        created_at=created_at,
        updated_at=updated_at,
        source_files=source_files,
        related_checks=related_checks,
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


def _optional_string_list(payload: dict[str, Any], field: str) -> tuple[str, ...]:
    value = payload.get(field, [])
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{field} must be a list of non-empty strings")
    return tuple(value)


def _optional_timestamp(payload: dict[str, Any], field: str) -> str | None:
    value = payload.get(field)
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty ISO 8601 string")
    try:
        normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
        datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO 8601 timestamp") from exc
    return value


def _contains_sensitive_value(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_sensitive_value(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_sensitive_value(item) for item in value)
    if not isinstance(value, str):
        return False
    return any(pattern.search(value) for pattern in SENSITIVE_VALUE_PATTERNS)


def _relative_path(path: Path, repository: FrankiePaths) -> str:
    if repository.repo_root is None:
        return path.name
    return path.relative_to(repository.repo_root).as_posix()
