from __future__ import annotations

from collections.abc import Iterable

from frankie.evidence.models import EvidenceLoadResult, EvidenceSummary, StructuredEvidence


def summarize_evidence(result: EvidenceLoadResult) -> EvidenceSummary:
    evidence = result.evidence
    return EvidenceSummary(
        total=len(evidence),
        invalid=len(result.issues),
        by_status=_count(item.status for item in evidence),
        by_severity=_count(item.severity for item in evidence),
        by_component=_count(item.component_name for item in evidence),
        by_evidence_type=_count(item.evidence_type for item in evidence),
        by_data_source=_count(item.data_source for item in evidence),
        by_mode=_count(item.mode for item in evidence),
    )


def _count(values: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))
