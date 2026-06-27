from __future__ import annotations

import ast
import subprocess
import sys
import unittest
from pathlib import Path

from frankie.core.models import AuditFinding, DoctorReport, InventoryItem
from frankie.doctor.advice import build_doctor_findings
from frankie.doctor.doctor_engine import run_doctor


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTOR_FLOW_FILES = (
    REPO_ROOT / "frankie" / "commands" / "doctor.py",
    REPO_ROOT / "frankie" / "doctor" / "doctor_engine.py",
    REPO_ROOT / "frankie" / "doctor" / "advice.py",
    REPO_ROOT / "frankie" / "doctor" / "rules.py",
    REPO_ROOT / "frankie" / "output" / "console.py",
)


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class DoctorCommandTests(unittest.TestCase):
    def test_doctor_returns_zero(self) -> None:
        result = run_frankie("doctor")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_doctor_output_contains_required_header_and_scope(self) -> None:
        result = run_frankie("doctor")
        self.assertIn("Frankie Doctor", result.stdout)
        self.assertIn("Version: 0.7.0-dev", result.stdout)
        self.assertIn("Mode: read-only foundation", result.stdout)
        self.assertIn("audit engine", result.stdout)
        self.assertIn("Live connection", result.stdout)
        self.assertIn("Repairs", result.stdout)
        self.assertIn("no", result.stdout)

    def test_doctor_output_contains_findings_steps_and_do_not_section(self) -> None:
        result = run_frankie("doctor")
        self.assertIn("AUD-", result.stdout)
        self.assertIn("Safe next steps", result.stdout)
        self.assertIn("Do not", result.stdout)
        self.assertIn("Overall doctor result: ACTIONS_RECOMMENDED", result.stdout)

    def test_doctor_does_not_present_validated_smb_as_pending_action(self) -> None:
        result = run_frankie("doctor")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("AUD-SERVICES-PORTAINER-001", result.stdout)
        self.assertNotIn("AUD-SAMBA-001", result.stdout)
        self.assertNotIn("SMB validation from a Windows client is still pending", result.stdout)

    def test_doctor_verbose_shows_extra_context(self) -> None:
        result = run_frankie("doctor", "--verbose")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Audit check:", result.stdout)
        self.assertIn("Why no automatic repair:", result.stdout)
        self.assertIn("Status and severity:", result.stdout)

    def test_help_shows_doctor_as_available_command(self) -> None:
        result = run_frankie("help")
        self.assertIn("frankie doctor", result.stdout)
        self.assertNotIn("Command 'doctor' is not implemented yet", result.stdout)

    def test_audit_status_and_inventory_still_work(self) -> None:
        for command in ("audit", "status", "inventory"):
            with self.subTest(command=command):
                result = run_frankie(command)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_doctor_handles_no_relevant_findings(self) -> None:
        report = DoctorReport(
            version="0.7.0-dev",
            mode="read-only foundation",
            scope=(InventoryItem("Source", "audit engine"),),
            audit_result="PASS",
            findings=(),
            overall_result="HEALTHY",
        )
        from frankie.output.console import render_doctor

        output = render_doctor(report)
        self.assertIn("No non-pass findings require explanation.", output)
        self.assertIn("Overall doctor result: HEALTHY", output)

    def test_doctor_only_explains_relevant_audit_findings(self) -> None:
        findings = (
            AuditFinding(
                id="AUD-X-001",
                name="ok finding",
                description="all good",
                category="Test",
                status="PASS",
                severity="INFO",
                evidence=("doc.md",),
                message="pass",
                recommendation="none",
            ),
            AuditFinding(
                id="AUD-X-002",
                name="warn finding",
                description="warn",
                category="Test",
                status="WARN",
                severity="LOW",
                evidence=("doc.md",),
                message="warn",
                recommendation="review",
            ),
        )
        doctor_findings = build_doctor_findings(findings)
        self.assertEqual(len(doctor_findings), 1)
        self.assertEqual(doctor_findings[0].source_check_id, "AUD-X-002")

    def test_doctor_flow_has_no_subprocess_or_write_operations(self) -> None:
        forbidden_names = {"open"}
        forbidden_attrs = {"run", "Popen", "write_text", "write_bytes", "unlink", "remove"}

        for path in DOCTOR_FLOW_FILES:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, forbidden_names, f"{path} uses {node.func.id}()")
                    if isinstance(node.func, ast.Attribute):
                        self.assertNotIn(node.func.attr, forbidden_attrs, f"{path} uses .{node.func.attr}()")
