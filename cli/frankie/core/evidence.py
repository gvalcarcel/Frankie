from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from frankie.core.context import AppContext


def latest_evidence(context: AppContext) -> dict[str, str] | None:
    evidence_root = context.path("docs/evidencias")
    if not evidence_root or not evidence_root.exists():
        return None

    candidates = [
        path
        for path in evidence_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}
    ]
    if not candidates:
        return None

    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    modified = datetime.fromtimestamp(latest.stat().st_mtime, tz=timezone.utc)
    return {
        "path": _relative_to_repo(latest, context),
        "modified": modified.isoformat(),
    }


def _relative_to_repo(path: Path, context: AppContext) -> str:
    if context.repo_root:
        try:
            return path.relative_to(context.repo_root).as_posix()
        except ValueError:
            pass
    return str(path)
