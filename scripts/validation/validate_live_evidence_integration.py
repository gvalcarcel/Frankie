#!/usr/bin/env python3
"""Validate sanitized LIVE evidence integration without contacting infrastructure."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]
LIVE_GLOB = "docs/evidencias/frankie-core-v0.8.0/wo-live-*/structured*.json"
FORBIDDEN_IMPORTS = {"paramiko", "requests", "socket", "subprocess"}
RUNTIME_FILES = (
    "frankie/evidence/loader.py",
    "frankie/evidence/summary.py",
    "frankie/commands/evidence.py",
    "frankie/reports/builder.py",
    "frankie/reports/rendering.py",
)


class ValidationError(RuntimeError):
    """A controlled validation failure."""


def _run_frankie(*args: str) -> str:
    completed = subprocess.run(
        (sys.executable, "-m", "frankie", *args),
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=60,
    )
    if completed.returncode:
        detail = (completed.stderr or completed.stdout).strip()
        raise ValidationError(f"frankie {' '.join(args)} failed: {detail}")
    return completed.stdout


def _json_output(*args: str) -> dict[str, Any]:
    try:
        payload = json.loads(_run_frankie(*args))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"frankie {' '.join(args)} returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise ValidationError(f"frankie {' '.join(args)} must return a JSON object")
    return payload


def _validate_runtime_boundaries() -> None:
    for relative in RUNTIME_FILES:
        path = REPO_ROOT / relative
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                names = {(node.module or "").split(".")[0]}
            else:
                continue
            forbidden = names & FORBIDDEN_IMPORTS
            if forbidden:
                raise ValidationError(f"{relative} imports forbidden module: {sorted(forbidden)[0]}")


def validate() -> tuple[int, int]:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
    from frankie.core.paths import FrankiePaths
    from frankie.evidence.loader import load_structured_evidence

    paths = FrankiePaths(REPO_ROOT)
    files = sorted(REPO_ROOT.glob(LIVE_GLOB))
    if len(files) != 2:
        raise ValidationError(f"expected 2 sanitized LIVE evidence files, found {len(files)}")

    result = load_structured_evidence(paths)
    if result.issues:
        raise ValidationError("evidence loader reported invalid files")
    live = [item for item in result.evidence if item.mode in {"live-readonly", "live-controlled"}]
    if len(live) != 2:
        raise ValidationError(f"expected 2 loaded LIVE evidences, found {len(live)}")
    if any(item.security[flag] for item in live for flag in item.security):
        raise ValidationError("loaded LIVE evidence reports sensitive content")
    if any(item.details.get("raw_outputs_committed") is not False for item in live):
        raise ValidationError("LIVE evidence raw-output guard is not satisfied")

    validation = _run_frankie("evidence", "validate")
    if "Result: PASS" not in validation or "Invalid: 0" not in validation:
        raise ValidationError("evidence validate did not report PASS")
    summary = _json_output("evidence", "summary", "--json")
    if summary.get("live_evidence", {}).get("total") != 2:
        raise ValidationError("evidence summary does not contain both LIVE evidences")
    report = _json_output("report", "--json")
    live_report = report.get("live_evidence", {})
    if live_report.get("temporary_access_removed") is not True:
        raise ValidationError("report does not confirm temporary access removal")
    if live_report.get("new_live_connection") is not False:
        raise ValidationError("report incorrectly claims a new LIVE connection")

    _validate_runtime_boundaries()
    return len(result.evidence), len(live)


def main(argv: Sequence[str] | None = None) -> int:
    if argv:
        print("This validator does not accept arguments.", file=sys.stderr)
        return 2
    try:
        total, live = validate()
    except (OSError, ValidationError) as exc:
        print(f"LIVE evidence integration: FAIL - {exc}", file=sys.stderr)
        return 1
    print("LIVE evidence integration: PASS")
    print(f"Evidence loaded: {total}")
    print(f"Sanitized LIVE evidence: {live}")
    print("New LIVE connections: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
