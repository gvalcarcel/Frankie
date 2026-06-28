"""Structured evidence models and read-only loading."""

from frankie.evidence.loader import load_structured_evidence
from frankie.evidence.models import EvidenceLoadIssue, EvidenceLoadResult, EvidenceSummary, StructuredEvidence
from frankie.evidence.summary import summarize_evidence

__all__ = (
    "EvidenceLoadIssue",
    "EvidenceLoadResult",
    "EvidenceSummary",
    "StructuredEvidence",
    "load_structured_evidence",
    "summarize_evidence",
)
