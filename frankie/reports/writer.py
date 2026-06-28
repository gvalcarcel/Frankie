from __future__ import annotations

from pathlib import Path

from frankie.core.paths import FrankiePaths


class ReportOutputError(ValueError):
    pass


def write_report(
    content: str,
    output_path: str,
    output_format: str,
    force: bool = False,
    paths: FrankiePaths | None = None,
) -> Path:
    repository = paths or FrankiePaths.discover()
    if repository.repo_root is None:
        raise ReportOutputError("Repository root could not be determined.")

    allowed_root = (repository.repo_root / "docs" / "evidencias").resolve()
    requested = Path(output_path)
    destination = (requested if requested.is_absolute() else repository.repo_root / requested).resolve()
    if not destination.is_relative_to(allowed_root) or destination == allowed_root:
        raise ReportOutputError("Report output must be inside docs/evidencias/.")

    expected_suffix = ".json" if output_format == "json" else ".md"
    if destination.suffix.lower() != expected_suffix:
        raise ReportOutputError(f"{output_format} report output must use the {expected_suffix} extension.")
    if destination.exists() and not force:
        raise ReportOutputError(f"Report output already exists: {destination.relative_to(repository.repo_root)}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content + "\n", encoding="utf-8")
    return destination
