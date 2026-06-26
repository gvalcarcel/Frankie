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
    def test_future_commands_report_not_implemented(self) -> None:
        for command in ("doctor",):
            with self.subTest(command=command):
                result = run_frankie(command)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(
                    f"Command '{command}' is not implemented yet in v0.6.0 foundation.",
                    result.stdout,
                )
                self.assertIn("planned for a future iteration", result.stdout)

    def test_unknown_command_returns_clear_error(self) -> None:
        result = run_frankie("unknown")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Unknown command: unknown", result.stderr)
        self.assertIn("frankie help", result.stderr)
