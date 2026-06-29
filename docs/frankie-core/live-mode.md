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

## Evidencia histórica frente a Live Mode

Frankie Core puede leer evidencias LIVE saneadas ya versionadas sin activar Live Mode. Esta lectura es OFFLINE: no abre conexiones, no usa credenciales y no consulta el estado actual de los servidores.

La captura de WO-LIVE-0001 y la retirada de acceso de WO-LIVE-0002 son hechos históricos documentados. No habilitan transporte LIVE ni contradicen el gate desactivado de `live-status` y `live-audit`.
