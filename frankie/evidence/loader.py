from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from frankie.core.paths import FrankiePaths
from frankie.evidence.models import EvidenceLoadIssue, EvidenceLoadResult, StructuredEvidence


STRUCTURED_EVIDENCE_DIRECTORY = "docs/evidencias/structured"
LIVE_EVIDENCE_GLOB = "docs/evidencias/frankie-core-v0.8.0/wo-live-*/structured*.json"
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
ALLOWED_MODES = {"offline", "documented-evidence", "live", "live-readonly", "live-controlled"}
SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----", re.IGNORECASE),
    re.compile(r"\bssh-(?:rsa|ed25519)\s+[A-Za-z0-9+/]{20,}", re.IGNORECASE),
    re.compile(r"\b(?:password|secret|token|client_secret|smtp_password|private_key|credential)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"\b10(?:\.\d{1,3}){3}\b"),
    re.compile(r"\b192\.168(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}\b"),
    re.compile(r"\b(?:[0-9a-f]{2}:){5}[0-9a-f]{2}\b", re.IGNORECASE),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
)


def load_structured_evidence(paths: FrankiePaths | None = None) -> EvidenceLoadResult:
    repository = paths or FrankiePaths.discover()
    directory = repository.resolve(STRUCTURED_EVIDENCE_DIRECTORY)
    root = repository.repo_root
    if root is None:
        return EvidenceLoadResult(False, STRUCTURED_EVIDENCE_DIRECTORY, (), ())

    structured_paths = sorted(directory.glob("*.json")) if directory and directory.is_dir() else []
    live_paths = sorted(root.glob(LIVE_EVIDENCE_GLOB))
    if not structured_paths and not live_paths and (directory is None or not directory.is_dir()):
        return EvidenceLoadResult(False, STRUCTURED_EVIDENCE_DIRECTORY, (), ())

    evidence: list[StructuredEvidence] = []
    issues: list[EvidenceLoadIssue] = []
    evidence_paths: dict[str, str] = {}
    candidates = [(path, False) for path in structured_paths] + [(path, True) for path in live_paths]
    for path, is_live in candidates:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            relative_path = _relative_path(path, repository)
            parsed = _parse_live_evidence(payload, relative_path) if is_live else _parse_evidence(payload)
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
        directory=f"{STRUCTURED_EVIDENCE_DIRECTORY}; {LIVE_EVIDENCE_GLOB}",
        evidence=tuple(evidence),
        issues=tuple(issues),
    )


def _parse_live_evidence(payload: Any, relative_path: str) -> StructuredEvidence:
    if not isinstance(payload, dict):
        raise ValueError("LIVE evidence root must be an object")
    required = (
        "schema_version",
        "evidence_id",
        "evidence_type",
        "mode",
        "server_contacted",
        "changes_made",
        "sanitization",
    )
    missing = [field for field in required if field not in payload]
    if missing:
        raise ValueError(f"missing required LIVE fields: {', '.join(missing)}")

    mode = _required_string(payload, "mode")
    if mode not in {"live-readonly", "live-controlled"}:
        raise ValueError(f"unsupported LIVE mode: {mode}")
    if not isinstance(payload["server_contacted"], bool) or not isinstance(payload["changes_made"], bool):
        raise ValueError("server_contacted and changes_made must be boolean")

    sanitization = _required_object(payload, "sanitization")
    for field in ("internal_ips_removed", "usernames_removed", "secrets_removed", "raw_outputs_committed"):
        if not isinstance(sanitization.get(field), bool):
            raise ValueError(f"sanitization.{field} must be boolean")
    if not all(sanitization[field] for field in ("internal_ips_removed", "usernames_removed", "secrets_removed")):
        raise ValueError("LIVE evidence sanitization is incomplete")
    if sanitization["raw_outputs_committed"]:
        raise ValueError("LIVE evidence must not contain raw outputs")
    if _contains_sensitive_value(payload) or _contains_identity_field(payload):
        raise ValueError("possible sensitive data detected in LIVE evidence values")

    evidence_type = _required_string(payload, "evidence_type")
    changes_made = payload["changes_made"]
    if evidence_type == "live_readonly_capture":
        if mode != "live-readonly" or changes_made:
            raise ValueError("live_readonly_capture must use live-readonly with changes_made=false")
        status = "WARNING" if payload.get("findings") else "OK"
        severity = _highest_live_severity(payload.get("findings", []))
        component_id = "frankie-live-capture"
        component_name = "Frankie LIVE Read-only Capture"
        summary = "Sanitized real read-only capture recorded for the Frankie infrastructure."
        recommendation = "Review the sanitized findings without treating them as a new LIVE observation."
    elif evidence_type == "live_access_cleanup":
        if mode != "live-controlled" or not changes_made:
            raise ValueError("live_access_cleanup must use live-controlled with changes_made=true")
        removed = payload.get("result") == "temporary_live_access_removed"
        status = "PASS" if removed else "WARNING"
        severity = "INFO" if removed else "MEDIUM"
        component_id = "frankie-live-access"
        component_name = "Frankie LIVE Temporary Access"
        summary = "Temporary LIVE access removal is documented and validated."
        recommendation = "Keep temporary LIVE access closed unless a new authorized Work Order requires it."
    else:
        raise ValueError(f"unsupported LIVE evidence_type: {evidence_type}")

    captured_at = payload.get("captured_at")
    if captured_at is not None:
        _optional_timestamp(payload, "captured_at")

    return StructuredEvidence(
        schema_version=_required_string(payload, "schema_version"),
        evidence_id=_required_string(payload, "evidence_id"),
        evidence_type=evidence_type,
        component_id=component_id,
        component_name=component_name,
        status=status,
        severity=severity,
        mode=mode,
        data_source="sanitized_live_evidence",
        summary=summary,
        details={
            "server_contacted": payload["server_contacted"],
            "changes_made": changes_made,
            "temporary_access_removed": payload.get("result") == "temporary_live_access_removed",
            "raw_outputs_committed": sanitization["raw_outputs_committed"],
        },
        references=(relative_path,),
        server_impact={
            "touches_physical_server": payload["server_contacted"],
            "requires_live_connection": payload["server_contacted"],
            "changes_configuration": changes_made,
        },
        security={
            "contains_secrets": False,
            "contains_credentials": False,
            "contains_internal_ips": False,
        },
        recommendation=recommendation,
        created_at=captured_at,
        source_files=(relative_path,),
    )


def _highest_live_severity(findings: Any) -> str:
    if not isinstance(findings, list):
        raise ValueError("findings must be a list")
    rank = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
    highest = "INFO"
    for finding in findings:
        if not isinstance(finding, dict):
            raise ValueError("each LIVE finding must be an object")
        severity = finding.get("severity", "INFO")
        if severity not in rank:
            raise ValueError(f"unsupported LIVE finding severity: {severity}")
        if rank[severity] > rank[highest]:
            highest = severity
    return highest


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


def _contains_identity_field(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if (
                key.lower() in {"user", "username", "credential", "credentials"}
                and item is not None
                and item != ""
                and item is not False
            ):
                return True
            if _contains_identity_field(item):
                return True
    elif isinstance(value, list):
        return any(_contains_identity_field(item) for item in value)
    return False


def _relative_path(path: Path, repository: FrankiePaths) -> str:
    if repository.repo_root is None:
        return path.name
    return path.relative_to(repository.repo_root).as_posix()
