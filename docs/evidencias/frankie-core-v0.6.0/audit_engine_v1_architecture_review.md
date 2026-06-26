# Frankie Audit Engine v1 - Architecture Review

## Fecha de auditoría

2026-06-26

## Alcance revisado

Esta auditoría revisa arquitectónicamente el MVP del comando:

```bash
python -m frankie audit
python -m frankie audit --verbose
```

Archivos revisados:

- `frankie/commands/audit.py`
- `frankie/audit/audit_engine.py`
- `frankie/audit/checks.py`
- `frankie/audit/rules.py`
- `frankie/core/models.py`
- `frankie/core/paths.py`
- `frankie/output/console.py`
- `frankie/cli/parser.py`
- `frankie/app.py`
- `tests/test_audit.py`
- `tests/test_not_implemented_commands.py`
- `tests/test_read_only_foundation.py`
- `docs/frankie-core/audit.md`
- `docs/frankie-core/README.md`
- `docs/evidencias/frankie-core-v0.6.0/audit_engine_v1_audit.md`
- `CHANGELOG.md`
- `ROADMAP.md`

No se han revisado servidores reales, Proxmox, Docker, Samba, backups en producción ni conexiones SSH.

## Resumen ejecutivo

`Frankie Audit Engine v1` cumple la arquitectura esperada para Frankie Core `0.6.0-dev`.

El comando `audit` ya no es un placeholder. Ejecuta un motor reutilizable que lee evidencias locales del repositorio, evalúa 7 checks con identificadores `AUD-*`, produce hallazgos con estado, severidad, evidencias, mensajes y recomendaciones, y calcula un resultado global prudente.

La implementación mantiene el modo estrictamente solo lectura: no ejecuta comandos externos, no escribe ficheros, no consulta servicios reales, no usa credenciales y no se conecta al servidor físico Frankie.

Se detectaron dos incoherencias documentales menores heredadas de la transición de `audit` desde placeholder a comando funcional. Fueron corregidas en `README.md` y `CHANGELOG.md`.

## Tabla de validaciones arquitectónicas

| Área | Resultado | Observación |
| --- | --- | --- |
| Capa de comando | OK | `frankie/commands/audit.py` actúa como capa fina. |
| Motor de auditoría | OK | `audit_engine.py` orquesta fuentes, checks y resultado global. |
| Checks | OK | `checks.py` contiene evaluación de las comprobaciones mínimas. |
| Reglas | OK | `rules.py` define checks reutilizables con ID, nombre, descripción y categoría. |
| Modelos | OK | Existen `AuditCheck`, `AuditFinding`, `AuditReport` y `AuditSource`. |
| Rutas | OK | `AUDIT_SOURCE_PATHS` centraliza las fuentes documentales. |
| Renderizado | OK | `render_audit()` presenta el informe sin evaluar reglas de negocio. |
| Resultado global | OK | Usa prioridad `FAIL > WARN > PENDING > UNKNOWN > MISSING_EVIDENCE > PASS`. |
| Verbose | OK | Amplía información sin cambiar el resultado ni el comportamiento. |
| Seguridad | OK | No se detectan operaciones peligrosas en el flujo real de auditoría. |
| Tests | OK | La suite local pasa con 25 tests. |
| Documentación | OK | Explica propósito, fuentes, estados, severidades, límites y uso pedagógico. |

## Validación de solo lectura

Se validó que `audit` y `audit --verbose`:

- no escriben ficheros;
- no modifican ficheros;
- no borran ficheros;
- no abren ficheros en modo escritura;
- no ejecutan subprocess;
- no lanzan scripts Bash;
- no consultan servicios reales;
- no usan SSH;
- no acceden a Internet;
- no leen credenciales;
- no leen `.env`;
- no modifican configuración;
- no se conectan al servidor físico Frankie.

El flujo de auditoría lee ficheros locales mediante `FrankiePaths.read_text()` y devuelve modelos en memoria.

## Validación de flujo interno

El flujo revisado es:

```text
CLI parser
  -> audit command
  -> audit engine
  -> audit checks/rules
  -> audit models
  -> console renderer
  -> output text
```

`frankie/commands/audit.py` se limita a:

```python
render_audit(run_audit(), verbose=verbose)
```

Esto mantiene el comando desacoplado de la lógica de auditoría.

## Validación de modelos

Los modelos de auditoría son:

- `AuditCheck`
- `AuditFinding`
- `AuditReport`
- `AuditSource`

También se reutiliza `InventoryItem` para representar el scope del informe.

La estructura permite evolución futura hacia:

- salida JSON;
- salida Markdown;
- dashboard;
- API;
- módulo IA;
- auditorías en vivo claramente separadas del modo actual.

Los estados permitidos son:

- `PASS`
- `WARN`
- `FAIL`
- `UNKNOWN`
- `PENDING`
- `MISSING_EVIDENCE`

Las severidades permitidas son:

- `INFO`
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

`AuditFinding.__post_init__()` valida estados y severidades, reduciendo el riesgo de valores arbitrarios.

## Validación de checks y reglas

Los checks implementados son:

- `AUD-EVIDENCE-001`
- `AUD-REPORT-001`
- `AUD-SERVICES-PORTAINER-001`
- `AUD-SAMBA-001`
- `AUD-POSTGRES-001`
- `AUD-CORE-READONLY-001`
- `AUD-CONCEPTS-001`

Cada check tiene:

- identificador claro;
- nombre;
- descripción;
- categoría;
- estado;
- severidad;
- evidencias;
- mensaje;
- recomendación.

Los checks no inventan datos en vivo. Evalúan únicamente documentación y evidencias locales disponibles en el repositorio.

## Validación de resultado global

La prioridad del resultado global está definida como:

```text
FAIL > WARN > PENDING > UNKNOWN > MISSING_EVIDENCE > PASS
```

El resultado actual es:

```text
Overall audit result: WARN
```

Es coherente con la desviación documentada de Portainer en `AUD-SERVICES-PORTAINER-001`.

## Validación de `--verbose`

`python -m frankie audit --verbose`:

- mantiene el mismo número de checks;
- mantiene el mismo resultado global;
- no cambia estados;
- no ejecuta acciones adicionales;
- no intenta conexión en vivo;
- añade categoría, descripción, recomendación y limitación cuando aplica.

La opción es segura porque solo modifica el renderizado de salida.

## Validación de seguridad

Se realizó búsqueda estática sobre el flujo de auditoría con patrones como:

- `subprocess`
- `popen`
- `os.system`
- `open(`
- `write_text`
- `unlink`
- `remove`
- `rmdir`
- `rmtree`
- `ssh`
- `docker`
- `systemctl`
- `requests`
- `urllib`
- `socket`
- `.env`
- `password`
- `secret`
- `token`
- `client_secret`
- `private key`

Hallazgos:

- `subprocess` y `write_text` aparecen en `tests/test_audit.py`, usados para ejecutar la CLI en pruebas y crear evidencias temporales dentro de `TemporaryDirectory`.
- `Docker` aparece como ruta documental o texto de recomendación, no como ejecución.
- No se detecta uso peligroso en `frankie/commands/audit.py`, `frankie/audit/*`, `frankie/output/console.py`, `frankie/core/models.py` ni `frankie/core/paths.py`.

No hay secretos ni credenciales en el flujo real de auditoría.

## Validación de relación con `status` e `inventory`

La separación conceptual se mantiene:

- `status`: cómo está Frankie según la información disponible.
- `inventory`: qué compone Frankie según la información disponible.
- `audit`: qué comprobaciones podemos validar, con qué evidencias y qué hallazgos aparecen.

Los comandos comparten rutas, modelos y renderizado de forma razonable sin duplicar responsabilidades principales.

## Validación de tests

`tests/test_audit.py` cubre:

- ejecución exitosa de `audit`;
- ejecución exitosa de `audit --verbose`;
- salida con `Frankie Audit`;
- versión `0.6.0-dev`;
- modo `read-only foundation`;
- `repository evidence`;
- `Live connection` con valor `no`;
- identificadores `AUD-*`;
- resumen de checks;
- resultado global;
- evidencias faltantes sin rotura;
- estados `PASS`, `WARN`, `PENDING`, `UNKNOWN` y `MISSING_EVIDENCE`;
- ausencia de subprocess y escritura en el flujo de auditoría;
- presencia de `audit` en `help`.

La suite completa ejecutada:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 25 tests ... OK
```

## Validación de documentación

La documentación revisada cubre:

- propósito del comando;
- diferencia entre `status`, `inventory` y `audit`;
- fuentes leídas;
- qué no hace;
- estados de auditoría;
- severidades;
- ejemplos de salida;
- limitaciones del MVP;
- carácter no tiempo real;
- ausencia de conexión con Frankie físico;
- ausencia de escritura;
- ausencia de ejecución de comandos externos;
- utilidad pedagógica;
- estado `0.6.0-dev` sin declarar release final.

Durante la auditoría se corrigieron dos mensajes obsoletos:

- `docs/frankie-core/README.md`: el ejemplo de comando no implementado ahora usa `doctor`, no `audit`.
- `CHANGELOG.md`: la lista de comandos futuros no implementados ahora solo menciona `doctor`.

## Comandos ejecutados

```bash
python -m frankie audit
python -m frankie audit --verbose
python -m frankie status
python -m frankie inventory
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

Resultados:

- `python -m frankie audit`: OK.
- `python -m frankie audit --verbose`: OK.
- `python -m frankie status`: OK.
- `python -m frankie inventory`: OK.
- `python -m frankie version`: OK.
- `python -m frankie help`: OK.
- `python -m unittest discover -s tests`: `Ran 25 tests ... OK`.
- `python -m compileall frankie`: OK.

## Riesgos detectados

### Riesgo menor: checks basados en texto

Los checks dependen de búsquedas textuales en documentos y evidencias. Es válido para el MVP, pero podría ser frágil si cambian los textos.

Clasificación: menor.

### Riesgo menor: reglas en código Python

Las reglas están separadas en `rules.py` y `checks.py`, pero no son todavía declarativas. Si aumenta mucho el número de checks, conviene estudiar un formato estructurado.

Clasificación: mejora futura.

### Mejora futura: salida estructurada

No existe salida JSON o Markdown. Los modelos actuales permiten añadirla sin reescribir el motor.

Clasificación: mejora futura.

## Correcciones realizadas

Se realizaron dos correcciones documentales menores:

- `docs/frankie-core/README.md`: ejemplo de placeholder actualizado de `audit` a `doctor`.
- `CHANGELOG.md`: lista de comandos futuros actualizada para retirar `audit`.

No se añadieron funcionalidades durante esta auditoría.

## Recomendaciones futuras

- Crear evidencias estructuradas para evitar dependencia de texto libre.
- Añadir salida JSON en una Work Order posterior.
- Añadir salida Markdown si se quiere generar informes portables.
- Separar reglas en un formato declarativo si crece el catálogo de checks.
- Mantener cualquier futuro modo live separado explícitamente del modo actual de solo lectura.
- Añadir tests específicos del orden de prioridad global.

## Decisión final

apto para cierre de WO-0004
