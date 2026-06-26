from __future__ import annotations

from frankie.core.context import AppContext
from frankie.core.payload import Payload


def run(context: AppContext) -> Payload:
    return Payload(
        title="Frankie Inventory",
        status="OK" if context.repo_root else "WARNING",
        summary="Documented infrastructure inventory",
        data={
            "mode": "read-only",
            "source": "repository documentation",
            "targets": [
                {
                    "id": "VM100",
                    "name": "srv-servicios",
                    "role": "Application and automation services",
                    "components": [
                        "Docker",
                        "Portainer",
                        "PostgreSQL",
                        "n8n",
                        "UFW",
                        "Fail2ban",
                        "Backups",
                    ],
                },
                {
                    "id": "VM101",
                    "name": "srv-recursos",
                    "role": "Shared educational resources",
                    "components": [
                        "Samba",
                        "/srv/recursos",
                        "alumno/profesor users",
                        "alumnado/profesorado groups",
                        "UFW",
                    ],
                },
            ],
            "knowledge_files": context.existing_paths(
                [
                    "knowledge/SERVIDORES.md",
                    "knowledge/SERVICIOS.md",
                    "knowledge/DOCKER.md",
                    "knowledge/SAMBA.md",
                    "knowledge/BACKUPS.md",
                    "knowledge/RED.md",
                ]
            ),
        },
    )
