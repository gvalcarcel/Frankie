# Auditoría de integración de evidencias LIVE saneadas

## Identificación

- Work Order: `WO-0022`.
- Fecha: 2026-06-29.
- Tipo: OFFLINE.
- Versión: `0.8.0-dev`.
- Decisión final: **listo para revisión**.

## Agentes aplicados

- Software Architect.
- Python Developer.
- Evidence Engineer.
- Data Model Designer.
- QA Engineer.
- Automation Readiness Engineer.
- Security Reviewer.
- System Auditor.
- Technical Writer.
- Live Operations Controller como control de límites OFFLINE/LIVE.

## Alcance

La intervención se limitó al repositorio local. Se integraron las fichas saneadas de WO-LIVE-0001 y WO-LIVE-0002 en el loader, la validación, el resumen y los informes de Frankie Core.

No se establecieron conexiones con el servidor físico Frankie, sus VMs ni ningún servicio. No se activó Live Mode ni se ejecutó Repair Mode.

## Cambios validados

### Loader

- Descubre las evidencias del catálogo `structured/` y las fichas `structured*.json` de `wo-live-*`.
- Mantiene compatibilidad con las siete fichas offline existentes.
- Normaliza dos contratos LIVE históricos sin modificarlos.
- Distingue `offline`, `documented-evidence`, `live-readonly` y `live-controlled`.

### Validación

- Informa de total, modos, válidas, inválidas y advertencias.
- Rechaza material de claves, credenciales con valor, direcciones privadas, MACs, saneamiento incompleto y publicación de salidas brutas.
- Resultado observado: 9 evidencias válidas, 0 inválidas y 0 advertencias.

### Resumen

- Incluye 2 evidencias LIVE: 1 captura de solo lectura y 1 retirada de acceso.
- Confirma que la captura no hizo cambios.
- Limita `changes_made=true` a la retirada controlada del acceso temporal.
- Confirma que el acceso temporal figura como retirado.

### Informe

- Markdown incorpora `Live evidence status`.
- JSON incorpora `live_evidence`, el alcance del cambio y `new_live_connection=false`.
- Conserva Samba como validado y Portainer 8000 como hallazgo conocido.
- No afirma una observación LIVE nueva.

## Validación ejecutada

Se ejecutaron correctamente:

- `python -m frankie`;
- `python -m frankie version`;
- `python -m frankie help`;
- `python -m frankie evidence validate`;
- `python -m frankie evidence summary`;
- `python -m frankie evidence summary --json`;
- `python -m frankie report`;
- `python -m frankie report --json`;
- `python -m frankie status`;
- `python -m frankie audit`;
- `python -m frankie doctor`;
- `python scripts/validation/validate_live_evidence_integration.py`;
- `python -m unittest discover -s tests`: 104 tests, resultado OK;
- `python -m compileall -q frankie`: resultado OK.

## Seguridad y saneamiento

El runtime de evidencias e informes no importa `subprocess`, `socket`, `requests` ni `paramiko`, no ejecuta `os.system` y no lee `.env`. El subproceso usado por el validador pertenece exclusivamente al arnés OFFLINE para invocar la CLI local.

Las fichas LIVE cargadas declaran direcciones, usuarios y secretos retirados, y salidas brutas no publicadas. La revisión final de archivos modificados no debe contener valores sensibles reales.

## Confirmaciones operativas

- Sin conexión LIVE nueva.
- Sin contacto con Frankie físico o sus VMs.
- Sin credenciales.
- Sin cambios en servicios o servidores.
- Sin Live Mode activado.
- Sin Repair Mode.
- Sin salidas brutas incorporadas.

## Riesgos y limitaciones

- Las evidencias LIVE describen observaciones históricas; no prueban por sí mismas el estado actual de la infraestructura.
- El parser LIVE admite únicamente los dos tipos conocidos. Un nuevo contrato requerirá revisión explícita y pruebas.
- La detección automática de datos sensibles reduce riesgo, pero no sustituye la revisión humana previa a publicación.
- Portainer 8000 continúa como hallazgo conocido y no se considera resuelto por esta integración.

## Decisión final

La integración mantiene la separación OFFLINE/LIVE, conserva compatibilidad, diferencia captura y cambio controlado y presenta evidencia histórica sin reconectar con la infraestructura.

**Listo para revisión.**
