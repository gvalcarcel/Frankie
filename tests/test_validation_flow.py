from __future__ import annotations

import argparse
import ast
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from scripts.validation.validate_evidence_flow import (
    ValidationFlowError,
    _build_validation_evidence,
    _resolve_output_dir,
    _validate_evidence_payload,
    _write_text,
    build_parser,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validation" / "validate_evidence_flow.py"


class ValidationFlowUnitTests(unittest.TestCase):
    def test_output_is_restricted_to_evidence_directory(self) -> None:
        generated_at = datetime(2026, 6, 28, tzinfo=timezone.utc)

        with self.assertRaises(ValidationFlowError):
            _resolve_output_dir(REPO_ROOT, "README.md", generated_at)

        output = _resolve_output_dir(REPO_ROOT, "docs/evidencias/test-run", generated_at)
        self.assertEqual(output, (REPO_ROOT / "docs/evidencias/test-run").resolve())

    def test_default_output_has_deterministic_utc_shape(self) -> None:
        generated_at = datetime(2026, 6, 28, 10, 30, 45, tzinfo=timezone.utc)

        output = _resolve_output_dir(REPO_ROOT, None, generated_at)

        self.assertEqual(
            output,
            (REPO_ROOT / "docs/evidencias/frankie-core-v0.8.0/validation-runs/20260628T103045Z").resolve(),
        )

    def test_writer_requires_force_for_existing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "artifact.md"
            _write_text(path, "first", False)

            with self.assertRaises(ValidationFlowError):
                _write_text(path, "second", False)

            _write_text(path, "second", True)
            self.assertEqual(path.read_text(encoding="utf-8"), "second\n")

    def test_writer_rejects_symbolic_link_artifact(self) -> None:
        path = Path("docs/evidencias/link.json")

        with patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaises(ValidationFlowError):
                _write_text(path, "unsafe", True)

    def test_generated_evidence_passes_the_real_loader(self) -> None:
        payload = _build_validation_evidence(
            generated_at="2026-06-28T12:00:00+02:00",
            output_relative="docs/evidencias/frankie-core-v0.8.0/test-run",
            test_count=84,
            evidence_total=7,
            report_hashes={"consolidated_report.md": "A" * 64, "consolidated_report.json": "B" * 64},
            baseline_clean=True,
        )

        _validate_evidence_payload(payload)

        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["mode"], "offline")
        self.assertFalse(any(payload["security"].values()))
        self.assertFalse(any(payload["server_impact"].values()))

    def test_parser_exposes_safety_controls(self) -> None:
        parser = build_parser()

        parsed = parser.parse_args(["--output-dir", "docs/evidencias/run", "--force", "--require-clean"])

        self.assertIsInstance(parsed, argparse.Namespace)
        self.assertTrue(parsed.force)
        self.assertTrue(parsed.require_clean)

    def test_script_does_not_use_shell_or_network_calls(self) -> None:
        tree = ast.parse(SCRIPT_PATH.read_text(encoding="utf-8"), filename=str(SCRIPT_PATH))
        forbidden_attributes = {"system", "connect", "create_connection", "urlopen"}
        for node in ast.walk(tree):
            if isinstance(node, ast.keyword) and node.arg == "shell":
                self.fail("Validation flow must not pass shell= to subprocess calls.")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotIn(node.func.attr, forbidden_attributes)


if __name__ == "__main__":
    unittest.main()
