# Auditoría de decisión sobre Portainer 8000

## Identificación

- Work Order: `WO-0023`.
- Fecha: 2026-06-29.
- Tipo: OFFLINE.
- Versión: `0.8.0-dev`.
- Decisión final: **decisión preparada para futura WO-LIVE**.

## Agentes aplicados

- Software Architect.
- Evidence Engineer.
- QA Engineer.
- Automation Readiness Engineer.
- Product Owner.
- Security Reviewer.
- System Auditor.
- Technical Writer.
- Live Operations Controller.
- Network Administrator.
- Service Administrator.

## Alcance

Se analizaron exclusivamente evidencias saneadas y versionadas en el repositorio. No se conectó con Frankie, VM100, Docker, Portainer o UFW, y no se modificó ningún servicio.

## Evidencias analizadas

- ficha estructurada `portainer-port-8000-warning`;
- resumen estructurado de WO-LIVE-0001;
- inventario saneado de servicios de VM100;
- evidencia saneada de puertos y UFW;
- línea base de seguridad saneada;
- evidencia de retirada del acceso temporal de WO-LIVE-0002;
- salidas offline actuales de Doctor y Report.

## Estado de Portainer 8000

La captura LIVE de WO-LIVE-0001 documenta que Portainer publicaba y escuchaba en `8000`. UFW estaba activo, aplicaba denegación de entrada por defecto y no permitía ese puerto explícitamente.

No existe evidencia de que el mapeo se haya retirado ni de que resulte necesario para una función en uso. WO-LIVE-0002 retiró accesos temporales y no modificó Portainer.

El hallazgo permanece abierto como `WARNING / WARN / LOW`. La evidencia reduce la urgencia mediante el firewall, pero no justifica marcar la publicación como resuelta.

## Decisión recomendada

Aplicar primero la Opción C: ejecutar `WO-LIVE-0003 — Revisión controlada de Portainer puerto 8000` en modo de solo lectura.

La futura revisión debe determinar finalidad, origen declarativo, alcance y dependencias. Si el puerto no es necesario, su retirada se planificará en otra WO-LIVE de cambio con protección previa y rollback. Si es necesario, deberá existir aceptación documentada del riesgo.

## Cambios funcionales

No se modificó código. Doctor ya mantiene el hallazgo, informa severidad y urgencia `LOW` y recomienda una revisión LIVE autorizada. Report ya conserva `WARNING / WARN / LOW`, el riesgo conocido y el siguiente paso, sin afirmar una conexión nueva.

## Documentación

- decisión técnica `docs/roadmap/portainer-8000-decision.md`;
- roadmap `docs/roadmap/live-workorders.md` reconciliado con las intervenciones completadas;
- futura `WO-LIVE-0003` detallada con precondiciones, consultas, prohibiciones y cierre;
- guía didáctica `docs/aula/puertos-y-riesgos.md`;
- índices, roadmap y changelog actualizados.

## Validación ejecutada

- `python -m frankie version`: OK, `0.8.0-dev`.
- `python -m frankie evidence validate`: OK.
- `python -m frankie evidence summary`: OK.
- `python -m frankie evidence summary --json`: JSON válido.
- `python -m frankie report --json`: JSON válido; Portainer sigue `WARNING / WARN / LOW`.
- `python -m frankie doctor`: OK; hallazgo y recomendación LIVE presentes.
- `python -m frankie doctor --json`: JSON válido.
- `python -m unittest discover -s tests`: 104 tests, OK.
- `python -m compileall -q frankie`: OK.

## Seguridad y saneamiento

La revisión final confirmó la ausencia de secretos, credenciales, direcciones internas, MACs, usuarios reales y salidas brutas. Los documentos emplean únicamente identificadores lógicos y evidencia ya saneada.

## Confirmaciones

- Sin conexión LIVE.
- Sin contacto con Frankie físico o sus VMs.
- Sin subprocess, shell, socket, requests o Paramiko añadidos al runtime.
- Sin cambios en Docker, Portainer o UFW.
- Sin reinicios.
- Sin Repair Mode.
- Sin cierre indebido del hallazgo.

## Riesgos y limitaciones

- La evidencia LIVE es histórica y puede no representar el estado actual.
- El bloqueo de UFW no demuestra que el mapeo Docker sea necesario ni innecesario.
- No se inspeccionaron configuración declarativa, variables o dependencias durante esta WO OFFLINE.
- Cualquier retirada futura podría afectar a Portainer si se ejecuta sin revisión, protección y rollback.

## Decisión final

La evidencia permite mantener el riesgo `LOW` y preparar una revisión segura, pero no permite cerrar el hallazgo ni autorizar un cambio.

**Decisión preparada para futura WO-LIVE.**
