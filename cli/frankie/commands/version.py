from __future__ import annotations

from frankie import __version__
from frankie.core.context import AppContext
from frankie.core.payload import Payload


def run(context: AppContext) -> Payload:
    return Payload(
        title="Frankie CLI",
        status="OK",
        summary="Version information",
        data={
            "cli_version": __version__,
            "project": "Frankie",
            "mode": "read-only",
            "repository": "detected" if context.repo_root else "not detected",
            "repository_path": str(context.repo_root) if context.repo_root else None,
        },
    )
