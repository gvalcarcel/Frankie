from __future__ import annotations

from frankie.core.models import InventoryReport, StatusReport


def render_status(report: StatusReport) -> str:
    lines = [
        "Frankie Status",
        f"Version: {report.version}",
        f"Mode: {report.mode}",
        "",
    ]

    for section in report.sections:
        lines.append(f"{section.title}:")
        for item in section.items:
            lines.append(f"  {_format_item(item.name, item.state)}")
        lines.append("")

    lines.append(f"Overall status: {report.overall_status}")
    return "\n".join(lines).rstrip()


def render_inventory(report: InventoryReport) -> str:
    lines = [
        "Frankie Inventory",
        f"Version: {report.version}",
        f"Mode: {report.mode}",
        "",
    ]

    for section in report.sections:
        lines.append(f"{section.title}:")
        for item in section.items:
            lines.append(f"  {_format_item(item.name, item.value)}")
            if item.state != "KNOWN":
                lines.append(f"    State: {item.state}")
        lines.append("")

    return "\n".join(lines).rstrip()


def _format_item(name: str, state: str) -> str:
    width = 30
    if len(name) >= width:
        return f"{name} {state}"
    dots = "." * (width - len(name))
    return f"{name}{dots} {state}"
