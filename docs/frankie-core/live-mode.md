# Live Mode preparado y desactivado

## Estado

Frankie Core `0.8.0-dev` incorpora contratos, guardas y simulación para un futuro Live Mode de solo lectura. No incorpora transporte real ni puede conectarse a Frankie.

## Comandos

```bash
python -m frankie live-status [--json] [--simulate]
python -m frankie live-audit [--json] [--simulate]
```

Sin `--simulate`, devuelven `BLOCKED`, `mode: live-disabled`, `enabled: false` y `server_contacted: false`.

Con `--simulate`, prueban modelos y formatos mediante datos ficticios. La simulación mantiene Live Mode desactivado y no representa el estado de Frankie.

## Arquitectura

| Módulo | Responsabilidad |
| --- | --- |
| `models.py` | Contratos inmutables para planes, guardas, resultados y candidatos. |
| `guards.py` | Gate desactivado y rechazo de activación real. |
| `simulator.py` | Resultado ficticio y saneado. |
| `engine.py` | Orquestación limitada a bloqueo o simulación. |
| `renderer.py` | Texto y JSON desde el mismo modelo. |

No existe adaptador de red, SSH, Docker, Samba, Proxmox o shell.

## Invariantes

- `enabled=false` y `server_contacted=false` siempre;
- cero credenciales y cero lectura de `.env`;
- cero subprocess, socket, requests, Paramiko o Docker SDK;
- cero escritura runtime y cero Repair Mode;
- candidatos simulados con `publishable=false`.

## Activación futura

Una futura WO LIVE deberá definir autorización, targets, allowlist, mínimo privilegio, timeouts, evidencia raw privada, saneamiento y criterios de parada. Esta arquitectura no acepta configuración de activación.

Consulta el [diseño detallado](live-mode-design.md) y las [Work Orders LIVE](../roadmap/live-workorders.md).
