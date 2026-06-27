from __future__ import annotations

from frankie.inventory.inventory_reader import build_inventory_report
from frankie.evidence.loader import load_structured_evidence
from frankie.output.console import render_inventory
from frankie.output.json_output import render_inventory_json


def run(json_output: bool = False) -> str:
    report = build_inventory_report()
    if json_output:
        return render_inventory_json(report, load_structured_evidence())
    return render_inventory(report)
