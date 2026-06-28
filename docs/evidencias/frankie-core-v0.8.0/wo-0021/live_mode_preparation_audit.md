# Auditoría de preparación de Live Mode

## Identificación

- Work Order: `WO-0021`.
- Fecha: 2026-06-28.
- Versión: `0.8.0-dev`.
- Tipo: `OFFLINE`.
- Riesgo para producción: nulo.

## Agentes usados

- Software Architect, Python Developer y CLI Designer.
- QA Engineer, Evidence Engineer y Automation Readiness Engineer.
- Security Reviewer, System Auditor y Technical Writer.
- LIVE Operations Controller, Network Administrator y Service Administrator.

## Alcance

- arquitectura interna sin transporte;
- comandos bloqueados `live-status` y `live-audit`;
- salida texto y JSON;
- simulación OFFLINE explícita;
- modelos para planes, guardas, resultados y candidatos;
- validador estático y funcional;
- documentación técnica y operativa;
- ejemplos simulados separados de evidencias reales.

No se implementaron SSH, sockets, requests, Docker SDK, Samba, Proxmox, systemctl, ping, credenciales, `.env`, escritura runtime o Repair Mode.

## Arquitectura creada

```text
frankie/live/
├── __init__.py
├── models.py
├── guards.py
├── simulator.py
├── renderer.py
└── engine.py
```

`frankie/commands/live.py` actúa como handler delgado. No existe adaptador o interfaz capaz de conectar.

## Contratos

- `LiveCheckResult`.
- `LiveCommandPlan`.
- `LiveSafetyGuard`.
- `LiveEvidenceCandidate`.

Los modelos son inmutables. Texto y JSON se construyen desde el mismo resultado.

## Guardas

| Guarda | Estado |
| --- | --- |
| Live Mode desactivado por defecto | PASS |
| Sin credenciales o `.env` | PASS |
| Sin operaciones de red | PASS |
| Sin subprocess o shell | PASS |
| Sin escritura runtime | PASS |
| Sin Repair Mode | PASS |

Un intento interno de activación mediante `reject_real_activation(True)` produce `LiveModeBlockedError`.

## Comandos añadidos

```bash
python -m frankie live-status [--json] [--simulate]
python -m frankie live-audit [--json] [--simulate]
```

Por defecto devuelven `BLOCKED`. La simulación devuelve `SIMULATED`, pero mantiene `enabled=false`, `connected=false` y `server_contacted=false`.

## Simulador

El simulador usa únicamente nombres lógicos y datos ficticios. Sus candidatos declaran:

```text
simulated=true
publishable=false
```

Los ejemplos están aislados en `docs/evidencias/frankie-core-v0.8.0/live-mode-simulated/` y no forman parte del catálogo de evidencia real.

## Validación CLI y JSON

Se ejecutaron nueve comandos de texto y nueve variantes JSON, incluidos todos los comandos obligatorios de la Work Order.

Los nueve JSON se analizaron correctamente. Las cuatro salidas LIVE JSON confirmaron:

- versión `0.8.0-dev`;
- `enabled=false`;
- `connected=false`;
- `server_contacted=false`;
- `BLOCKED` sin simulación;
- `SIMULATED` con simulación.

Los comandos históricos, `report --json` y `evidence validate` siguen funcionando.

## Script de validación

```bash
python scripts/validation/validate_live_mode_guards.py
```

Resultado:

```text
Frankie Live Mode guard validation: PASS
Commands checked: 8
Server contacted: false
Dangerous runtime imports or calls: 0
```

## Tests y compilación

```text
python -m unittest discover -s tests
Ran 98 tests
OK

python -m compileall -q frankie
OK
```

Los tests cubren bloqueo, JSON, simulación, activación rechazada, help, compatibilidad y ausencia de APIs peligrosas.

## Seguridad

- No se incluyeron secretos, credenciales o direcciones internas.
- Los términos preventivos de documentación no son valores sensibles.
- No se leyó `.env`.
- No se ejecutaron comandos externos desde el runtime LIVE.
- No se realizó ninguna conexión.
- No se escribieron evidencias LIVE reales.

## Confirmaciones operativas

- Frankie físico: no contactado ni modificado.
- VM100 y VM101: no contactadas ni modificadas.
- Servicios reales: no consultados.
- Live Mode real: desactivado y sin transporte.
- Repair Mode: no implementado.
- Portainer: no corregido.

## Riesgos

- Un usuario podría confundir simulación con evidencia real si elimina los avisos.
- Una futura implementación de transporte deberá pasar una revisión arquitectónica y de seguridad independiente.
- El estado `BLOCKED` usa exit code `0` porque el bloqueo es el comportamiento esperado; automatizaciones deben comprobar también el campo `status`.
- Los ejemplos simulados deben permanecer separados del catálogo canónico.

## Decisión final

```text
listo para revisión
```
