from __future__ import annotations

from frankie.audit.audit_engine import run_audit
from frankie.evidence.loader import load_structured_evidence
from frankie.output.console import render_audit
from frankie.output.json_output import render_audit_json


def run(verbose: bool = False, json_output: bool = False) -> str:
    report = run_audit()
    if json_output:
        return render_audit_json(report, load_structured_evidence(), verbose=verbose)
    return render_audit(report, verbose=verbose)
