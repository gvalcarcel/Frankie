from __future__ import annotations

from frankie.core.paths import FrankiePaths
from frankie.reports.builder import build_consolidated_report
from frankie.reports.rendering import render_report_json, render_report_markdown
from frankie.reports.writer import write_report


def generate(
    json_output: bool = False,
    markdown_output: bool = False,
    output_path: str | None = None,
    force: bool = False,
    paths: FrankiePaths | None = None,
) -> str:
    repository = paths or FrankiePaths.discover()
    report = build_consolidated_report(repository)
    output_format = "json" if json_output else "markdown"
    content = render_report_json(report) if json_output else render_report_markdown(report)
    if output_path:
        destination = write_report(content, output_path, output_format, force=force, paths=repository)
        return f"Report written: {destination.relative_to(repository.repo_root).as_posix()}"
    return content
