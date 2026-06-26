from __future__ import annotations

from frankie.core.status import build_status_report
from frankie.output.console import render_status


def run() -> str:
    return render_status(build_status_report())
