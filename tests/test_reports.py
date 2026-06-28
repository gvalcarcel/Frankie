from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from frankie.core.paths import FrankiePaths
from frankie.reports.writer import ReportOutputError, write_report


REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_RUNTIME_FILES = (
    REPO_ROOT / "frankie" / "commands" / "report.py",
    REPO_ROOT / "frankie" / "reports" / "builder.py",
    REPO_ROOT / "frankie" / "reports" / "models.py",
    REPO_ROOT / "frankie" / "reports" / "rendering.py",
    REPO_ROOT / "frankie" / "reports" / "writer.py",
)


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ReportCommandTests(unittest.TestCase):
    def test_report_defaults_to_markdown(self) -> None:
        result = run_frankie("report")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("# Frankie Core Consolidated Report"))
        for heading in ("Overall status", "Inventory summary", "Audit findings", "Doctor diagnosis", "Evidence summary"):
            self.assertIn(heading, result.stdout)
        self.assertIn("Mode: `offline`", result.stdout)
        self.assertIn("Frankie physical server was not consulted.", result.stdout)
        self.assertIn("Live Mode is not implemented.", result.stdout)
        self.assertIn("Repair Mode is not implemented.", result.stdout)

    def test_report_markdown_is_explicit(self) -> None:
        result = run_frankie("report", "--markdown")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("# Frankie Core Consolidated Report", result.stdout)
        self.assertIn("SMB: `OK / PASS / INFO`", result.stdout)
        self.assertIn("Portainer: `WARNING / WARN / LOW`", result.stdout)

    def test_report_json_contract(self) -> None:
        result = run_frankie("report", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["command"], "report")
        self.assertEqual(payload["frankie_core_version"], "0.8.0-dev")
        self.assertEqual(payload["mode"], "offline")
        self.assertEqual(payload["known_state"]["smb"], "OK / PASS / INFO")
        self.assertEqual(payload["known_state"]["portainer"], "WARNING / WARN / LOW")
        for section in ("status", "inventory", "audit", "doctor", "evidence"):
            self.assertIn(section, payload)

    def test_report_rejects_conflicting_formats(self) -> None:
        result = run_frankie("report", "--json", "--markdown")

        self.assertEqual(result.returncode, 2)
        self.assertIn("either --json or --markdown", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_report_cli_blocks_output_outside_evidence_directory(self) -> None:
        result = run_frankie("report", "--output", "README.md")

        self.assertEqual(result.returncode, 2)
        self.assertIn("inside docs/evidencias", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_existing_commands_still_work(self) -> None:
        for command in ("version", "help", "status", "inventory", "audit", "doctor"):
            with self.subTest(command=command):
                result = run_frankie(command)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_report_runtime_has_no_subprocess_env_or_network_access(self) -> None:
        forbidden_names = {"open", "exec", "eval"}
        forbidden_attrs = {"run", "Popen", "system", "connect", "create_connection", "getenv"}
        for path in REPORT_RUNTIME_FILES:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, forbidden_names, f"{path} uses {node.func.id}()")
                if isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, forbidden_attrs, f"{path} uses .{node.func.attr}()")


class ReportWriterTests(unittest.TestCase):
    def test_writer_allows_only_evidence_directory_and_expected_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = FrankiePaths(root)
            destination = write_report("# Safe", "docs/evidencias/test/report.md", "markdown", paths=paths)

            self.assertTrue(destination.exists())
            self.assertEqual(destination.read_text(encoding="utf-8"), "# Safe\n")
            with self.assertRaises(ReportOutputError):
                write_report("unsafe", "outside.md", "markdown", paths=paths)
            with self.assertRaises(ReportOutputError):
                write_report("wrong", "docs/evidencias/report.txt", "markdown", paths=paths)

    def test_writer_does_not_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = FrankiePaths(root)
            output = "docs/evidencias/report.json"
            write_report('{"first": true}', output, "json", paths=paths)

            with self.assertRaises(ReportOutputError):
                write_report('{"second": true}', output, "json", paths=paths)

            write_report('{"second": true}', output, "json", force=True, paths=paths)
            self.assertIn("second", (root / output).read_text(encoding="utf-8"))
