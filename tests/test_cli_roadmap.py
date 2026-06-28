from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from frankie.commands import evidence
from frankie.evidence.models import EvidenceLoadResult


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class EvidenceCommandTests(unittest.TestCase):
    def test_evidence_list(self) -> None:
        result = run_frankie("evidence", "list")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Structured evidences", result.stdout)
        self.assertIn("samba-validation-current", result.stdout)
        self.assertIn("portainer-port-8000-warning", result.stdout)

    def test_evidence_validate(self) -> None:
        result = run_frankie("evidence", "validate")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Valid: 7", result.stdout)
        self.assertIn("Invalid: 0", result.stdout)
        self.assertIn("Result: PASS", result.stdout)

    def test_evidence_summary_text(self) -> None:
        result = run_frankie("evidence", "summary")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Structured evidence summary", result.stdout)
        self.assertIn("Total: 7", result.stdout)
        self.assertIn("Status:", result.stdout)
        self.assertIn("Mode:", result.stdout)

    def test_evidence_summary_json(self) -> None:
        result = run_frankie("evidence", "summary", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["command"], "evidence summary")
        self.assertEqual(payload["total"], 7)
        self.assertEqual(payload["by_mode"], {"offline": 7})
        self.assertIn("Samba / SMB", payload["by_component"])

    def test_evidence_validate_reports_unavailable_directory(self) -> None:
        unavailable = EvidenceLoadResult(False, "docs/evidencias/structured", (), ())

        with patch.object(evidence, "load_structured_evidence", return_value=unavailable):
            output, exit_code = evidence.dispatch("validate")

        self.assertEqual(exit_code, 1)
        self.assertIn("Result: WARN", output)

    def test_evidence_show_text(self) -> None:
        result = run_frankie("evidence", "show", "samba-validation-current")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Evidence id: samba-validation-current", result.stdout)
        self.assertIn("Status: OK", result.stdout)
        self.assertIn("Severity: INFO", result.stdout)

    def test_evidence_show_json(self) -> None:
        result = run_frankie("evidence", "show", "samba-validation-current", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["evidence_id"], "samba-validation-current")
        self.assertEqual(payload["component"]["id"], "samba")
        self.assertEqual(payload["status"], "OK")

    def test_missing_evidence_is_controlled(self) -> None:
        result = run_frankie("evidence", "show", "missing-id")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("Evidence not found: missing-id", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class CliErrorTests(unittest.TestCase):
    def test_evidence_requires_an_action(self) -> None:
        result = run_frankie("evidence")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Evidence action required", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_evidence_rejects_unknown_action(self) -> None:
        result = run_frankie("evidence", "unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unknown evidence action", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_evidence_show_requires_id(self) -> None:
        result = run_frankie("evidence", "show")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Evidence id required", result.stderr)

    def test_bad_flag_is_reported_without_traceback(self) -> None:
        result = run_frankie("status", "--badflag")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unrecognized arguments", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_help_lists_complete_cli(self) -> None:
        result = run_frankie("help")
        for text in (
            "frankie inventory [--json]",
            "frankie doctor [--verbose] [--json]",
            "frankie evidence list",
            "frankie evidence validate",
            "frankie evidence summary [--json]",
            "frankie evidence show <evidence_id> [--json]",
            "frankie report [--markdown | --json] [--output <path>] [--force]",
            "All commands run offline.",
            "No command connects to the Frankie physical server.",
        ):
            self.assertIn(text, result.stdout)
