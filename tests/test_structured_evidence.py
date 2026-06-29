from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from frankie.core.paths import FrankiePaths
from frankie.evidence.loader import LIVE_EVIDENCE_GLOB, STRUCTURED_EVIDENCE_DIRECTORY, load_structured_evidence


REPO_ROOT = Path(__file__).resolve().parents[1]
STRUCTURED_ROOT = REPO_ROOT / STRUCTURED_EVIDENCE_DIRECTORY


def valid_payload(evidence_id: str = "test-evidence") -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "evidence_id": evidence_id,
        "evidence_type": "test",
        "component": {"id": "test", "name": "Test component"},
        "status": "OK",
        "severity": "INFO",
        "mode": "offline",
        "data_source": "documented_evidence",
        "summary": "Safe test evidence.",
        "details": {},
        "references": ["docs/example.md"],
        "server_impact": {
            "touches_physical_server": False,
            "requires_live_connection": False,
            "changes_configuration": False,
        },
        "security": {
            "contains_secrets": False,
            "contains_credentials": False,
            "contains_internal_ips": False,
        },
        "recommendation": "No action required.",
    }


def valid_live_payload(evidence_id: str = "test-live") -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "evidence_id": evidence_id,
        "evidence_type": "live_readonly_capture",
        "captured_at": "2026-06-29T10:00:00+02:00",
        "mode": "live-readonly",
        "server_contacted": True,
        "changes_made": False,
        "components": [],
        "findings": [],
        "sanitization": {
            "internal_ips_removed": True,
            "usernames_removed": True,
            "secrets_removed": True,
            "raw_outputs_committed": False,
        },
    }


def write_live_payload(root: Path, payload: dict[str, object]) -> None:
    directory = root / "docs" / "evidencias" / "frankie-core-v0.8.0" / "wo-live-test"
    directory.mkdir(parents=True)
    (directory / "structured_test.json").write_text(json.dumps(payload), encoding="utf-8")


class StructuredEvidenceLoaderTests(unittest.TestCase):
    def test_loader_reads_repository_evidence(self) -> None:
        result = load_structured_evidence(FrankiePaths(REPO_ROOT))

        self.assertTrue(result.available)
        self.assertEqual(len(result.evidence), 9)
        self.assertEqual(result.issues, ())
        self.assertEqual(
            {item.evidence_id for item in result.evidence},
            {
                "frankie-core-current",
                "samba-validation-current",
                "portainer-port-8000-warning",
                "audit-summary-current",
                "release-v0.6.0-published",
                "offline-live-strategy-current",
                "wo-0019-evidence-report-validation",
                "wo-live-0001-real-state-capture",
                "wo-live-0002-temporary-access-removal",
            },
        )
        self.assertEqual(result.warnings, ())

    def test_missing_directory_returns_controlled_empty_result(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = load_structured_evidence(FrankiePaths(Path(tmp)))

        self.assertFalse(result.directory_available)
        self.assertFalse(result.available)
        self.assertEqual(result.evidence, ())
        self.assertEqual(result.issues, ())

    def test_invalid_json_is_reported_without_breaking_valid_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / STRUCTURED_EVIDENCE_DIRECTORY
            directory.mkdir(parents=True)
            (directory / "valid.json").write_text(json.dumps(valid_payload()), encoding="utf-8")
            (directory / "invalid.json").write_text("{invalid", encoding="utf-8")

            result = load_structured_evidence(FrankiePaths(root))

        self.assertTrue(result.available)
        self.assertEqual(len(result.evidence), 1)
        self.assertEqual(len(result.issues), 1)
        self.assertTrue(result.issues[0].path.endswith("invalid.json"))

    def test_missing_required_field_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / STRUCTURED_EVIDENCE_DIRECTORY
            directory.mkdir(parents=True)
            payload = valid_payload()
            del payload["status"]
            (directory / "missing.json").write_text(json.dumps(payload), encoding="utf-8")

            result = load_structured_evidence(FrankiePaths(root))

        self.assertFalse(result.available)
        self.assertEqual(len(result.issues), 1)
        self.assertIn("status", result.issues[0].message)

    def test_sensitive_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / STRUCTURED_EVIDENCE_DIRECTORY
            directory.mkdir(parents=True)
            payload = valid_payload()
            payload["security"]["contains_secrets"] = True  # type: ignore[index]
            (directory / "unsafe.json").write_text(json.dumps(payload), encoding="utf-8")

            result = load_structured_evidence(FrankiePaths(root))

        self.assertFalse(result.available)
        self.assertEqual(len(result.issues), 1)
        self.assertIn("sensitive data", result.issues[0].message)

    def test_duplicate_evidence_id_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / STRUCTURED_EVIDENCE_DIRECTORY
            directory.mkdir(parents=True)
            payload = valid_payload("duplicate-id")
            (directory / "first.json").write_text(json.dumps(payload), encoding="utf-8")
            (directory / "second.json").write_text(json.dumps(payload), encoding="utf-8")

            result = load_structured_evidence(FrankiePaths(root))

        self.assertEqual(len(result.evidence), 1)
        self.assertEqual(len(result.issues), 1)
        self.assertIn("duplicate evidence_id: duplicate-id", result.issues[0].message)

    def test_unrecognized_vocabulary_and_empty_references_are_reported(self) -> None:
        cases = (("status", "BROKEN"), ("severity", "TRIVIAL"), ("mode", "remote"), ("references", []))
        for field, value in cases:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                directory = root / STRUCTURED_EVIDENCE_DIRECTORY
                directory.mkdir(parents=True)
                payload = valid_payload()
                payload[field] = value
                (directory / "invalid.json").write_text(json.dumps(payload), encoding="utf-8")

                result = load_structured_evidence(FrankiePaths(root))

            self.assertEqual(len(result.issues), 1)
            self.assertIn(field, result.issues[0].message)

    def test_possible_sensitive_value_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / STRUCTURED_EVIDENCE_DIRECTORY
            directory.mkdir(parents=True)
            payload = valid_payload()
            payload["details"] = {"example": "password=not-a-real-password"}
            (directory / "unsafe-value.json").write_text(json.dumps(payload), encoding="utf-8")

            result = load_structured_evidence(FrankiePaths(root))

        self.assertEqual(len(result.issues), 1)
        self.assertIn("possible sensitive data", result.issues[0].message)

    def test_optional_metadata_is_loaded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            directory = root / STRUCTURED_EVIDENCE_DIRECTORY
            directory.mkdir(parents=True)
            payload = valid_payload()
            payload.update(
                {
                    "created_at": "2026-06-28T10:00:00+02:00",
                    "source_files": ["docs/source.md"],
                    "related_checks": ["AUD-TEST-001"],
                }
            )
            (directory / "metadata.json").write_text(json.dumps(payload), encoding="utf-8")

            result = load_structured_evidence(FrankiePaths(root))

        self.assertEqual(result.issues, ())
        self.assertEqual(result.evidence[0].created_at, "2026-06-28T10:00:00+02:00")
        self.assertEqual(result.evidence[0].source_files, ("docs/source.md",))
        self.assertEqual(result.evidence[0].related_checks, ("AUD-TEST-001",))

    def test_loader_detects_sanitized_live_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_live_payload(root, valid_live_payload())

            result = load_structured_evidence(FrankiePaths(root))

        self.assertTrue(result.available)
        self.assertEqual(result.issues, ())
        self.assertEqual(result.evidence[0].mode, "live-readonly")
        self.assertEqual(result.evidence[0].data_source, "sanitized_live_evidence")
        self.assertFalse(result.evidence[0].details["changes_made"])

    def test_loader_rejects_sensitive_live_values(self) -> None:
        unsafe_values = (
            "password=" + "real-value",
            "ssh-" + "ed25519 AAAAC3NzaC1lZDI1NTE5AAAAITestMaterial",
            "10" + ".0.0.1",
            "00" + ":11:22:33:44:55",
            "teacher" + "@example.invalid",
        )
        for unsafe in unsafe_values:
            with self.subTest(unsafe=unsafe), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                payload = valid_live_payload()
                payload["components"] = [{"summary": unsafe}]
                write_live_payload(root, payload)

                result = load_structured_evidence(FrankiePaths(root))

            self.assertEqual(len(result.evidence), 0)
            self.assertEqual(len(result.issues), 1)
            self.assertIn("sensitive data", result.issues[0].message)

    def test_loader_rejects_live_identity_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = valid_live_payload()
            payload["username"] = "example-account"
            write_live_payload(root, payload)

            result = load_structured_evidence(FrankiePaths(root))

        self.assertEqual(len(result.issues), 1)
        self.assertIn("sensitive data", result.issues[0].message)

    def test_loader_rejects_live_raw_output_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = valid_live_payload()
            payload["sanitization"]["raw_outputs_committed"] = True  # type: ignore[index]
            write_live_payload(root, payload)

            result = load_structured_evidence(FrankiePaths(root))

        self.assertEqual(len(result.issues), 1)
        self.assertIn("raw outputs", result.issues[0].message)


class StructuredEvidenceDocumentTests(unittest.TestCase):
    def test_all_evidence_files_are_valid_public_json(self) -> None:
        for path in sorted(STRUCTURED_ROOT.glob("*.json")):
            with self.subTest(path=path.name):
                payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(payload["schema_version"], "1.0")
                self.assertTrue(payload["evidence_id"])
                self.assertTrue(payload["status"])
                self.assertFalse(payload["security"]["contains_secrets"])
                self.assertFalse(payload["security"]["contains_credentials"])
                self.assertFalse(payload["security"]["contains_internal_ips"])

    def test_samba_and_portainer_states_match_known_evidence(self) -> None:
        samba = json.loads((STRUCTURED_ROOT / "samba_validation.json").read_text(encoding="utf-8"))
        portainer = json.loads((STRUCTURED_ROOT / "portainer_warning.json").read_text(encoding="utf-8"))

        self.assertEqual(samba["status"], "OK")
        self.assertEqual(samba["severity"], "INFO")
        self.assertEqual(portainer["status"], "WARNING")
        self.assertEqual(portainer["severity"], "LOW")
        self.assertFalse(portainer["details"]["resolved"])

    def test_live_strategy_requires_explicit_access(self) -> None:
        strategy = json.loads((STRUCTURED_ROOT / "offline_live_strategy.json").read_text(encoding="utf-8"))

        self.assertEqual(strategy["details"]["default_mode"], "OFFLINE")
        self.assertTrue(strategy["details"]["live_requires_explicit_access"])
        self.assertFalse(strategy["details"]["live_mode_implemented"])
