from __future__ import annotations

from frankie.evidence.loader import load_structured_evidence
from frankie.evidence.summary import summarize_evidence
from frankie.output.console import (
    render_evidence,
    render_evidence_list,
    render_evidence_summary,
    render_evidence_validation,
)
from frankie.output.json_output import render_evidence_json, render_evidence_summary_json


def dispatch(action: str, evidence_id: str | None = None, json_output: bool = False) -> tuple[str, int]:
    result = load_structured_evidence()

    if action == "list":
        return render_evidence_list(result), 0
    if action == "validate":
        exit_code = 1 if not result.directory_available or result.issues else 0
        return render_evidence_validation(result), exit_code
    if action == "summary":
        summary = summarize_evidence(result)
        output = render_evidence_summary_json(summary) if json_output else render_evidence_summary(summary)
        return output, 0

    selected = next((item for item in result.evidence if item.evidence_id == evidence_id), None)
    if selected is None:
        return f"Evidence not found: {evidence_id}", 1
    if json_output:
        return render_evidence_json(selected), 0
    return render_evidence(selected), 0
