# Changelog

Este proyecto sigue Semantic Versioning.

## [Unreleased]

Ciclo de desarrollo `0.8.0-dev` abierto tras la publicación de `v0.7.0`.

### Added

- Sistema operativo de 24 agentes reutilizables para futuras Work Orders.
- Índice, guía de uso y matriz de selección de agentes.
- Plantillas VS Code/Codex para WOs generales, OFFLINE, LIVE, release y pedagogía.
- Planificación priorizada, plan OFFLINE/LIVE y backlog inicial de `v0.8.0`.
- `evidence summary` con salida de texto y JSON.
- Informe consolidado `report` en Markdown y JSON.
- Exportación segura de informes dentro de `docs/evidencias/` con protección de sobrescritura.
- Metadatos opcionales de evidencia para timestamps, fuentes y checks relacionados.
- Evidencia estructurada y artefactos reproducibles de la validación operativa `WO-0019`.
- Flujo automatizado OFFLINE para tests, regresión CLI, evidencias e informes de `WO-0020`.

### Changed

- Documentación general sincronizada con la publicación oficial de `v0.7.0`.
- `.gitignore` permite versionar exclusivamente las plantillas Markdown de `.vscode/prompts/`.
- Versión de desarrollo actualizada a `0.8.0-dev` sin cambios funcionales.
- Validación de evidencias ampliada con duplicados, vocabularios, referencias y posibles datos sensibles.
- Flujo de evidencias e informes validado de extremo a extremo en modo OFFLINE, incluidos controles de ruta, formato y sobrescritura.
- Validación operativa convertida en un comando repetible con timeouts, hashes, protección de salida y control de delta Git.

## [v0.7.0] - 2026-06-28

Release publicada oficialmente en GitHub.

### Added

- Salida JSON determinista para `python -m frankie status --json`.
- Salida JSON determinista para `python -m frankie audit --json`.
- Salida JSON ampliada para `python -m frankie audit --verbose --json`.
- Contrato JSON `1.0` basado en los mismos modelos internos que la salida de consola.
- Documentación pedagógica inicial sobre JSON en Frankie Core.
- Modelo inicial de evidencias estructuradas con seis fichas JSON saneadas.
- Loader offline y tolerante para evidencias estructuradas.
- Esquema documental `frankie_evidence.schema.json`.
- Doctor pedagógico con urgencia, impacto, motivo, acción recomendada y explicación para alumnado.
- Salida JSON para `inventory` y `doctor`, incluido `doctor --verbose --json`.
- Comandos `evidence list`, `evidence validate` y `evidence show` con vista JSON opcional.
- Referencia completa de Frankie CLI para `v0.7.0`.
- Itinerario didáctico para FP Básica con guías, glosario y ocho actividades evaluables.
- Diseño seguro de Live Mode, sin implementación de conexión.
- Roadmap de cinco Work Orders LIVE futuras y controladas.

### Changed

- Ayuda CLI actualizada con las opciones JSON soportadas.
- Versión de Frankie Core actualizada a `0.7.0`.
- `status --json` y `audit --json` informan de la disponibilidad de evidencias estructuradas.
- Doctor verbose distingue checks activos de checks resueltos que no requieren acción.
- Ayuda general y validación de argumentos unificadas para el roadmap CLI completo.
- Índices y documentación general sincronizados con el alcance didáctico y la separación OFFLINE/LIVE.

### Security

- La salida JSON mantiene el modo offline, no ejecuta comandos externos, no usa credenciales y escribe únicamente en `stdout`.
- Live Mode permanece sin implementar; su diseño exige autorización expresa, mínimo privilegio, lista cerrada de consultas y saneamiento de evidencias.

## [v0.6.0] - 2026-06-26

Release preparada localmente. Pendiente de auditoria final, tag y publicacion en GitHub.

### Added

- Procedimiento de mantenimiento, actualización y optimización del servidor.
- Checklist operativa para mantenimiento controlado de `srv-servicios` y `srv-recursos`.
- Informe de mantenimiento real del Paso 6.
- Diseño técnico inicial de `v0.6.0 - Frankie CLI Foundation`.
- Implementación inicial de Frankie CLI en Python, en modo solo lectura.
- Creación de Frankie Core como paquete raíz `frankie/`.
- Esqueleto CLI inicial dentro de Frankie Core.
- Comandos `version` y `help` funcionales.
- Comandos foundation iniciales completados hasta `doctor` en modo solo lectura.
- Garantía de solo lectura para la foundation `0.6.0`.
- Implementación inicial de `python -m frankie status`.
- Lectura de evidencias documentadas para construir un resumen de estado.
- Resumen de estado de Frankie basado exclusivamente en el repositorio local.
- Mantenimiento del modo solo lectura en el comando `status`.
- Implementación inicial de `python -m frankie inventory`.
- Lectura de documentación, knowledge base y evidencias locales para inventario.
- Inventario conocido del servidor físico Frankie, VMs, servicios, recursos, seguridad y backups.
- Diferenciación explícita entre Frankie físico, Frankie Core y repositorio Frankie.
- Mantenimiento del modo solo lectura en el comando `inventory`.
- Implementación inicial de `python -m frankie audit`.
- Creación de `Audit Engine v1` como motor reutilizable de auditoría.
- Evaluación de evidencias documentadas del repositorio.
- Hallazgos de auditoría con estados, severidades, evidencias y recomendaciones.
- Soporte de salida detallada mediante `python -m frankie audit --verbose`.
- Mantenimiento del modo solo lectura en el comando `audit`.
- Implementación inicial de `python -m frankie doctor`.
- Creación de Doctor Engine MVP apoyado en Audit Engine.
- Interpretación de hallazgos del Audit Engine en forma de diagnostico asistido.
- Explicación de problemas, impacto probable y pasos seguros.
- Mantenimiento de modo solo lectura y sin reparación en el comando `doctor`.
- Sincronización de Frankie Core con evidencia pre-release de SMB validado.
- Priorización de evidencia actual sobre pendiente histórico en `status`, `audit` y `doctor`.
- Auditoría documental de sincronización de evidencia SMB previa a `v0.6.0`.

### Release readiness

- Readiness review de Frankie Core `v0.6.0`.
- Pre-release live evidence check con evidencias saneadas.
- Sincronización SMB validada por evidencia pre-release.
- Auditoría arquitectónica de sincronización SMB.
- Tests automatizados de comandos foundation.
- Confirmación de modo solo lectura.

### Known Risks

- Portainer puerto `8000` sigue documentado como `WARN`.
- No existe conexión live con Frankie físico en esta release.
- No existe modo repair ni autocorrección.
- La interpretación de estado se basa en evidencias documentadas.

## [0.5.0] - Foundation - 2026-06-25

Primera release interna de fundación del proyecto Frankie.

### Added

- Estructura inicial de plataforma.
- Carpetas de gobernanza y knowledge base.
- Documentación base del proyecto.
- Plantillas Docker, Samba, backups y env.
- Scripts idempotentes con dry-run.
- Scripts de auditoría de solo lectura.
- Checklists de validación.
- Evidencias iniciales de auditoría.
- Roadmap por fases.
- Plantilla de Pull Request.
- Areas futuras `monitor/` y `ai/`.
- Documento de release `docs/releases/v0.5.0-foundation.md`.

### Changed

- El proyecto se redefine como plataforma mantenible para infraestructuras Linux docentes.
- README actualizado con enfoque de producto software.

### Security

- Se establece regla de no versionar secretos reales.
- `.gitignore` preparado para excluir `.env`, backups, dumps, claves privadas, logs y temporales.
- Se mantiene separación entre plantillas `.example` y configuraciones reales.

### Known Risks

- Licencia definitiva pendiente.
- Revision de secretos del historial Git pendiente antes de publicación.
- Evidencias reales pendientes de decidir si son publicables o privadas.
- Validacion SMB desde cliente real pendiente.

### Release Checklist

- [ ] Revision de secretos.
- [ ] Revision de `.gitignore`.
- [ ] Revision de README.
- [ ] Revision de licencia.
- [ ] Revision de scripts.
- [ ] Revision de evidencias.
- [ ] Crear tag Git `v0.5.0`.
- [ ] Push a GitHub.

## Formato futuro

```markdown
## [MAJOR.MINOR.PATCH] - YYYY-MM-DD

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
```
