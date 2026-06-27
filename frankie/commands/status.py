from __future__ import annotations

from frankie.core.status import build_status_report
from frankie.evidence.loader import load_structured_evidence
from frankie.output.console import render_status
from frankie.output.json_output import render_status_json


def run(json_output: bool = False) -> str:
    report = build_status_report()
    if json_output:
        return render_status_json(report, load_structured_evidence())
    return render_status(report)
