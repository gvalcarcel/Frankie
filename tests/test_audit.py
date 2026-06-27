from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from frankie.audit.audit_engine import run_audit
from frankie.core.paths import (
    EVIDENCE_AUDIT_REPORT,
    EVIDENCE_PRE_RELEASE_LIVE_CHECK,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_SRV_SERVICIOS,
    FrankiePaths,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_FLOW_FILES = (
    REPO_ROOT / "frankie" / "commands" / "audit.py",
    REPO_ROOT / "frankie" / "audit" / "audit_engine.py",
    REPO_ROOT / "frankie" / "audit" / "checks.py",
    REPO_ROOT / "frankie" / "audit" / "rules.py",
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


class AuditCommandTests(unittest.TestCase):
    def test_audit_returns_zero(self) -> None:
        result = run_frankie("audit")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_audit_output_contains_required_header_and_scope(self) -> None:
        result = run_frankie("audit")
        self.assertIn("Frankie Audit", result.stdout)
        self.assertIn("Version: 0.7.0", result.stdout)
        self.assertIn("Mode: read-only foundation", result.stdout)
        self.assertIn("repository evidence", result.stdout)
        self.assertIn("Live connection", result.stdout)
        self.assertIn("no", result.stdout)

    def test_audit_output_contains_summary_findings_and_overall_result(self) -> None:
        result = run_frankie("audit")
        self.assertIn("Checks total", result.stdout)
        self.assertIn("AUD-", result.stdout)
        self.assertIn("Overall audit result", result.stdout)

    def test_audit_verbose_shows_description_and_recommendation(self) -> None:
        result = run_frankie("audit", "--verbose")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Description:", result.stdout)
        self.assertIn("Recommendation:", result.stdout)

    def test_help_shows_audit_as_available_command(self) -> None:
        result = run_frankie("help")
        self.assertIn("frankie audit", result.stdout)
        self.assertIn("Planned commands:", result.stdout)
        self.assertIn("  none", result.stdout)

    def test_missing_evidence_does_not_break_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = run_audit(FrankiePaths(Path(tmp)))
            statuses = {finding.status for finding in report.findings}

            self.assertIn("MISSING_EVIDENCE", statuses)
            self.assertIn("UNKNOWN", statuses)

    def test_engine_can_produce_required_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root, EVIDENCE_SRV_SERVICIOS, "5432 no escucha en el host")
            self._write(root, EVIDENCE_SRV_RECURSOS, "Samba activo")
            self._write(
                root,
                EVIDENCE_AUDIT_REPORT,
                "\n".join(
                    [
                        "apto para dry-run",
                        "Portainer publica 8000",
                        "falta validar Samba desde cliente Windows",
                        "PostgreSQL no expone 5432",
                    ]
                ),
            )
            self._write(root, "docs/frankie-core/status.md", "read-only no ejecuta comandos externos")
            self._write(root, "docs/frankie-core/inventory.md", "Frankie Core servidor físico repositorio Frankie")

            report = run_audit(FrankiePaths(root))
            statuses = {finding.status for finding in report.findings}

            self.assertIn("PASS", statuses)
            self.assertIn("WARN", statuses)
            self.assertIn("PENDING", statuses)
            self.assertEqual(report.overall_result, "WARN")

    def test_smb_pre_release_evidence_resolves_historical_pending_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root, EVIDENCE_SRV_SERVICIOS, "5432 no escucha en el host")
            self._write(root, EVIDENCE_SRV_RECURSOS, "Samba activo")
            self._write(
                root,
                EVIDENCE_AUDIT_REPORT,
                "\n".join(
                    [
                        "apto para dry-run",
                        "Portainer publica 8000",
                        "falta validar Samba desde cliente Windows",
                        "PostgreSQL no expone 5432",
                    ]
                ),
            )
            self._write(
                root,
                EVIDENCE_PRE_RELEASE_LIVE_CHECK,
                "\n".join(
                    [
                        "SMB validation: OK",
                        "Samba/SMB validation: validated",
                        "No se modifico Samba durante la validacion.",
                    ]
                ),
            )
            self._write(root, "docs/frankie-core/status.md", "read-only no ejecuta comandos externos")
            self._write(root, "docs/frankie-core/inventory.md", "Frankie Core servidor físico repositorio Frankie")

            report = run_audit(FrankiePaths(root))
            findings = {finding.id: finding for finding in report.findings}

            self.assertEqual(findings["AUD-SAMBA-001"].status, "PASS")
            self.assertEqual(findings["AUD-SAMBA-001"].severity, "INFO")
            self.assertIn(EVIDENCE_PRE_RELEASE_LIVE_CHECK, findings["AUD-SAMBA-001"].evidence)
            self.assertEqual(findings["AUD-SERVICES-PORTAINER-001"].status, "WARN")
            self.assertEqual(report.overall_result, "WARN")

    def test_audit_flow_has_no_subprocess_or_write_operations(self) -> None:
        forbidden_names = {"open"}
        forbidden_attrs = {"run", "Popen", "write_text", "write_bytes", "unlink", "remove"}

        for path in AUDIT_FLOW_FILES:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, forbidden_names, f"{path} uses {node.func.id}()")
                    if isinstance(node.func, ast.Attribute):
                        self.assertNotIn(node.func.attr, forbidden_attrs, f"{path} uses .{node.func.attr}()")

    def _write(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
