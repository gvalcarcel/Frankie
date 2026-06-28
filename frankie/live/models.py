from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LiveSafetyGuard:
    guard_id: str
    passed: bool
    summary: str


@dataclass(frozen=True)
class LiveCommandPlan:
    command_type: str
    mode: str
    enabled: bool
    simulated: bool
    checks: tuple[str, ...]
    guards: tuple[LiveSafetyGuard, ...]


@dataclass(frozen=True)
class LiveEvidenceCandidate:
    candidate_id: str
    evidence_type: str
    simulated: bool
    publishable: bool
    summary: str


@dataclass(frozen=True)
class LiveCheckResult:
    check_id: str
    component: str
    command_type: str
    mode: str
    enabled: bool
    simulated: bool
    server_contacted: bool
    status: str
    severity: str
    summary: str
    details: dict[str, Any]
    evidence_candidate: LiveEvidenceCandidate | None
    risks: tuple[str, ...]
    next_steps: tuple[str, ...]
