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


class HelpCommandTests(unittest.TestCase):
    def test_help_returns_zero(self) -> None:
        result = run_frankie("help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Available commands:", result.stdout)
        self.assertIn("Planned commands:", result.stdout)

    def test_no_arguments_shows_help(self) -> None:
        result = run_frankie()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Frankie Core is the foundation package", result.stdout)
