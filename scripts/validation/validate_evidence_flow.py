#!/usr/bin/env python3
"""Automate Frankie Core's offline evidence and report validation flow."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence


ARTIFACT_NAMES = (
    "consolidated_report.md",
    "consolidated_report.json",
    "validation_evidence.json",
    "validation_summary.md",
)
REPO_MARKERS = ("README.md", "ROADMAP.md", "pyproject.toml", "frankie")
DEFAULT_TIMEOUT_SECONDS = 180
CLI_REGRESSION: tuple[tuple[str, ...], ...] = (
    ("version",),
    ("help",),
    ("status",),
    ("inventory",),
    ("audit",),
    ("audit", "--verbose"),
    ("doctor",),
    ("doctor", "--verbose"),
    ("evidence", "list"),
    ("evidence", "validate"),
    ("evidence", "summary"),
    ("evidence", "summary", "--json"),
    ("report",),
    ("report", "--json"),
)


class ValidationFlowError(RuntimeError):
    """Controlled validation failure suitable for concise CLI output."""


@dataclass(frozen=True)
class CommandResult:
    label: str
    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


def _discover_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    raise ValidationFlowError("Frankie repository root could not be determined.")


def _resolve_output_dir(repo_root: Path, requested: str | None, generated_at: datetime) -> Path:
    allowed_root = (repo_root / "docs" / "evidencias").resolve()
    if requested:
        candidate = Path(requested)
        output_dir = (candidate if candidate.is_absolute() else repo_root / candidate).resolve()
    else:
        run_id = generated_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = (allowed_root / "frankie-core-v0.8.0" / "validation-runs" / run_id).resolve()
    if not output_dir.is_relative_to(allowed_root) or output_dir == allowed_root:
        raise ValidationFlowError("Output directory must be inside docs/evidencias/.")
    return output_dir


def _run(
    command: Sequence[str],
    repo_root: Path,
    label: str,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> CommandResult:
    try:
        completed = subprocess.run(
            list(command),
            cwd=repo_root,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise ValidationFlowError(f"{label} exceeded the {timeout}-second timeout.") from exc
    result = CommandResult(label, tuple(command), completed.returncode, completed.stdout, completed.stderr)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        suffix = f" Last output: {detail[-1]}" if detail else ""
        raise ValidationFlowError(f"{label} failed with exit code {result.returncode}.{suffix}")
    return result


def _run_frankie(repo_root: Path, args: Sequence[str], label: str) -> CommandResult:
    return _run((sys.executable, "-m", "frankie", *args), repo_root, label)


def _parse_json_output(result: CommandResult) -> dict[str, Any]:
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValidationFlowError(f"{result.label} did not produce valid JSON.") from exc
    if not isinstance(payload, dict):
        raise ValidationFlowError(f"{result.label} JSON root must be an object.")
    return payload


def _git_status(repo_root: Path) -> set[str]:
    result = _run(
        ("git", "status", "--porcelain", "--untracked-files=all"),
        repo_root,
        "Git status",
        timeout=30,
    )
    paths: set[str] = set()
    for line in result.stdout.splitlines():
        value = line[3:].strip() if len(line) > 3 else ""
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        if value:
            paths.add(value.replace("\\", "/"))
    return paths


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _write_text(path: Path, content: str, force: bool) -> None:
    if path.is_symlink():
        raise ValidationFlowError(f"Symbolic-link artifacts are not allowed: {path.name}.")
    if path.exists() and not force:
        raise ValidationFlowError(f"Artifact already exists: {path.name}. Use --force to replace it.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def _build_validation_evidence(
    *,
    generated_at: str,
    output_relative: str,
    test_count: int,
    evidence_total: int,
    report_hashes: dict[str, str],
    baseline_clean: bool,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "evidence_id": f"automated-validation-{generated_at.replace(':', '').replace('+', '-')}",
        "evidence_type": "automated_operational_validation",
        "component": {"id": "frankie-core-validation-flow", "name": "Frankie Core Validation Flow"},
        "status": "PASS",
        "severity": "INFO",
        "mode": "offline",
        "data_source": "automated_local_validation",
        "summary": "Automated tests, CLI regression, evidence checks and report exports completed successfully.",
        "details": {
            "tests_passed": test_count,
            "cli_commands_passed": len(CLI_REGRESSION),
            "structured_evidence_valid": evidence_total,
            "structured_evidence_invalid": 0,
            "git_baseline_clean": baseline_clean,
            "report_sha256": report_hashes,
        },
        "references": [
            f"{output_relative}/validation_summary.md",
            f"{output_relative}/consolidated_report.md",
            f"{output_relative}/consolidated_report.json",
        ],
        "created_at": generated_at,
        "updated_at": generated_at,
        "source_files": ["scripts/validation/validate_evidence_flow.py"],
        "related_checks": [
            "WO-0020-TESTS-001",
            "WO-0020-CLI-001",
            "WO-0020-EVIDENCE-001",
            "WO-0020-REPORTS-001",
            "WO-0020-GIT-001",
        ],
        "server_impact": {
            "touches_physical_server": False,
            "requires_live_connection": False,
            "changes_configuration": False,
        },
        "security": {
            "contains_secrets": False,
            "contains_credentials": False,
            "contains_internal_ips": False,
        },
        "recommendation": "Reuse this offline flow before future releases and keep LIVE validation in separate authorized Work Orders.",
    }


def _validate_evidence_payload(payload: dict[str, Any]) -> None:
    from frankie.core.paths import FrankiePaths
    from frankie.evidence.loader import load_structured_evidence

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        evidence_dir = root / "docs" / "evidencias" / "structured"
        evidence_dir.mkdir(parents=True)
        (evidence_dir / "validation_evidence.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result = load_structured_evidence(FrankiePaths(root))
    if len(result.evidence) != 1 or result.issues:
        messages = "; ".join(issue.message for issue in result.issues) or "evidence was not loaded"
        raise ValidationFlowError(f"Generated evidence failed validation: {messages}")


def _summary_markdown(
    *,
    generated_at: str,
    output_relative: str,
    test_count: int,
    evidence_total: int,
    report_hashes: dict[str, str],
    evidence_hash: str,
    baseline_clean: bool,
    repository_delta_ok: bool,
) -> str:
    baseline = "clean" if baseline_clean else "contained pre-existing Work Order changes"
    delta = "PASS" if repository_delta_ok else "FAIL"
    return f"""# Automated validation result

## Identification

- Work Order: `WO-0020`.
- Generated at: `{generated_at}`.
- Mode: `offline`.
- Result: `PASS`.
- Output directory: `{output_relative}`.

## Checks

| Check | Result |
| --- | --- |
| Unit and integration tests | PASS ({test_count} tests) |
| Python compilation | PASS |
| CLI regression | PASS ({len(CLI_REGRESSION)} commands) |
| Structured evidence | PASS ({evidence_total} valid, 0 invalid) |
| Markdown report export | PASS |
| JSON report export and parsing | PASS |
| Repository delta | {delta} |

The Git baseline {baseline}. The final delta check accepts only the four generated artifacts in this output directory and preserves any pre-existing changes without modifying them.

## Artifacts

| File | SHA-256 |
| --- | --- |
| `consolidated_report.md` | `{report_hashes['consolidated_report.md']}` |
| `consolidated_report.json` | `{report_hashes['consolidated_report.json']}` |
| `validation_evidence.json` | `{evidence_hash}` |

## Safety

- No connection to Frankie or its virtual machines.
- No package installation, service restart or configuration change.
- No secrets, credentials or internal addresses collected.
- Files are written only inside `docs/evidencias/`.
- Existing artifacts are not replaced unless `--force` is explicit.

## Limitations

- Results describe the local repository and documented evidence, not current LIVE infrastructure.
- The generated execution evidence is validated with the Frankie loader but is not added automatically to the canonical structured evidence catalog.
- Git cleanliness is a delta check; use `--require-clean` when a completely clean baseline is mandatory.
"""


def run_flow(args: argparse.Namespace) -> Path:
    repo_root = _discover_repo_root()
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    generated = datetime.now().astimezone().replace(microsecond=0)
    generated_at = generated.isoformat()
    output_dir = _resolve_output_dir(repo_root, args.output_dir, generated)
    output_relative = output_dir.relative_to(repo_root).as_posix()
    expected_paths = {f"{output_relative}/{name}" for name in ARTIFACT_NAMES}

    existing = [name for name in ARTIFACT_NAMES if (output_dir / name).exists()]
    if existing and not args.force:
        raise ValidationFlowError("Output contains existing artifacts. Use --force to replace known files.")

    baseline_status = _git_status(repo_root)
    if args.require_clean and baseline_status:
        raise ValidationFlowError("Repository must be clean when --require-clean is used.")

    tests = _run(
        (sys.executable, "-m", "unittest", "discover", "-s", "tests"),
        repo_root,
        "Automated tests",
    )
    test_output = f"{tests.stdout}\n{tests.stderr}"
    match = re.search(r"Ran\s+(\d+)\s+tests?", test_output)
    if not match or "OK" not in test_output:
        raise ValidationFlowError("Automated test summary could not be verified.")
    test_count = int(match.group(1))

    _run((sys.executable, "-m", "compileall", "-q", "frankie"), repo_root, "Python compilation")

    regression_payloads: dict[tuple[str, ...], dict[str, Any]] = {}
    for command_args in CLI_REGRESSION:
        result = _run_frankie(repo_root, command_args, f"frankie {' '.join(command_args)}")
        if command_args[-1] == "--json":
            regression_payloads[command_args] = _parse_json_output(result)

    validation = _run_frankie(repo_root, ("evidence", "validate"), "Evidence validation")
    if "Result: PASS" not in validation.stdout or "Invalid: 0" not in validation.stdout:
        raise ValidationFlowError("Structured evidence validation did not report PASS with zero invalid files.")
    summary = regression_payloads[("evidence", "summary", "--json")]
    evidence_total = summary.get("total")
    if not isinstance(evidence_total, int) or evidence_total < 1 or summary.get("invalid") != 0:
        raise ValidationFlowError("Evidence summary contains unexpected counts.")

    output_dir.mkdir(parents=True, exist_ok=True)
    markdown_relative = f"{output_relative}/consolidated_report.md"
    json_relative = f"{output_relative}/consolidated_report.json"
    markdown_args = ["report", "--markdown", "--output", markdown_relative]
    json_args = ["report", "--json", "--output", json_relative]
    if args.force:
        markdown_args.append("--force")
        json_args.append("--force")
    _run_frankie(repo_root, markdown_args, "Markdown report export")
    _run_frankie(repo_root, json_args, "JSON report export")

    markdown_path = output_dir / "consolidated_report.md"
    json_path = output_dir / "consolidated_report.json"
    exported = json.loads(json_path.read_text(encoding="utf-8"))
    if exported.get("command") != "report" or exported.get("mode") != "offline":
        raise ValidationFlowError("Exported report JSON contract is invalid.")
    if exported.get("evidence", {}).get("total") != evidence_total:
        raise ValidationFlowError("Exported report evidence count does not match the validated summary.")
    markdown = markdown_path.read_text(encoding="utf-8")
    if "# Frankie Core Consolidated Report" not in markdown or f"Valid evidence: `{evidence_total}`" not in markdown:
        raise ValidationFlowError("Exported Markdown report does not contain the expected evidence summary.")

    report_hashes = {
        "consolidated_report.md": _sha256(markdown_path),
        "consolidated_report.json": _sha256(json_path),
    }
    current_status = _git_status(repo_root)
    unexpected_delta = (current_status - baseline_status) - expected_paths
    repository_delta_ok = not unexpected_delta
    if not repository_delta_ok:
        raise ValidationFlowError("Validation created files outside the expected output set.")

    evidence = _build_validation_evidence(
        generated_at=generated_at,
        output_relative=output_relative,
        test_count=test_count,
        evidence_total=evidence_total,
        report_hashes=report_hashes,
        baseline_clean=not baseline_status,
    )
    _validate_evidence_payload(evidence)
    evidence_path = output_dir / "validation_evidence.json"
    _write_text(evidence_path, json.dumps(evidence, ensure_ascii=False, indent=2), args.force)
    evidence_hash = _sha256(evidence_path)

    summary_text = _summary_markdown(
        generated_at=generated_at,
        output_relative=output_relative,
        test_count=test_count,
        evidence_total=evidence_total,
        report_hashes=report_hashes,
        evidence_hash=evidence_hash,
        baseline_clean=not baseline_status,
        repository_delta_ok=repository_delta_ok,
    )
    _write_text(output_dir / "validation_summary.md", summary_text, args.force)

    final_status = _git_status(repo_root)
    unexpected_final = (final_status - baseline_status) - expected_paths
    if unexpected_final:
        raise ValidationFlowError("Final repository delta contains unexpected files.")
    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Frankie Core's offline evidence validation flow.")
    parser.add_argument("--output-dir", help="Destination inside docs/evidencias/. Defaults to a UTC run folder.")
    parser.add_argument("--force", action="store_true", help="Replace only the four known artifacts if they exist.")
    parser.add_argument("--require-clean", action="store_true", help="Stop unless the Git baseline is completely clean.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        destination = run_flow(args)
    except ValidationFlowError as exc:
        print(f"Validation flow error: {exc}", file=sys.stderr)
        return 1
    print("Frankie automated validation: PASS")
    print(f"Artifacts: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
