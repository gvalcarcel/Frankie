from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class NotImplementedCommandTests(unittest.TestCase):
    def test_no_foundation_commands_remain_as_placeholders(self) -> None:
        result = run_frankie("help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Planned commands:", result.stdout)
        self.assertIn("  none", result.stdout)

        for command in ("status", "inventory", "audit", "doctor"):
            with self.subTest(command=command):
                command_result = run_frankie(command)
                self.assertEqual(command_result.returncode, 0, command_result.stderr)
                self.assertNotIn("is not implemented yet", command_result.stdout)

    def test_unknown_command_returns_clear_error(self) -> None:
        result = run_frankie("unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unknown command: unknown", result.stderr)
        self.assertIn("frankie help", result.stderr)
