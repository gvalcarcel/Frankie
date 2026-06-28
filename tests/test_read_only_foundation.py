from __future__ import annotations

import ast
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = REPO_ROOT / "frankie"
FORBIDDEN_CALLS = {
    "open",
    "exec",
    "eval",
}
FORBIDDEN_ATTRS = {
    "run",
    "Popen",
    "call",
    "check_call",
    "check_output",
    "remove",
    "unlink",
    "rmdir",
    "rmtree",
    "replace",
    "rename",
    "write_text",
    "write_bytes",
}
REPORT_WRITER = PACKAGE_ROOT / "reports" / "writer.py"


class ReadOnlyFoundationTests(unittest.TestCase):
    def test_foundation_has_no_unapproved_write_or_subprocess_operations(self) -> None:
        for path in PACKAGE_ROOT.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    self._assert_call_is_safe(path, node)

    def _assert_call_is_safe(self, path: Path, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Name):
            self.assertNotIn(func.id, FORBIDDEN_CALLS, f"{path} uses {func.id}()")
        if isinstance(func, ast.Attribute):
            if path == REPORT_WRITER and func.attr == "write_text":
                return
            self.assertNotIn(func.attr, FORBIDDEN_ATTRS, f"{path} uses .{func.attr}()")
