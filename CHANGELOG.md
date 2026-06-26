# Changelog

Este proyecto sigue Semantic Versioning.

## [Unreleased]

### Added

- Procedimiento de mantenimiento, actualización y optimización del servidor.
- Checklist operativa para mantenimiento controlado de `srv-servicios` y `srv-recursos`.
- Informe de mantenimiento real del Paso 6.
- Diseño técnico inicial de `v0.6.0 - Frankie CLI Foundation`.
- Implementación inicial de Frankie CLI en Python, en modo solo lectura.
- Creación de Frankie Core como paquete raíz `frankie/`.
- Esqueleto CLI inicial dentro de Frankie Core.
- Comandos `version` y `help` funcionales.
- Comandos futuros `audit` y `doctor` definidos como no implementados.
- Garantía de solo lectura para la foundation `0.6.0-dev`.
- Implementación inicial de `python -m frankie status`.
- Lectura de evidencias documentadas para construir un resumen de estado.
- Resumen de estado de Frankie basado exclusivamente en el repositorio local.
- Mantenimiento del modo solo lectura en el comando `status`.
- Implementación inicial de `python -m frankie inventory`.
- Lectura de documentación, knowledge base y evidencias locales para inventario.
- Inventario conocido del servidor físico Frankie, VMs, servicios, recursos, seguridad y backups.
- Diferenciación explícita entre Frankie físico, Frankie Core y repositorio Frankie.
- Mantenimiento del modo solo lectura en el comando `inventory`.

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
