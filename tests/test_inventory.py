from __future__ import annotations

import ast
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from frankie.core.paths import FrankiePaths
from frankie.inventory.inventory_reader import build_inventory_report


REPO_ROOT = Path(__file__).resolve().parents[1]
INVENTORY_FLOW_FILES = (
    REPO_ROOT / "frankie" / "commands" / "inventory.py",
    REPO_ROOT / "frankie" / "inventory" / "inventory_reader.py",
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


class InventoryCommandTests(unittest.TestCase):
    def test_inventory_returns_zero(self) -> None:
        result = run_frankie("inventory")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_inventory_output_contains_required_header(self) -> None:
        result = run_frankie("inventory")
        self.assertIn("Frankie Inventory", result.stdout)
        self.assertIn("Version: 0.8.0-dev", result.stdout)
        self.assertIn("Mode: read-only foundation", result.stdout)

    def test_inventory_distinguishes_physical_server_core_and_repository(self) -> None:
        result = run_frankie("inventory")
        self.assertIn("Physical server", result.stdout)
        self.assertIn("Name.......................... Frankie", result.stdout)
        self.assertIn("Frankie Core", result.stdout)
        self.assertIn("Read-only software tool", result.stdout)
        self.assertIn("Repository", result.stdout)
        self.assertIn("Documentation, scripts, evidence and source code", result.stdout)

    def test_inventory_contains_known_infrastructure(self) -> None:
        result = run_frankie("inventory")
        for expected in (
            "srv-servicios",
            "srv-recursos",
            "Docker",
            "Samba",
            "aula-network",
            "/srv/recursos",
            "srv-recursos backup evidence",
            "PostgreSQL",
            "not exposed on host port 5432",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, result.stdout)

    def test_missing_evidence_does_not_break_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = build_inventory_report(FrankiePaths(Path(tmp)))
            states = [item.state for section in report.sections for item in section.items]

            self.assertIn("MISSING EVIDENCE", states)
            self.assertIn("UNKNOWN", states)

    def test_inventory_flow_has_no_subprocess_or_write_operations(self) -> None:
        forbidden_names = {"open"}
        forbidden_attrs = {"run", "Popen", "write_text", "write_bytes", "unlink", "remove"}

        for path in INVENTORY_FLOW_FILES:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, forbidden_names, f"{path} uses {node.func.id}()")
                    if isinstance(node.func, ast.Attribute):
                        self.assertNotIn(node.func.attr, forbidden_attrs, f"{path} uses .{node.func.attr}()")
