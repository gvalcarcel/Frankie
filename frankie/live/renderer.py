from __future__ import annotations

import json
from dataclasses import asdict

from frankie.core.constants import VERSION
from frankie.live.models import LiveCheckResult


def render_live_text(result: LiveCheckResult) -> str:
    if result.simulated:
        return "\n".join(
            [
                "Frankie Live Mode simulation",
                "",
                "This is an offline simulation for output-contract testing.",
                "It does not represent the real state of Frankie.",
                "No server has been contacted.",
                "No live command has been executed.",
                "",
                f"Command: {result.command_type}",
                f"Status: {result.status}",
                "Enabled: false",
                "Simulated: true",
                "Server contacted: false",
            ]
        )
    return "\n".join(
        [
            "Frankie Live Mode is not enabled.",
            "",
            "This command is prepared for future read-only checks, but it cannot connect to Frankie yet.",
            "No server has been contacted.",
            "No live command has been executed.",
            "",
            "Use a future LIVE Work Order to enable and validate this safely.",
        ]
    )


def live_payload(result: LiveCheckResult) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "command": result.command_type,
        "frankie_core_version": VERSION,
        "mode": result.mode,
        "enabled": result.enabled,
        "simulated": result.simulated,
        "connected": False,
        "server_contacted": result.server_contacted,
        "status": result.status,
        "severity": result.severity,
        "reason": "Live Mode is not enabled" if not result.simulated else "Offline simulation requested",
        "message": "No server has been contacted.",
        "check_id": result.check_id,
        "component": result.component,
        "summary": result.summary,
        "details": result.details,
        "evidence_candidate": asdict(result.evidence_candidate) if result.evidence_candidate else None,
        "risks": list(result.risks),
        "next_steps": list(result.next_steps),
    }


def render_live_json(result: LiveCheckResult) -> str:
    return json.dumps(live_payload(result), ensure_ascii=False, indent=2)
