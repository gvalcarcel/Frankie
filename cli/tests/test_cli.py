from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI_DIR = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=CLI_DIR,
        text=True,
        capture_output=True,
        check=False,
    )


class FrankieCliTests(unittest.TestCase):
    def test_version_command_reports_read_only_mode(self) -> None:
        result = run_cli("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Frankie CLI", result.stdout)
        self.assertIn("mode: read-only", result.stdout)

    def test_help_command_lists_initial_commands(self) -> None:
        result = run_cli("help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("version", "status", "inventory", "audit", "help"):
            self.assertIn(f"frankie {command}", result.stdout)

    def test_inventory_json_is_valid(self) -> None:
        result = run_cli("inventory", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["data"]["mode"], "read-only")
        self.assertEqual(len(payload["data"]["targets"]), 2)

    def test_audit_does_not_execute_scripts_by_default(self) -> None:
        result = run_cli("audit")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("execution: not executed by default", result.stdout)
        self.assertIn("scripts/auditoria/auditar_srv-servicios.sh", result.stdout)

    def test_output_writes_only_when_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "status.md"
            result = run_cli("status", "--format", "markdown", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists())
            self.assertIn("# Frankie Status", output.read_text(encoding="utf-8"))

    def test_output_does_not_overwrite_existing_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "status.md"
            output.write_text("existing\n", encoding="utf-8")
            result = run_cli("status", "--format", "markdown", "--output", str(output))
            self.assertEqual(result.returncode, 2)
            self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
