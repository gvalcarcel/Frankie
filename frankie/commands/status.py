from __future__ import annotations

from frankie.core.status import build_status_report
from frankie.output.console import render_status
from frankie.output.json_output import render_status_json


def run(json_output: bool = False) -> str:
    report = build_status_report()
    if json_output:
        return render_status_json(report)
    return render_status(report)
