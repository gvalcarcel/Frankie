from __future__ import annotations

from frankie.core.context import AppContext
from frankie.core.payload import Payload


def run(context: AppContext) -> Payload:
    scripts = context.existing_paths(
        [
            "scripts/auditoria/auditar_srv-servicios.sh",
            "scripts/auditoria/auditar_srv-recursos.sh",
        ]
    )
    return Payload(
        title="Frankie Audit",
        status="OK" if len(scripts) == 2 else "WARNING",
        summary="Read-only audit entry point",
        data={
            "mode": "read-only",
            "execution": "not executed by default",
            "available_scripts": scripts,
            "recommended_commands": [
                "sudo ./scripts/auditoria/auditar_srv-servicios.sh",
                "sudo ./scripts/auditoria/auditar_srv-recursos.sh",
            ],
            "rules": [
                "The CLI does not install packages.",
                "The CLI does not restart services.",
                "The CLI does not correct deviations automatically.",
                "Audit scripts remain the operational source for VM checks.",
            ],
        },
    )
