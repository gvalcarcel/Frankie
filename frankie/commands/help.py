from __future__ import annotations

from frankie.core.constants import MODE, READ_ONLY_MESSAGE, VERSION


def run() -> str:
    return "\n".join(
        [
            f"Frankie Core {VERSION}",
            "",
            "Frankie Core is the foundation package for the Frankie platform.",
            "The CLI is one interface inside the core, not the whole project.",
            "",
            f"Mode: {MODE}",
            READ_ONLY_MESSAGE,
            "",
            "Available commands:",
            "  frankie version",
            "  frankie help",
            "  frankie status",
            "  frankie inventory",
            "  frankie audit",
            "  frankie doctor",
            "",
            "Planned commands:",
            "  none",
            "",
            "This foundation version does not modify servers, services, files, or configurations.",
        ]
    )
