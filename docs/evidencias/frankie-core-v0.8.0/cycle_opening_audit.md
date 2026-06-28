# Auditoría de apertura del ciclo v0.8.0-dev

## Identificación

- Work Order: `WO-0017`.
- Fecha: 2026-06-28.
- Tipo: `OFFLINE`.
- Versión anterior: `0.7.0`.
- Versión nueva: `0.8.0-dev`.
- Riesgo para producción: nulo.

## Objetivo

Abrir el ciclo de desarrollo `v0.8.0-dev`, priorizar su alcance candidato y separar el trabajo local de las futuras intervenciones LIVE.

## Contexto de v0.7.0

- `v0.7.0` está publicada oficialmente en GitHub.
- Su release y cierre post-release están documentados.
- El alcance funcional offline de esa versión está cerrado.
- Los tags publicados no se modificaron durante esta Work Order.

## Estructura de roadmap creada

- `docs/roadmap/v0.8.0-planning.md`: objetivo, prioridades, candidatos, riesgos, dependencias y criterios.
- `docs/roadmap/v0.8.0-offline-live-plan.md`: fronteras y gates OFFLINE/LIVE.
- `docs/roadmap/v0.8.0-workorders.md`: backlog de tres WOs OFFLINE y cuatro WOs LIVE.

El núcleo candidato prioriza evidencias, exportación, preparación LIVE desactivada, limpieza técnica y material didáctico asociado. Dashboard, API, IA y Repair Mode quedan diferidos.

## Plan OFFLINE / LIVE

El camino OFFLINE incluye diseño, documentación, schemas, validadores, simuladores, tests, exportación y refactor acotado.

El camino LIVE separa captura real, Portainer, Samba, backups y Proxmox en WOs pequeñas. Incluye autorización, identidad, allowlist, timeout, saneamiento y criterios de parada.

La regla principal queda documentada de forma literal:

```text
Las tareas LIVE solo se ejecutarán cuando el usuario confirme acceso real a Frankie.
```

## Backlog de Work Orders

### OFFLINE

- `WO-0018`: mejorar evidencias y exportación de informes.
- `WO-0019`: preparar Live Mode de solo lectura con código desactivado.
- `WO-0020`: limpieza técnica y consistencia del repositorio.

### LIVE

- `WO-LIVE-0001`: captura real de estado Frankie.
- `WO-LIVE-0002`: revisión controlada de Portainer puerto 8000.
- `WO-LIVE-0003`: validación avanzada Samba.
- `WO-LIVE-0004`: validación real de backups.

Cada propuesta incluye tipo, agentes, objetivo, riesgo, dependencias y criterio de cierre.

## Uso del sistema de agentes

Se leyeron y aplicaron los perfiles asignados:

- `docs/agents/software/software-architect.md`.
- `docs/agents/software/release-manager.md`.
- `docs/agents/software/repository-maintainer.md`.
- `docs/agents/software/automation-readiness-engineer.md`.
- `docs/agents/transversal/product-owner.md`.
- `docs/agents/transversal/security-reviewer.md`.
- `docs/agents/transversal/technical-writer.md`.
- `docs/agents/transversal/system-auditor.md`.

Aplicación observada:

- Product Owner priorizó un núcleo viable y difirió dashboard/API.
- Software Architect mantuvo contratos y comportamiento existentes.
- Automation Readiness Engineer exigió gate desactivado, simuladores y guardrails.
- Security Reviewer mantuvo separación OFFLINE/LIVE y ausencia de secretos.
- System Auditor exigió evidencia y criterios de entrada/salida.
- Technical Writer preservó la línea temporal entre release estable y ciclo dev.
- Release Manager protegió los tags publicados.
- Repository Maintainer acotó archivos y registro Git.

## Archivos creados

- `docs/roadmap/v0.8.0-planning.md`.
- `docs/roadmap/v0.8.0-offline-live-plan.md`.
- `docs/roadmap/v0.8.0-workorders.md`.
- `docs/evidencias/frankie-core-v0.8.0/cycle_opening_audit.md`.

## Archivos modificados

- `frankie/core/constants.py`.
- `pyproject.toml`.
- `tests/test_version.py`.
- `tests/test_status.py`.
- `tests/test_inventory.py`.
- `tests/test_audit.py`.
- `tests/test_doctor.py`.
- `tests/test_json_output.py`.
- `README.md`.
- `ROADMAP.md`.
- `CHANGELOG.md`.
- `docs/frankie-core/README.md`.
- `docs/frankie-core/status.md`.
- `docs/frankie-core/inventory.md`.
- `docs/frankie-core/audit.md`.
- `docs/frankie-core/doctor.md`.
- `docs/frankie-core/cli.md`.
- `docs/frankie-core/evidence.md`.
- `docs/frankie-core/live-mode-design.md`.
- `docs/evidencias/structured/frankie_core.json`.
- `docs/evidencias/structured/release_v0.6.0.json`.

No fue necesario modificar perfiles o plantillas de agentes: ya soportan ciclos de versión sin referencias específicas.

## Validación técnica

Se ejecutó la CLI completa requerida en texto y JSON. Todas las salidas JSON se analizaron correctamente y declaran `frankie_core_version: 0.8.0-dev`.

```text
python -m frankie version
Frankie Core 0.8.0-dev

python -m unittest discover -s tests
Ran 68 tests
OK

python -m compileall frankie
OK
```

`evidence validate` informa seis fichas válidas, cero inválidas y resultado `PASS`.

## Estado funcional conservado

- SMB: `OK / PASS / INFO`.
- Portainer puerto 8000: `WARNING / WARN / LOW`.
- Status global: `WARNING`.
- Audit global: `WARN`.
- No se introdujeron nuevas funciones en esta Work Order.

## Revisión de seguridad

- No se incluyeron contraseñas, tokens, claves privadas o credenciales reales.
- No se añadieron direcciones IP internas.
- Los términos sensibles se limitan a reglas preventivas y campos booleanos.
- No se incluyeron `.env`, logs, dumps, backups o cachés Python.
- No se usaron conexiones, SSH, Docker, Samba o Proxmox reales.

## Confirmaciones

- Live Mode real: no implementado y no ejecutado.
- Repair Mode: no implementado.
- Frankie físico: no contactado ni modificado.
- VM100 y VM101: no contactadas ni modificadas.
- Portainer: no corregido.
- Tag o GitHub Release: no creados.

## Riesgos

- La preparación de Live Mode puede confundirse con activación si el gate no permanece explícito.
- Exportar informes introduce escritura local y necesita rutas y no sobrescritura seguras.
- Una evolución de evidencias debe preservar compatibilidad o documentar migración.
- Las WOs LIVE dependen de acceso, autorización y saneamiento todavía no probados.
- El backlog debe revisarse para evitar que dashboard/API amplíen el ciclo prematuramente.

## Decisión final

```text
ciclo v0.8.0-dev abierto correctamente
```
