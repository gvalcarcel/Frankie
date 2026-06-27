"""Structured evidence models and read-only loading."""

from frankie.evidence.loader import load_structured_evidence
from frankie.evidence.models import EvidenceLoadIssue, EvidenceLoadResult, StructuredEvidence

__all__ = (
    "EvidenceLoadIssue",
    "EvidenceLoadResult",
    "StructuredEvidence",
    "load_structured_evidence",
)
