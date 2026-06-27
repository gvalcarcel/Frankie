from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from frankie.core.paths import (
    EVIDENCE_AUDIT_REPORT,
    EVIDENCE_MAINTENANCE_REPORT,
    EVIDENCE_PRE_RELEASE_LIVE_CHECK,
    EVIDENCE_SRV_RECURSOS,
    EVIDENCE_SRV_SERVICIOS,
    FrankiePaths,
)
from frankie.core.status import build_status_report


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class StatusCommandTests(unittest.TestCase):
    def test_status_returns_zero(self) -> None:
        result = run_frankie("status")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_status_output_contains_required_header(self) -> None:
        result = run_frankie("status")
        self.assertIn("Frankie Status", result.stdout)
        self.assertIn("Version: 0.7.0-dev", result.stdout)
        self.assertIn("Mode: read-only foundation", result.stdout)

    def test_missing_evidence_does_not_break_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = build_status_report(FrankiePaths(root))
            states = [item.state for section in report.sections for item in section.items]
            self.assertIn("MISSING EVIDENCE", states)

    def test_simulated_evidence_detects_warning_and_ok_states(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root, EVIDENCE_SRV_SERVICIOS, "OK: Docker activo\n5432 no escucha en el host\n")
            self._write(root, EVIDENCE_SRV_RECURSOS, "OK: Samba activo\n")
            self._write(
                root,
                EVIDENCE_AUDIT_REPORT,
                "\n".join(
                    [
                        "apto para dry-run",
                        "Portainer publica 8000",
                        "falta validar Samba desde un cliente Windows",
                        "PostgreSQL no expone 5432",
                        "backups existentes",
                    ]
                ),
            )
            self._write(root, "docs/arquitectura.md", "Frankie architecture")
            self._write(
                root,
                EVIDENCE_MAINTENANCE_REPORT,
                "Backup de srv-recursos instalado en /srv/scripts/backup-recursos.sh y /srv/backups/recursos",
            )

            report = build_status_report(FrankiePaths(root))
            flattened = {item.name: item.state for section in report.sections for item in section.items}

            self.assertEqual(flattened["srv-servicios audit"], "OK")
            self.assertEqual(flattened["srv-recursos audit"], "OK")
            self.assertEqual(flattened["Audit report"], "OK")
            self.assertEqual(flattened["Portainer"], "WARNING")
            self.assertEqual(flattened["Samba"], "WARNING")
            self.assertEqual(flattened["Windows/SMB validation"], "PENDING")
            self.assertEqual(flattened["PostgreSQL exposure"], "OK")
            self.assertEqual(flattened["srv-recursos backups"], "OK")
            self.assertEqual(report.overall_status, "WARNING")

    def test_pre_release_smb_validation_overrides_historical_pending_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write(root, EVIDENCE_SRV_SERVICIOS, "OK: Docker activo\n5432 no escucha en el host\n")
            self._write(root, EVIDENCE_SRV_RECURSOS, "OK: Samba activo\n")
            self._write(
                root,
                EVIDENCE_AUDIT_REPORT,
                "\n".join(
                    [
                        "apto para dry-run",
                        "Portainer publica 8000",
                        "falta validar Samba desde un cliente Windows",
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
                    ]
                ),
            )
            self._write(root, "docs/arquitectura.md", "Frankie architecture")

            report = build_status_report(FrankiePaths(root))
            flattened = {item.name: item.state for section in report.sections for item in section.items}

            self.assertEqual(flattened["Portainer"], "WARNING")
            self.assertEqual(flattened["Samba"], "OK")
            self.assertEqual(flattened["Windows/SMB validation"], "OK")
            self.assertEqual(report.overall_status, "WARNING")

    def _write(self, root: Path, relative_path: str, content: str) -> None:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
