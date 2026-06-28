#!/usr/bin/env python3
"""Validate that prepared Live Mode remains disabled, simulated and offline."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_FILES = (
    *sorted((REPO_ROOT / "frankie" / "live").glob("*.py")),
    REPO_ROOT / "frankie" / "commands" / "live.py",
)
FORBIDDEN_IMPORTS = {"subprocess", "socket", "requests", "paramiko", "docker", "os", "pathlib"}
FORBIDDEN_NAMES = {"open", "exec", "eval"}
FORBIDDEN_ATTRIBUTES = {
    "system", "run", "Popen", "connect", "create_connection", "getenv", "write_text", "write_bytes"
}


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
        timeout=30,
    )


def _validate_runtime_ast() -> list[str]:
    issues: list[str] = []
    for path in RUNTIME_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] in FORBIDDEN_IMPORTS:
                        issues.append(f"{path.name}: forbidden import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.split(".")[0] in FORBIDDEN_IMPORTS:
                    issues.append(f"{path.name}: forbidden import {node.module}")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in FORBIDDEN_NAMES:
                    issues.append(f"{path.name}: forbidden call {node.func.id}")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in FORBIDDEN_ATTRIBUTES:
                    issues.append(f"{path.name}: forbidden call {node.func.attr}")
    return issues


def main() -> int:
    issues = _validate_runtime_ast()
    for command in ("live-status", "live-audit"):
        for simulated in (False, True):
            base_args = [command]
            if simulated:
                base_args.append("--simulate")
            text_result = _run(*base_args)
            if text_result.returncode != 0 or "No server has been contacted" not in text_result.stdout:
                issues.append(f"{' '.join(base_args)}: invalid text result")

            json_result = _run(*base_args, "--json")
            if json_result.returncode != 0:
                issues.append(f"{' '.join((*base_args, '--json'))}: non-zero exit")
                continue
            try:
                payload = json.loads(json_result.stdout)
            except json.JSONDecodeError:
                issues.append(f"{' '.join((*base_args, '--json'))}: invalid JSON")
                continue
            expected_status = "SIMULATED" if simulated else "BLOCKED"
            if payload.get("status") != expected_status:
                issues.append(f"{command}: unexpected status")
            for field in ("enabled", "connected", "server_contacted"):
                if payload.get(field) is not False:
                    issues.append(f"{command}: {field} must be false")
            if payload.get("simulated") is not simulated:
                issues.append(f"{command}: simulation flag mismatch")

    if issues:
        print("Frankie Live Mode guard validation: FAIL", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1
    print("Frankie Live Mode guard validation: PASS")
    print("Commands checked: 8")
    print("Server contacted: false")
    print("Dangerous runtime imports or calls: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
