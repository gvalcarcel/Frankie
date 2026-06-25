# Changelog

Este proyecto sigue Semantic Versioning.

## [0.5.0] - Foundation - 2026-06-25

Primera release interna de fundacion del proyecto Frankie.

### Added

- Estructura inicial de plataforma.
- Carpetas de gobernanza y knowledge base.
- Documentacion base del proyecto.
- Plantillas Docker, Samba, backups y env.
- Scripts idempotentes con dry-run.
- Scripts de auditoria de solo lectura.
- Checklists de validacion.
- Evidencias iniciales de auditoria.
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
- Se mantiene separacion entre plantillas `.example` y configuraciones reales.

### Known Risks

- Licencia definitiva pendiente.
- Revision de secretos del historial Git pendiente antes de publicacion.
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
