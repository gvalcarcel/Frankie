from __future__ import annotations

from frankie.live.models import LiveCheckResult, LiveCommandPlan, LiveEvidenceCandidate


def simulate(plan: LiveCommandPlan) -> LiveCheckResult:
    if not plan.simulated or plan.enabled:
        raise ValueError("Simulator requires a disabled simulation plan.")
    is_audit = plan.command_type == "live-audit"
    candidate = LiveEvidenceCandidate(
        candidate_id=f"simulated-{plan.command_type}-candidate",
        evidence_type="simulated_live_candidate",
        simulated=True,
        publishable=False,
        summary="Fictitious candidate for contract testing only; it is not real infrastructure evidence.",
    )
    details = {
        "scenario": "offline-format-simulation",
        "checks": ["guard-state", "output-contract"],
        "observations": [
            "No target address exists in this simulation.",
            "No service state was observed.",
            "All displayed values are fictitious and sanitized.",
        ],
    }
    return LiveCheckResult(
        check_id="SIM-LIVE-AUDIT-001" if is_audit else "SIM-LIVE-STATUS-001",
        component="simulated-infrastructure",
        command_type=plan.command_type,
        mode="simulation",
        enabled=False,
        simulated=True,
        server_contacted=False,
        status="SIMULATED",
        severity="INFO",
        summary="Offline simulation completed. This result does not represent Frankie state.",
        details=details,
        evidence_candidate=candidate,
        risks=("Simulated output could be mistaken for real evidence if its disclaimer is removed.",),
        next_steps=("Use a future authorized LIVE Work Order before implementing any real transport.",),
    )
