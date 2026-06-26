from __future__ import annotations

from frankie.doctor.doctor_engine import run_doctor
from frankie.output.console import render_doctor


def run(verbose: bool = False) -> str:
    return render_doctor(run_doctor(), verbose=verbose)
