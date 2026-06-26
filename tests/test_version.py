from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from frankie.core.constants import MODE, VERSION


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class VersionCommandTests(unittest.TestCase):
    def test_version_returns_zero(self) -> None:
        result = run_frankie("version")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Frankie Core {VERSION}", result.stdout)
        self.assertIn(f"Mode: {MODE}", result.stdout)
        self.assertIn("This version does not modify servers or services.", result.stdout)

    def test_version_comes_from_central_constant(self) -> None:
        self.assertEqual(VERSION, "0.6.0-dev")
