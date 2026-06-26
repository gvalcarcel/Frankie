from __future__ import annotations

from frankie.inventory.inventory_reader import build_inventory_report
from frankie.output.console import render_inventory


def run() -> str:
    return render_inventory(build_inventory_report())
