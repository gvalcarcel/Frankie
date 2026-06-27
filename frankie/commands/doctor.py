from __future__ import annotations

from frankie.doctor.doctor_engine import run_doctor
from frankie.evidence.loader import load_structured_evidence
from frankie.output.console import render_doctor
from frankie.output.json_output import render_doctor_json


def run(verbose: bool = False, json_output: bool = False) -> str:
    structured = load_structured_evidence()
    report = run_doctor(structured)
    if json_output:
        return render_doctor_json(report, structured, verbose=verbose)
    return render_doctor(report, verbose=verbose)
