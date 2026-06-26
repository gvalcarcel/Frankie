from __future__ import annotations

from frankie.audit.audit_engine import run_audit
from frankie.output.console import render_audit


def run(verbose: bool = False) -> str:
    return render_audit(run_audit(), verbose=verbose)
