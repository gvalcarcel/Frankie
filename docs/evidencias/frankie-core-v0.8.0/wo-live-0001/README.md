# WO-LIVE-0001: captura real de estado

Captura saneada de solo lectura realizada el 2026-06-29 sobre el servidor físico Frankie, VM100 y VM101.

## Alcance

- Proxmox, VMs y almacenamiento general.
- Docker, Portainer, PostgreSQL y n8n.
- Samba y recursos compartidos.
- Puertos y firewall.
- Estado básico de seguridad y backups visibles.

No se conservan outputs brutos, direcciones, MACs, credenciales, datos personales, identificadores de máquina o contenido de backups.

## Resultado

La captura se completó sin modificar servidores. Portainer `8000` sigue como warning; PostgreSQL no expone `5432`. La existencia y restaurabilidad de backups no pudieron verificarse con la allowlist actual.
