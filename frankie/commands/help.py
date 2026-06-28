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
            "  frankie evidence summary [--json]",
            "  frankie evidence show <evidence_id> [--json]",
            "  frankie report [--markdown | --json] [--output <path>] [--force]",
            "  frankie live-status [--json] [--simulate]  (prepared but disabled)",
            "  frankie live-audit [--json] [--simulate]   (prepared but disabled)",
            "",
            "Planned commands:",
            "  none",
            "",
            "JSON output:",
            "  --json returns structured data for status, inventory, audit and doctor.",
            "  Evidence show and summary also support --json.",
            "  Report defaults to Markdown and can return JSON.",
            "  Report --output only writes inside docs/evidencias/ and never overwrites without --force.",
            "  Live simulation uses fictitious data and does not represent Frankie state.",
            "",
            "All commands run offline.",
            "No command connects to the Frankie physical server.",
            "Live commands require a future authorized LIVE Work Order before any real connection can exist.",
            "This development version does not modify servers, services, or configurations.",
            "No file is written by default; report --output performs the documented local export only.",
        ]
    )
