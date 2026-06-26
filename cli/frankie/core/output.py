from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from frankie.core.payload import Payload


class OutputError(Exception):
    """Raised when output cannot be emitted safely."""


def emit(payload: Payload, output_format: str, output_path: str | None = None) -> None:
    rendered = render(payload, output_format)
    if output_path:
        write_output(rendered, output_path)
    else:
        print(rendered)


def render(payload: Payload, output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload.as_dict(), ensure_ascii=False, indent=2)
    if output_format == "markdown":
        return render_markdown(payload)
    if output_format == "text":
        return render_text(payload)
    raise OutputError(f"Unsupported output format: {output_format}")


def write_output(content: str, output_path: str) -> None:
    path = Path(output_path)
    if path.exists():
        raise OutputError(f"Output file already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content + "\n", encoding="utf-8")


def render_text(payload: Payload) -> str:
    lines = [
        payload.title,
        f"Status: {payload.status}",
        f"Summary: {payload.summary}",
        "",
    ]
    lines.extend(_render_text_value(payload.data))
    return "\n".join(lines).rstrip()


def _render_text_value(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_render_text_value(item, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {item}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_render_text_value(item, indent + 2))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}{value}")
    return lines


def render_markdown(payload: Payload) -> str:
    lines = [
        f"# {payload.title}",
        "",
        f"- Status: `{payload.status}`",
        f"- Summary: {payload.summary}",
        "",
        "## Data",
        "",
    ]
    lines.extend(_render_markdown_value(payload.data))
    return "\n".join(lines).rstrip()


def _render_markdown_value(value: Any, indent: int = 0) -> list[str]:
    prefix = "  " * indent
    lines: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}- **{key}**:")
                lines.extend(_render_markdown_value(item, indent + 1))
            else:
                lines.append(f"{prefix}- **{key}**: `{item}`")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_render_markdown_value(item, indent + 1))
            else:
                lines.append(f"{prefix}- {item}")
    else:
        lines.append(f"{prefix}- {value}")
    return lines
