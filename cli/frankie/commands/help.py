from __future__ import annotations

from frankie.core.context import AppContext
from frankie.core.payload import Payload


def run(context: AppContext) -> Payload:
    return Payload(
        title="Frankie CLI Help",
        status="OK",
        summary="Read-only commands for the Frankie repository",
        data={
            "mode": "read-only",
            "commands": [
                "frankie version",
                "frankie status",
                "frankie inventory",
                "frankie audit",
                "frankie help",
            ],
            "documentation": [
                "docs/frankie-cli/design.md",
                "docs/validacion_scripts.md",
                "docs/mantenimiento_servidor.md",
                "knowledge/",
                "checklists/",
            ],
            "safety": [
                "No installs",
                "No service restarts",
                "No file deletion",
                "No server connections in v0.6.0",
                "No secrets required",
            ],
        },
    )
