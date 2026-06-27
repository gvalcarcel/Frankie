# Auditoría final de preparación de v0.7.0

## Identificación

- Work Order: `WO-0014`.
- Fecha: 2026-06-28.
- Tipo: `OFFLINE`.
- Riesgo para producción: nulo.
- Versión antes: `0.7.0-dev`.
- Versión después: `0.7.0`.

## Alcance revisado

- metadatos de versión y empaquetado;
- comandos y ayuda de Frankie CLI;
- salidas de consola y JSON;
- modelo y comandos de evidencias;
- Doctor pedagógico;
- documentación técnica y de aula;
- planificación OFFLINE/LIVE;
- notas e índice de releases;
- tests automatizados y compilación.

## Archivos creados

- `docs/releases/v0.7.0.md`.
- `docs/evidencias/frankie-core-v0.7.0/release_preparation_audit.md`.

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
- `docs/aula/que-es-frankie.md`.
- `docs/frankie-core/README.md`.
- `docs/frankie-core/status.md`.
- `docs/frankie-core/inventory.md`.
- `docs/frankie-core/audit.md`.
- `docs/frankie-core/doctor.md`.
- `docs/frankie-core/cli.md`.
- `docs/frankie-core/evidence.md`.
- `docs/frankie-core/live-mode-design.md`.
- `docs/roadmap/v0.7.0-planning.md`.
- `docs/releases/README.md`.
- `docs/releases/v0.6.0.md`.
- `docs/evidencias/structured/frankie_core.json`.
- `docs/evidencias/structured/release_v0.6.0.json`.

## Validación CLI

Se ejecutaron correctamente:

- comando raíz, `version` y `help`;
- Status e Inventory en texto y JSON;
- Audit en texto, verbose, JSON y verbose JSON;
- Doctor en texto, verbose, JSON y verbose JSON;
- `evidence list` y `evidence validate`.

`python -m frankie version` devuelve `Frankie Core 0.7.0`. La ayuda contiene la CLI offline completa y no expone comandos live o repair.

También se probaron `live-status` y `live-audit` como casos negativos. Ambos devuelven código `2`, comando desconocido y ningún traceback. No se inicia ninguna conexión.

## Validación JSON

Las salidas de Status, Inventory, Audit y Doctor se analizaron correctamente como JSON. Todas informan `frankie_core_version: 0.7.0` y `mode: offline`.

## Validación de evidencias

```text
Structured evidence validation
Valid: 6
Invalid: 0
Result: PASS
```

Las fichas actuales distinguen la versión preparada `0.7.0` de la última release publicada `v0.6.0`.

## Validación Doctor

- Portainer continúa como diagnóstico activo de severidad `LOW`.
- SMB no aparece como incidencia activa.
- El modo verbose conserva SMB como check resuelto.
- Doctor no implementa reparación automática.

## Validación de documentación de aula

- ocho actividades disponibles;
- ocho objetivos, materiales, secuencias guiadas, resultados, bloques de preguntas y mini rúbricas;
- enlaces relativos comprobados;
- glosario y guías accesibles desde el índice de aula.

## Validación de Live Mode

Live Mode solo existe como diseño en `docs/frankie-core/live-mode-design.md`. No hay transporte, perfiles reales, credenciales, conexión, recolector o comando registrado.

Repair Mode no está implementado ni forma parte de la CLI.

## Tests y compilación

```text
python -m unittest discover -s tests
Ran 68 tests
OK

python -m compileall frankie
OK
```

## Revisión de seguridad

- archivos nuevos y modificados revisados con patrones sensibles;
- sin contraseñas, tokens, claves privadas o credenciales reales;
- sin direcciones IP internas nuevas;
- sin `.env`, logs, dumps, backups comprimidos o cachés Python;
- las coincidencias de términos sensibles son reglas preventivas, campos booleanos o placeholders;
- no se accedió a Frankie, VM100 o VM101.

## Estado conocido

- SMB: `OK / PASS / INFO`.
- Portainer puerto 8000: `WARNING / WARN / LOW`.
- Status global: `WARNING`.
- Audit global: `WARN`.
- Evidencias estructuradas: `PASS`.

## Riesgos

- Portainer mantiene el aviso conocido hasta una Work Order LIVE autorizada.
- La información offline puede quedar desactualizada si no se renuevan evidencias.
- El material didáctico necesita revisión docente antes de una evaluación formal.
- Live Mode requiere decisiones y pruebas futuras sobre autenticación, transporte y saneamiento.
- La versión preparada no será una release publicada hasta crear tag y GitHub Release en otra Work Order.

## GitHub

- No se creó tag durante WO-0014.
- No se creó GitHub Release durante WO-0014.
- El único tag existente al preparar esta auditoría es `v0.6.0`.

## Decisión final

```text
listo para publicar release v0.7.0
```
