# Roadmap

Versión base actual: `v0.6.0 Frankie Core / CLI Foundation`, publicada oficialmente.

Planificación activa: [`v0.8.0 - evidencias, exportación y preparación LIVE segura`](docs/roadmap/v0.8.0-planning.md).

Estrategia operativa: [OFFLINE por defecto y LIVE solo con autorización expresa](docs/roadmap/offline-live-strategy.md).

Sistema operativo de trabajo: [agentes reutilizables y plantillas de Work Orders](docs/agents/README.md).

## Fase 1 - Infraestructura Base

### Objetivos

- Documentar host, VMs, red, almacenamiento y servicios base.
- Mantener plantillas Docker, Samba, env y backups.
- Definir estructura de repositorio.

### Estado

En curso.

### Dependencias

- Inventario real.
- Evidencias de auditoría.
- Reglas de seguridad documental.

### Hitos

- Estructura base del repositorio.
- Documentación inicial.
- Auditoria inicial de VMs.

## Fase 2 - Automatizacion

### Objetivos

- Convertir operaciónes repetibles en scripts idempotentes.
- Mantener dry-run y validaciones.
- Evitar secretos en automatizaciones.

### Estado

Iniciada.

### Dependencias

- Fase 1.
- Snapshots antes de pruebas.

### Hitos

- Scripts base.
- Scripts idempotentes.
- Validacion controlada.

## Fase 3 - Auditoria

### Objetivos

- Crear auditorías de solo lectura.
- Guardar evidencias.
- Comparar estado real contra documentación.

### Estado

Iniciada.

### Dependencias

- Scripts de auditoría.
- Checklists.

### Hitos

- Auditoria de `srv-servicios`.
- Auditoria de `srv-recursos`.
- Informe de desviaciones.
- Procedimiento de mantenimiento, actualización y optimización.

## Fase 4 - Monitorizacion

### Objetivos

- Definir metricas de salud.
- Preparar monitorización de servicios, backups y espacio.
- Registrar alertas.

### Estado

Pendiente.

### Dependencias

- Auditoria estable.
- Servicios definidos.

### Hitos

- Eleccion de herramienta.
- Checks iniciales.
- Alertas basicas.

## Fase 5 - Dashboard

### Objetivos

- Crear vista operativa del estado de infraestructuras.
- Mostrar servicios, backups, incidencias y riesgos.

### Estado

Pendiente.

### Dependencias

- Monitorizacion.
- Modelo de datos.

### Hitos

- Prototipo de dashboard.
- Vista por servidor.
- Vista por laboratorio.

## Fase 6 - Knowledge Base

### Objetivos

- Consolidar conocimiento reutilizable.
- Documentar patrones de despliegue.
- Registrar incidencias y decisiones.

### Estado

Pendiente.

### Dependencias

- Governance.
- Evidencias reales.

### Hitos

- Taxonomia de conocimiento.
- Plantillas de incidencias.
- Guias operativas.

## Fase 7 - Frankie AI

### Objetivos

- Incorporar asistencia IA sobre documentación y evidencias.
- Ayudar en diagnostico, propuestas y revisiones.

### Estado

Pendiente.

### Dependencias

- Knowledge base limpia.
- Políticas de seguridad de datos.

### Hitos

- Casos de uso.
- Prompting operativo.
- Políticas de no exposición de secretos.

## Fase 8 - Autocuracion

### Objetivos

- Proponer respuestas automaticas o semiautomaticas ante incidencias.
- Mantener control humano en cambios de riesgo.

### Estado

Pendiente.

### Dependencias

- Monitorizacion.
- Auditoria.
- Runbooks.
- Políticas de aprobacion.

### Hitos

- Runbooks validados.
- Acciones sugeridas.
- Acciones con aprobacion humana.

## v0.6.0 - Frankie Core / CLI Foundation

### Objetivos

- Diseñar e iniciar `Frankie Core` como paquete raíz de la plataforma.
- Mantener `Frankie CLI` como una interfaz dentro del núcleo.
- Mantener la primera versión en modo solo lectura.
- Implementar `version` y `help` como comandos base.
- Implementar `status` como primer MVP funcional basado en evidencias locales.
- Implementar `inventory` como segundo MVP funcional basado en documentación y knowledge base.
- Implementar `audit` como primer motor reutilizable de auditoría basado en evidencias.
- Implementar `doctor` como MVP de diagnóstico asistido basado en Audit Engine.
- Integrar la CLI con `docs/`, `knowledge/` y `checklists/`.

### Estado

Release preparada localmente. Pendiente de auditoría final, tag y publicación en GitHub.

### Dependencias

- Documentación actualizada.
- Evidencias publicables disponibles.
- Scripts de auditoría estables.
- Reglas de seguridad y no exposición de secretos.

### Hitos

- Documento de diseño en `docs/frankie-cli/design.md`.
- Documento de Frankie Core en `docs/frankie-core/README.md`.
- Estructura base del paquete raíz `frankie/`.
- Definición de comandos iniciales.
- Tests básicos de foundation.
- Frankie Status MVP basado en evidencias documentadas.
- Frankie Inventory MVP basado en documentación, knowledge base y evidencias locales.
- Frankie Audit Engine v1 basado en checks, hallazgos, estados y severidades.
- Frankie Doctor MVP basado en interpretación segura de hallazgos del Audit Engine.
- Sincronización de evidencia pre-release para diferenciar pendientes históricos de estado actual validado.
- Criterios de finalización de `v0.6.0`.
- Preparación documental de release `v0.6.0`.

### Próximos pasos sugeridos

- Añadir salida `--json` para comandos principales.
- Evolucionar hacia evidencias estructuradas.
- Diseñar `live status` sin romper el modo seguro.
- Diseñar `live audit` con permisos y alcance claramente controlados.
- Revisar la publicación del puerto `8000` de Portainer.
- Revisar si la carpeta histórica `cli/` debe mantenerse o documentarse.
- Preparar dashboard futuro.
- Preparar integración IA futura sobre documentación y evidencias.

## v0.7.0 - Datos estructurados y comprensión pedagógica

### Objetivos propuestos

- Añadir salida JSON estable para `status` y `audit`.
- Introducir un modelo inicial de evidencias estructuradas.
- Mejorar Doctor como herramienta de diagnóstico y aprendizaje.
- Crear documentación didáctica inicial para FP Básica.
- Diseñar Live Mode sin implementar conexión real.

### Estado

Publicada oficialmente como `v0.7.0`.

Bloques implementados:

- salida JSON para `status` y `audit`, incluida la variante `audit --verbose --json`;
- modelo inicial y loader offline de evidencias estructuradas;
- Doctor mejorado con orientación pedagógica y pasos seguros;
- roadmap CLI completado con JSON para Inventory/Doctor y consulta de evidencias estructuradas;
- documentación didáctica, glosario y ocho actividades guiadas para FP Básica;
- diseño formal de Live Mode y propuesta de Work Orders LIVE, sin conexión real.

### Límites

- OFFLINE y solo lectura por defecto.
- Sin Live Mode real ni Repair Mode.
- Sin cambios sobre Frankie, sus VMs o servicios.
- Portainer puerto `8000` queda pendiente de una Work Order LIVE.

### Plan detallado

Ver [docs/roadmap/v0.7.0-planning.md](docs/roadmap/v0.7.0-planning.md).

Diseño y ejecución futura:

- [Diseño seguro de Live Mode](docs/frankie-core/live-mode-design.md).
- [Work Orders LIVE propuestas](docs/roadmap/live-workorders.md).

## Sistema de agentes reutilizables

Estado: incorporado después de `v0.7.0` dentro de `Unreleased`.

- 24 perfiles clasificados en hardware, software y transversales.
- índice, guía de uso y matriz de selección.
- seis plantillas de Work Orders para VS Code/Codex.
- selección explícita por tipo de tarea y riesgo.
- estrategia OFFLINE/LIVE integrada en todos los perfiles.

## v0.8.0 - Evidencias, exportación y preparación LIVE segura

### Estado

Ciclo abierto como `0.8.0-dev`.

### Prioridad

- mejorar evidencias y exportación de informes;
- preparar Live Mode con interfaces, simuladores y gate desactivado;
- realizar limpieza técnica y consistencia documental;
- mantener las intervenciones reales en WOs LIVE separadas.

### Límites

- sin Live Mode real activo;
- sin Repair Mode;
- sin dashboard o API funcional;
- sin conexión con Frankie durante tareas OFFLINE;
- sin corrección del puerto 8000 fuera de una WO LIVE autorizada.

### Documentos

- [Planificación v0.8.0](docs/roadmap/v0.8.0-planning.md).
- [Plan OFFLINE / LIVE](docs/roadmap/v0.8.0-offline-live-plan.md).
- [Backlog de Work Orders](docs/roadmap/v0.8.0-workorders.md).

### Avance registrado

- `WO-0018`: resumen de evidencias, validación reforzada e informes Markdown/JSON con exportación segura.
- `WO-0019`: validación operativa OFFLINE del registro, consulta, resumen y exportación de evidencias; siete fichas válidas y artefactos Markdown/JSON verificables.
- `WO-0020`: automatización OFFLINE del flujo de validación; 90 tests, 14 comandos de regresión y evidencia de ejecución saneada.
- `WO-0021`: arquitectura Live de solo lectura preparada con guardas cerradas, comandos bloqueados y simulador OFFLINE.
