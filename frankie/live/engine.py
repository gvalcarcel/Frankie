from __future__ import annotations

from frankie.live.guards import build_disabled_plan, reject_real_activation
from frankie.live.models import LiveCheckResult
from frankie.live.simulator import simulate


def run_live_command(command_type: str, simulated: bool = False) -> LiveCheckResult:
    reject_real_activation(False)
    plan = build_disabled_plan(command_type, simulated)
    if simulated:
        return simulate(plan)
    return LiveCheckResult(
        check_id="LIVE-AUDIT-DISABLED" if command_type == "live-audit" else "LIVE-STATUS-DISABLED",
        component="frankie-live-mode",
        command_type=command_type,
        mode="live-disabled",
        enabled=False,
        simulated=False,
        server_contacted=False,
        status="BLOCKED",
        severity="INFO",
        summary="Live Mode is not enabled.",
        details={"reason": "Live Mode is not enabled", "server_contacted": False},
        evidence_candidate=None,
        risks=("No real-state conclusion can be made from a blocked command.",),
        next_steps=("Use a future LIVE Work Order to enable and validate this safely.",),
    )
