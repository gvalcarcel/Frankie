# Frankie Audit Engine v1 - Auditoría inicial

## Datos de auditoría

- Work Order: WO-0004
- Componente auditado: `python -m frankie audit`
- Versión objetivo: `0.6.0-dev`
- Fecha: 2026-06-26
- Tipo de revisión: auditoría local de implementación MVP.
- Decisión final provisional: listo para auditoría externa.

## Alcance

Esta auditoría cubre la implementación inicial de `Audit Engine v1`:

```bash
python -m frankie audit
```

También cubre el modo detallado:

```bash
python -m frankie audit --verbose
```

El alcance incluye:

- ejecución local del comando;
- revisión de salida por consola;
- revisión de separación arquitectónica;
- revisión de checks mínimos;
- revisión de estados y severidades;
- revisión de modo solo lectura;
- pruebas automatizadas con `unittest`;
- compilación del paquete Python;
- documentación asociada.

No se han revisado servidores reales, Proxmox, Docker, Samba, backups en vivo, conexiones SSH ni servicios de producción.

## Arquitectura revisada

El flujo implementado es:

```text
CLI parser
        |
        v
frankie.commands.audit.run()
        |
        v
frankie.audit.audit_engine.run_audit()
        |
        v
frankie.audit.checks.run_checks()
        |
        v
frankie.core.models.AuditReport
        |
        v
frankie.output.console.render_audit()
```

La lógica de auditoría no vive dentro de `commands/audit.py`. El comando actúa como capa fina y delega en el motor, los checks, los modelos y el renderizador.

## Fuentes de datos

El MVP lee únicamente fuentes locales del repositorio:

- `docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt`
- `docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt`
- `docs/evidencias/paso-5-auditorias/informe_auditoria.md`
- `docs/evidencias/frankie-core-v0.6.0/status_mvp_audit.md`
- `docs/evidencias/frankie-core-v0.6.0/status_mvp_architecture_review.md`
- `docs/evidencias/frankie-core-v0.6.0/inventory_mvp_audit.md`
- `docs/evidencias/frankie-core-v0.6.0/inventory_mvp_architecture_review.md`
- `docs/frankie-core/status.md`
- `docs/frankie-core/inventory.md`
- `knowledge/SERVIDORES.md`
- `knowledge/SERVICIOS.md`
- `knowledge/DOCKER.md`
- `knowledge/SAMBA.md`
- `knowledge/BACKUPS.md`
- `knowledge/RED.md`

Si una fuente falta, el motor conserva la ejecución y marca los checks afectados como `UNKNOWN` o `MISSING_EVIDENCE`.

## Confirmación de solo lectura

La implementación revisada:

- no modifica servidores;
- no se conecta a Frankie físico;
- no usa SSH;
- no ejecuta Docker;
- no ejecuta Samba;
- no ejecuta scripts Bash;
- no ejecuta comandos externos;
- no instala paquetes;
- no reinicia servicios;
- no borra archivos;
- no escribe ficheros;
- no lee `.env`;
- no usa credenciales;
- no consulta Internet;
- no accede a GitHub API.

La búsqueda estática local no detecta operaciones incompatibles con el modo solo lectura en el flujo de `audit`.

## Confirmación de que no se conecta a Frankie físico

La salida del comando declara explícitamente:

```text
Live connection............... no
```

No existe código de conexión remota ni integración con servicios externos en `Audit Engine v1`.

## Confirmación de que no ejecuta comandos externos

Los checks se basan en lectura de ficheros locales mediante `FrankiePaths.read_text()`.

No se usan:

- `subprocess`;
- `os.system`;
- scripts Bash;
- comandos de Docker;
- comandos de Samba;
- `systemctl`;
- SSH.

## Confirmación de que no escribe ficheros

El comando `audit` no genera ficheros de salida.

Los únicos archivos creados durante esta Work Order pertenecen al desarrollo del repositorio: código, tests, documentación y esta auditoría.

## Checks implementados

- `AUD-EVIDENCE-001`: evidencias de auditoría disponibles.
- `AUD-REPORT-001`: informe apto para dry-run.
- `AUD-SERVICES-PORTAINER-001`: desviación conocida de Portainer en puerto 8000.
- `AUD-SAMBA-001`: validación SMB desde Windows pendiente.
- `AUD-POSTGRES-001`: PostgreSQL sin exposición externa.
- `AUD-CORE-READONLY-001`: modo solo lectura de Frankie Core.
- `AUD-CONCEPTS-001`: distinción Frankie / Frankie Core / Repositorio.

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

## Resultados

- `python -m frankie audit`: correcto.
- `python -m frankie audit --verbose`: correcto.
- `python -m frankie status`: correcto.
- `python -m frankie inventory`: correcto.
- `python -m frankie version`: correcto.
- `python -m frankie help`: correcto.
- `python -m unittest discover -s tests`: `Ran 25 tests ... OK`.
- `python -m compileall frankie`: correcto.

## Salida verificada

La salida de `python -m frankie audit` incluye:

- `Frankie Audit`.
- `0.6.0-dev`.
- `read-only foundation`.
- `repository evidence`.
- `Live connection................ no`.
- `Writes files.................. no`.
- `Executes commands............. no`.
- `Checks total.................. 7`.
- identificadores `AUD-`.
- estados `PASS`, `WARN` y `PENDING`.
- severidades.
- evidencias.
- recomendaciones.
- `Overall audit result: WARN`.

## Tests añadidos

Se añadió cobertura para:

- ejecución correcta del comando;
- cabecera y versión;
- modo de solo lectura;
- alcance basado en evidencias del repositorio;
- salida con identificadores `AUD-`;
- resumen de checks;
- resultado global;
- modo `--verbose`;
- evidencias faltantes sin rotura;
- generación de estados `PASS`, `WARN`, `PENDING`, `UNKNOWN` y `MISSING_EVIDENCE`;
- ausencia de operaciones de escritura o subprocess en el flujo de auditoría;
- `frankie help` mostrando `audit` como comando disponible.

## Riesgos detectados

### Riesgo menor: checks basados en texto

Los checks iniciales detectan evidencias mediante búsqueda textual. Es suficiente para el MVP, pero a futuro conviene normalizar evidencias en un formato estructurado.

Clasificación: menor.

### Riesgo menor: reglas en código

Las reglas están separadas en `rules.py` y `checks.py`, pero siguen siendo código Python. Si crece el número de checks, podría convenir una capa declarativa.

Clasificación: mejora futura.

### Mejora futura: salida estructurada

No se implementa salida JSON en esta Work Order. La arquitectura de modelos permite añadirla posteriormente.

Clasificación: mejora futura.

## Decisión final provisional

listo para auditoría externa

La implementación cumple los criterios de la Work Order para quedar lista para revisión, sin cerrar todavía la Work Order ni declarar release.
