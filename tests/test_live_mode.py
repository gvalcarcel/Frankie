from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

from frankie.live.guards import LiveModeBlockedError, reject_real_activation


REPO_ROOT = Path(__file__).resolve().parents[1]
LIVE_ROOT = REPO_ROOT / "frankie" / "live"
RUNTIME_FILES = (*LIVE_ROOT.glob("*.py"), REPO_ROOT / "frankie" / "commands" / "live.py")


def run_frankie(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "frankie", *args],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class DisabledLiveCommandTests(unittest.TestCase):
    def test_text_commands_are_blocked_without_contact(self) -> None:
        for command in ("live-status", "live-audit"):
            with self.subTest(command=command):
                result = run_frankie(command)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("Live Mode is not enabled", result.stdout)
                self.assertIn("No server has been contacted", result.stdout)
                self.assertIn("No live command has been executed", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_json_commands_are_blocked_with_stable_contract(self) -> None:
        for command in ("live-status", "live-audit"):
            with self.subTest(command=command):
                result = run_frankie(command, "--json")
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["command"], command)
                self.assertEqual(payload["mode"], "live-disabled")
                self.assertEqual(payload["status"], "BLOCKED")
                self.assertFalse(payload["enabled"])
                self.assertFalse(payload["connected"])
                self.assertFalse(payload["server_contacted"])
                self.assertFalse(payload["simulated"])

    def test_simulated_text_is_explicitly_fictitious(self) -> None:
        for command in ("live-status", "live-audit"):
            result = run_frankie(command, "--simulate")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("offline simulation", result.stdout)
            self.assertIn("does not represent the real state", result.stdout)
            self.assertIn("Server contacted: false", result.stdout)

    def test_simulated_json_never_claims_activation_or_contact(self) -> None:
        for command in ("live-status", "live-audit"):
            result = run_frankie(command, "--simulate", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["mode"], "simulation")
            self.assertEqual(payload["status"], "SIMULATED")
            self.assertTrue(payload["simulated"])
            self.assertFalse(payload["enabled"])
            self.assertFalse(payload["connected"])
            self.assertFalse(payload["server_contacted"])
            self.assertTrue(payload["evidence_candidate"]["simulated"])
            self.assertFalse(payload["evidence_candidate"]["publishable"])

    def test_real_activation_is_rejected(self) -> None:
        with self.assertRaises(LiveModeBlockedError):
            reject_real_activation(True)

    def test_simulate_flag_is_rejected_for_offline_commands(self) -> None:
        result = run_frankie("status", "--simulate")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Simulation is not available", result.stderr)

    def test_help_marks_live_commands_as_disabled(self) -> None:
        result = run_frankie("help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("live-status [--json] [--simulate]", result.stdout)
        self.assertIn("live-audit [--json] [--simulate]", result.stdout)
        self.assertIn("prepared but disabled", result.stdout)
        self.assertIn("future authorized LIVE Work Order", result.stdout)

    def test_live_runtime_has_no_dangerous_imports_or_calls(self) -> None:
        forbidden_imports = {"subprocess", "socket", "requests", "paramiko", "docker", "os", "pathlib"}
        forbidden_calls = {"open", "exec", "eval"}
        forbidden_attrs = {"system", "run", "Popen", "connect", "getenv", "write_text", "write_bytes"}
        for path in RUNTIME_FILES:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertNotIn(alias.name.split(".")[0], forbidden_imports, str(path))
                if isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotIn(node.module.split(".")[0], forbidden_imports, str(path))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, forbidden_calls, str(path))
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, forbidden_attrs, str(path))


if __name__ == "__main__":
    unittest.main()
