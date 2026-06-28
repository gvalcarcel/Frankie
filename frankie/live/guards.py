from __future__ import annotations

from frankie.live.models import LiveCommandPlan, LiveSafetyGuard


class LiveModeBlockedError(RuntimeError):
    """Raised when code attempts to cross the disabled Live Mode boundary."""


def build_disabled_plan(command_type: str, simulated: bool) -> LiveCommandPlan:
    if command_type not in {"live-status", "live-audit"}:
        raise LiveModeBlockedError("Unsupported Live Mode command.")
    guards = (
        LiveSafetyGuard("LIVE-DISABLED", True, "Live Mode is disabled by default."),
        LiveSafetyGuard("NO-CREDENTIALS", True, "No credentials are accepted or read."),
        LiveSafetyGuard("NO-NETWORK", True, "No network operations are available."),
        LiveSafetyGuard("NO-SUBPROCESS", True, "No external commands are available."),
        LiveSafetyGuard("NO-WRITES", True, "No runtime writes are available."),
        LiveSafetyGuard("NO-REPAIR", True, "Repair operations are outside this architecture."),
    )
    return LiveCommandPlan(
        command_type=command_type,
        mode="simulation" if simulated else "live-disabled",
        enabled=False,
        simulated=simulated,
        checks=("format-contract", "safety-guards") if simulated else (),
        guards=guards,
    )


def reject_real_activation(enabled: bool) -> None:
    if enabled:
        raise LiveModeBlockedError("Live Mode activation is not implemented or authorized.")
