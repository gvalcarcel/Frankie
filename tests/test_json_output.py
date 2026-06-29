from __future__ import annotations

import json
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


class StatusJsonTests(unittest.TestCase):
    def test_status_json_contract(self) -> None:
        result = run_frankie("status", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["command"], "status")
        self.assertEqual(payload["frankie_core_version"], "0.8.0-dev")
        self.assertEqual(payload["mode"], "offline")
        self.assertEqual(payload["data_source"], "structured_and_documented_evidence")
        self.assertTrue(payload["structured_evidence"]["available"])
        self.assertEqual(payload["structured_evidence"]["loaded"], 9)
        self.assertEqual(payload["overall_status"], "WARNING")
        self.assertIsInstance(payload["components"], list)

    def test_status_json_contains_samba_and_portainer_states(self) -> None:
        payload = json.loads(run_frankie("status", "--json").stdout)
        components = {item["id"]: item for item in payload["components"]}

        self.assertEqual(components["samba"]["status"], "OK")
        self.assertEqual(components["samba"]["severity"], "INFO")
        self.assertEqual(components["portainer"]["status"], "WARNING")
        self.assertEqual(components["portainer"]["severity"], "LOW")

    def test_status_text_output_remains_human_readable(self) -> None:
        result = run_frankie("status")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Frankie Status", result.stdout)
        self.assertIn("Overall status: WARNING", result.stdout)


class AuditJsonTests(unittest.TestCase):
    def test_audit_json_contract(self) -> None:
        result = run_frankie("audit", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["command"], "audit")
        self.assertEqual(payload["frankie_core_version"], "0.8.0-dev")
        self.assertEqual(payload["mode"], "offline")
        self.assertEqual(payload["data_source"], "structured_and_documented_evidence")
        self.assertTrue(payload["structured_evidence"]["available"])
        self.assertEqual(payload["structured_evidence"]["loaded"], 9)
        self.assertEqual(payload["overall_result"], "WARN")
        self.assertEqual(payload["counts"]["total"], 7)
        self.assertEqual(payload["counts"]["pass"], 6)
        self.assertEqual(payload["counts"]["warn"], 1)
        self.assertIsInstance(payload["checks"], list)

    def test_audit_json_contains_samba_and_portainer_findings(self) -> None:
        payload = json.loads(run_frankie("audit", "--json").stdout)
        checks = {item["id"]: item for item in payload["checks"]}

        self.assertEqual(checks["AUD-SAMBA-001"]["status"], "PASS")
        self.assertEqual(checks["AUD-SAMBA-001"]["severity"], "INFO")
        self.assertEqual(checks["AUD-SERVICES-PORTAINER-001"]["status"], "WARN")
        self.assertEqual(checks["AUD-SERVICES-PORTAINER-001"]["severity"], "LOW")

    def test_verbose_audit_json_adds_detail_without_mixing_text(self) -> None:
        regular = json.loads(run_frankie("audit", "--json").stdout)
        result = run_frankie("audit", "--verbose", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        verbose = json.loads(result.stdout)
        self.assertEqual(len(verbose["checks"]), len(regular["checks"]))
        self.assertNotIn("description", regular["checks"][0])
        self.assertIn("description", verbose["checks"][0])
        self.assertIn("category", verbose["checks"][0])
        self.assertIn("limitation", verbose["checks"][0])

    def test_audit_text_modes_remain_human_readable(self) -> None:
        regular = run_frankie("audit")
        verbose = run_frankie("audit", "--verbose")

        self.assertEqual(regular.returncode, 0, regular.stderr)
        self.assertEqual(verbose.returncode, 0, verbose.stderr)
        self.assertIn("Overall audit result: WARN", regular.stdout)
        self.assertIn("Description:", verbose.stdout)


class JsonAvailabilityTests(unittest.TestCase):
    def test_json_is_rejected_for_commands_not_in_scope(self) -> None:
        for command in ("version", "help"):
            with self.subTest(command=command):
                result = run_frankie(command, "--json")
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("JSON output is not available", result.stderr)


class InventoryJsonTests(unittest.TestCase):
    def test_inventory_json_contract(self) -> None:
        result = run_frankie("inventory", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["command"], "inventory")
        self.assertEqual(payload["frankie_core_version"], "0.8.0-dev")
        self.assertEqual(payload["mode"], "offline")
        self.assertIsInstance(payload["items"], list)
        values = {item["value"] for item in payload["items"]}
        self.assertIn("Frankie", values)
        self.assertIn("srv-servicios", values)
        self.assertIn("srv-recursos", values)


class DoctorJsonTests(unittest.TestCase):
    def test_doctor_json_contract(self) -> None:
        result = run_frankie("doctor", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["command"], "doctor")
        self.assertEqual(payload["frankie_core_version"], "0.8.0-dev")
        self.assertEqual(payload["mode"], "offline")
        self.assertEqual(payload["overall_diagnosis"], "ACTIONS_RECOMMENDED")
        self.assertEqual(payload["issues_reviewed"], 1)
        self.assertEqual(payload["issues"][0]["issue_id"], "AUD-SERVICES-PORTAINER-001")
        self.assertNotIn("AUD-SAMBA-001", {item["issue_id"] for item in payload["issues"]})

    def test_verbose_doctor_json_adds_resolved_context(self) -> None:
        regular = json.loads(run_frankie("doctor", "--json").stdout)
        result = run_frankie("doctor", "--verbose", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        verbose = json.loads(result.stdout)
        self.assertNotIn("resolved_checks", regular)
        self.assertIn("AUD-SAMBA-001 (PASS; no active action)", verbose["resolved_checks"])
        self.assertIn("result", verbose["issues"][0])
