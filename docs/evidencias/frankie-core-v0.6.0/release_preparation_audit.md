# Release Preparation Audit - v0.6.0

Fecha: 2026-06-26

Version antes: `0.6.0-dev`

Version despues: `0.6.0`

Decision final: `listo para auditoría final de release`

## 1. Alcance

Esta auditoria documenta la preparacion local de Frankie Core `v0.6.0`.

La Work Order prepara el repositorio para una auditoria final y una publicacion posterior, pero no publica la release.

Durante esta preparacion:

- no se tocaron servidores;
- no se uso SSH;
- no se ejecuto Docker;
- no se ejecuto Samba;
- no se ejecutaron scripts de produccion;
- no se creo tag;
- no se creo release;
- no se hizo push;
- no se cambio arquitectura;
- no se añadieron funcionalidades nuevas.

## 2. Archivos modificados

- `frankie/core/constants.py`
- `frankie/core/status.py`
- `frankie/audit/checks.py`
- `pyproject.toml`
- `tests/test_version.py`
- `tests/test_status.py`
- `tests/test_inventory.py`
- `tests/test_audit.py`
- `tests/test_doctor.py`
- `CHANGELOG.md`
- `README.md`
- `ROADMAP.md`
- `docs/frankie-core/README.md`
- `docs/frankie-core/status.md`
- `docs/frankie-core/inventory.md`
- `docs/frankie-core/audit.md`
- `docs/frankie-core/doctor.md`
- `docs/releases/README.md`

## 3. Archivos creados

- `docs/releases/v0.6.0.md`
- `docs/evidencias/frankie-core-v0.6.0/release_preparation_audit.md`

## 4. Validacion de version

Comando:

```bash
python -m frankie version
```

Resultado:

```text
Frankie Core 0.6.0
Mode: read-only foundation
Project: Frankie
This version does not modify servers or services.
```

## 5. Validacion de comandos

Comandos ejecutados:

```bash
python -m frankie
python -m frankie version
python -m frankie help
python -m frankie status
python -m frankie inventory
python -m frankie audit
python -m frankie audit --verbose
python -m frankie doctor
python -m frankie doctor --verbose
```

Resultado:

- `python -m frankie` muestra ayuda general.
- `version` muestra `0.6.0`.
- `help` lista comandos disponibles.
- `status` mantiene `WARNING` global por Portainer.
- `inventory` muestra inventario conocido.
- `audit` mantiene `WARN` global por Portainer.
- `audit --verbose` conserva evidencias y recomendaciones.
- `doctor` revisa una unica incidencia activa.
- `doctor --verbose` confirma que no hay reparacion automatica.

## 6. Resultado de tests

Comando:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 37 tests
OK
```

## 7. Resultado de compileall

Comando:

```bash
python -m compileall frankie
```

Resultado:

```text
compileall OK
```

## 8. Estado SMB

Estado actual documentado:

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO
```

La validacion SMB queda resuelta por evidencia pre-release. La evidencia historica donde SMB estaba pendiente se conserva como trazabilidad.

## 9. Estado Portainer

Estado actual:

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN / LOW
Doctor issues reviewed: 1
Doctor main issue: Portainer puerto 8000
```

El riesgo de Portainer puerto `8000` sigue visible y no se ha ocultado durante la preparacion de release.

## 10. Riesgos conocidos

| Riesgo | Estado | Tratamiento |
| --- | --- | --- |
| Portainer puerto `8000` sigue publicado por Docker. | Vigente | Mantener como `WARN` hasta decision tecnica futura. |
| Frankie Core no tiene live mode. | Aceptado | Diseñar en una version posterior. |
| Frankie Core no tiene repair mode. | Aceptado | Mantener seguridad y control humano. |
| Evidencias basadas en texto documental. | Aceptado para foundation | Evolucionar hacia evidencias estructuradas. |

## 11. Confirmaciones

- No se creo tag.
- No se creo release.
- No se hizo push.
- No se tocaron servidores.
- No se ejecutaron scripts de produccion.
- No se incluyeron secretos reales.
- No se cambio el hallazgo de Portainer a estado satisfactorio.

## 12. Decision final

```text
listo para auditoría final de release
```

Esta decision no publica `v0.6.0`. La publicacion requiere auditoria final y una Work Order posterior.
