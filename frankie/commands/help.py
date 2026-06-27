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
            "  frankie status [--json]",
            "  frankie inventory [--json]",
            "  frankie audit [--verbose] [--json]",
            "  frankie doctor [--verbose] [--json]",
            "  frankie evidence list",
            "  frankie evidence validate",
            "  frankie evidence show <evidence_id> [--json]",
            "",
            "Planned commands:",
            "  none",
            "",
            "JSON output:",
            "  --json returns structured data for status, inventory, audit and doctor.",
            "  Evidence show also supports --json.",
            "",
            "All commands run offline.",
            "No command connects to the Frankie physical server.",
            "This development version does not modify servers, services, files, or configurations.",
        ]
    )
