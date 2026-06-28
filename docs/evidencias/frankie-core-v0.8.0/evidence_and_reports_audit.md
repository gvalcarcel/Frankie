# Auditoría de evidencias e informes

## Identificación

- Work Order: `WO-0018`.
- Fecha: 2026-06-28.
- Tipo: `OFFLINE`.
- Versión: `0.8.0-dev`.
- Riesgo para producción: nulo.

## Agentes usados

- Software Architect.
- Python Developer.
- Data Model Designer.
- Evidence Engineer.
- Automation Readiness Engineer.
- QA Engineer.
- Security Reviewer.
- Technical Writer.
- System Auditor.

Los perfiles se leyeron antes de implementar y se aplicaron como contratos de arquitectura, datos, seguridad, tests, documentación y cierre.

## Alcance

- modelo compatible de evidencias con metadatos opcionales;
- validación reforzada;
- resumen de evidencias en texto y JSON;
- informe consolidado Markdown y JSON;
- escritura segura dentro de `docs/evidencias/`;
- documentación técnica y de aula;
- tests positivos, negativos, de regresión y seguridad.

No se implementaron conexiones, captura live, Repair Mode o cambios en servidores.

## Comandos implementados

```bash
python -m frankie evidence summary
python -m frankie evidence summary --json
python -m frankie report
python -m frankie report --markdown
python -m frankie report --json
python -m frankie report --markdown --output docs/evidencias/<ruta>.md
python -m frankie report --json --output docs/evidencias/<ruta>.json
python -m frankie report --json --output docs/evidencias/<ruta>.json --force
```

## Modelo de evidencias

El modelo v1 sigue siendo compatible. Se añadieron campos opcionales:

- `created_at`;
- `updated_at`;
- `source_files`;
- `related_checks`.

`EvidenceSummary` agrupa fichas por estado, severidad, componente, tipo, fuente y modo.

El schema documenta vocabularios reconocidos, referencias no vacías, timestamps y los metadatos nuevos. Puede representar evidencia `offline` o `live` saneada; esto no activa Live Mode.

## Validación de evidencias

El loader detecta de forma controlada:

- JSON inválido;
- campos obligatorios ausentes;
- `evidence_id` duplicado;
- status, severity o mode no reconocidos;
- referencias vacías;
- timestamps inválidos;
- listas opcionales mal formadas;
- flags de seguridad activos;
- patrones de posibles secretos o direcciones internas en valores.

Una ficha inválida no impide conservar otras fichas válidas. No se producen tracebacks en la CLI.

Estado del repositorio:

```text
Valid: 6
Invalid: 0
Result: PASS
```

## Exportación Markdown

El informe Markdown contiene título, versión, modo, fecha, resumen ejecutivo, estado, inventario, auditoría, Doctor, evidencias, riesgos, SMB, Portainer, limitaciones y próximos pasos.

La salida predeterminada de `report` es Markdown y se imprime por consola sin escribir archivos.

## Exportación JSON

`report --json` produce un objeto JSON único con contratos derivados de los mismos modelos usados por Status, Inventory, Audit y Doctor. La salida se analizó correctamente como JSON.

`evidence summary --json` produce recuentos deterministas y ordenados.

## Escritura segura

`--output`:

- resuelve el destino contra la raíz del repositorio;
- bloquea rutas fuera de `docs/evidencias/`;
- exige `.md` o `.json` según formato;
- crea directorios intermedios;
- no sobrescribe sin `--force`.

Se realizó una prueba CLI temporal dentro de `docs/evidencias/frankie-core-v0.8.0/`: creación, bloqueo, reemplazo forzado y retirada del artefacto. No quedó fichero temporal.

## Archivos creados

- `frankie/commands/report.py`.
- `frankie/evidence/summary.py`.
- `frankie/reports/__init__.py`.
- `frankie/reports/models.py`.
- `frankie/reports/builder.py`.
- `frankie/reports/rendering.py`.
- `frankie/reports/writer.py`.
- `tests/test_reports.py`.
- `docs/frankie-core/reports.md`.
- `docs/aula/informes-en-frankie-core.md`.
- `docs/evidencias/frankie-core-v0.8.0/evidence_and_reports_audit.md`.

## Archivos modificados

- `frankie/app.py`.
- `frankie/cli/parser.py`.
- `frankie/commands/evidence.py`.
- `frankie/commands/help.py`.
- `frankie/doctor/doctor_engine.py`.
- `frankie/evidence/__init__.py`.
- `frankie/evidence/loader.py`.
- `frankie/evidence/models.py`.
- `frankie/output/console.py`.
- `frankie/output/json_output.py`.
- `tests/test_cli_roadmap.py`.
- `tests/test_read_only_foundation.py`.
- `tests/test_structured_evidence.py`.
- `docs/schemas/frankie_evidence.schema.json`.
- `docs/frankie-core/evidence.md`.
- `docs/frankie-core/cli.md`.
- `docs/frankie-core/README.md`.
- `docs/aula/README.md`.
- `README.md`.
- `ROADMAP.md`.
- `CHANGELOG.md`.

## Validación CLI

Se ejecutaron todos los comandos anteriores y la CLI previa requerida. Los comandos sin `--output` no cambiaron el working tree.

- Version: `0.8.0-dev`.
- SMB: `OK / PASS / INFO`.
- Portainer: `WARNING / WARN / LOW`.
- Evidence summary: 6 válidas, 0 inválidas, 6 offline.
- Report: Markdown y JSON correctos.

## Tests y compilación

```text
python -m unittest discover -s tests
Ran 83 tests
OK

python -m compileall frankie
OK
```

La protección foundation permite escritura únicamente en `frankie/reports/writer.py`; el resto del paquete conserva el veto de subprocess y escritura no aprobada.

## Revisión de seguridad

- No se incluyeron contraseñas, tokens, claves privadas o credenciales reales.
- Los valores sensibles de tests son marcadores negativos y no secretos utilizables.
- No se incluyeron direcciones IP internas reales.
- No se leen `.env` ni credenciales.
- No se usa subprocess, `os.system`, SSH, sockets o red.
- No se incluyen logs, dumps, backups o caches Python.

## Confirmaciones

- Live Mode real: no implementado.
- Repair Mode: no implementado.
- Frankie físico: no consultado ni modificado.
- VM100 y VM101: no consultadas ni modificadas.
- Portainer: no corregido.
- Escritura runtime: limitada al destino explícito de `report --output`.

## Riesgos

- La frescura del informe depende de evidencias documentadas.
- `--force` puede reemplazar un informe existente, pero solo con intención explícita.
- Los patrones sensibles son preventivos y no sustituyen una revisión humana.
- Evidencias LIVE futuras necesitarán saneamiento antes de ser públicas.
- El schema mantiene compatibilidad por campos opcionales; hacerlos obligatorios exigiría migración.

## Decisión final

```text
listo para revisión
```
