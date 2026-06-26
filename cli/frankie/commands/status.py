from __future__ import annotations

from frankie.core.context import AppContext
from frankie.core.evidence import latest_evidence
from frankie.core.payload import Payload


def run(context: AppContext) -> Payload:
    evidence = latest_evidence(context)
    state = "OK" if evidence else "UNKNOWN"
    summary = "Latest repository evidence found" if evidence else "No evidence found"

    targets = [
        {
            "name": "srv-servicios",
            "state": state,
            "source": evidence["path"] if evidence else None,
        },
        {
            "name": "srv-recursos",
            "state": state,
            "source": evidence["path"] if evidence else None,
        },
    ]

    return Payload(
        title="Frankie Status",
        status=state,
        summary=summary,
        data={
            "mode": "read-only",
            "latest_evidence": evidence,
            "targets": targets,
            "notes": [
                "Status is based on local repository evidence.",
                "Frankie CLI v0.6.0 does not connect to servers.",
            ],
        },
    )
