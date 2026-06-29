from __future__ import annotations

from collections.abc import Iterable

from frankie.evidence.models import EvidenceLoadResult, EvidenceSummary, LiveEvidenceSummary


def summarize_evidence(result: EvidenceLoadResult) -> EvidenceSummary:
    evidence = result.evidence
    live = tuple(item for item in evidence if item.mode in {"live-readonly", "live-controlled"})
    return EvidenceSummary(
        total=len(evidence),
        invalid=len(result.issues),
        by_status=_count(item.status for item in evidence),
        by_severity=_count(item.severity for item in evidence),
        by_component=_count(item.component_name for item in evidence),
        by_evidence_type=_count(item.evidence_type for item in evidence),
        by_data_source=_count(item.data_source for item in evidence),
        by_mode=_count(item.mode for item in evidence),
        live_evidence=LiveEvidenceSummary(
            total=len(live),
            readonly_captures=sum(item.evidence_type == "live_readonly_capture" for item in live),
            access_cleanup=sum(item.evidence_type == "live_access_cleanup" for item in live),
            server_contacted=any(item.details.get("server_contacted") is True for item in live),
            changes_made=any(item.details.get("changes_made") is True for item in live),
            temporary_access_removed=any(
                item.details.get("temporary_access_removed") is True for item in live
            ),
            evidence_ids=tuple(item.evidence_id for item in live),
        ),
    )


def _count(values: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))
