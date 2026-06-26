# Frankie Status MVP - Architecture Review

## Datos de auditoría

- Work Order: WO-0002A
- Componente auditado: `python -m frankie status`
- Versión objetivo: `0.6.0-dev`
- Fecha: 2026-06-26
- Alcance: revisión arquitectónica, revisión de solo lectura, revisión documental y validación local.
- Decisión final: apto para cierre de WO-0002.

## Resumen ejecutivo

El MVP de `frankie status` cumple el objetivo definido para la foundation `v0.6.0-dev`: ofrece una vista resumida del estado de Frankie basada únicamente en evidencias documentadas dentro del repositorio local.

La implementación mantiene una separación razonable entre comando CLI, modelo de datos, lógica de estado, resolución de rutas y renderizado de consola. No ejecuta scripts del sistema, no instala paquetes, no se conecta a servidores, no usa credenciales y no modifica producción.

Durante la revisión se detectaron incoherencias menores heredadas de la fase previa: el comando `help`, el README de Frankie Core y el changelog seguían describiendo `status` como no implementado. Se corrigieron como ajustes de coherencia documental y de mensaje, sin añadir funcionalidad nueva.

## Alcance revisado

Archivos principales revisados:

- `frankie/commands/status.py`
- `frankie/core/status.py`
- `frankie/core/models.py`
- `frankie/core/paths.py`
- `frankie/output/console.py`
- `frankie/commands/help.py`
- `tests/test_status.py`
- `tests/test_not_implemented_commands.py`
- `tests/test_read_only_foundation.py`
- `docs/frankie-core/status.md`
- `docs/frankie-core/README.md`
- `docs/evidencias/frankie-core-v0.6.0/status_mvp_audit.md`
- `CHANGELOG.md`
- `ROADMAP.md`

No se han revisado servidores reales ni servicios en producción.

## Arquitectura observada

El flujo del comando es:

```text
python -m frankie status
        |
        v
frankie.commands.status.run()
        |
        v
frankie.core.status.build_status_report()
        |
        v
frankie.output.console.render_status()
```

La arquitectura queda distribuida en responsabilidades claras:

- `frankie/commands/status.py`: punto de entrada del comando.
- `frankie/core/status.py`: construcción del informe de estado.
- `frankie/core/models.py`: modelos tipados mediante dataclasses.
- `frankie/core/paths.py`: descubrimiento de rutas del repositorio y lectura de evidencias.
- `frankie/output/console.py`: presentación legible en consola.

Esta separación es adecuada para una foundation y permite evolucionar hacia salidas adicionales, inventario, auditoría y dashboard sin acoplar todo al comando CLI.

## Validación de solo lectura

La revisión estática confirma que el MVP no contiene operaciones de modificación del sistema dentro del flujo de `status`.

No se han encontrado usos funcionales de:

- `subprocess`
- `os.system`
- SSH
- clientes HTTP
- sockets
- escritura de ficheros
- borrado de ficheros
- instalación de paquetes
- reinicio de servicios
- secretos embebidos

La única coincidencia relevante en la búsqueda estática aparece en `frankie/utils/safe_subprocess.py`, dentro de documentación interna del módulo existente. No forma parte del flujo de `status`.

## Fuentes de evidencia

`frankie status` usa exclusivamente evidencias locales del repositorio:

- `docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt`
- `docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt`
- `docs/evidencias/paso-5-auditorias/informe_auditoria.md`

Si una evidencia falta, el sistema marca el área correspondiente como `MISSING EVIDENCE` o `UNKNOWN` en vez de inventar datos. Este comportamiento es correcto para una CLI de solo lectura y evita presentar inferencias no verificadas como hechos.

## Estados soportados

Los estados están centralizados en `frankie/core/models.py`:

- `OK`
- `WARNING`
- `ERROR`
- `UNKNOWN`
- `PENDING`
- `MISSING EVIDENCE`

La validación de estado en `StatusItem.__post_init__` reduce el riesgo de estados arbitrarios y facilita que futuras salidas mantengan consistencia.

## Resultado funcional observado

La salida actual de `python -m frankie status` muestra:

```text
Frankie Status
Version: 0.6.0-dev
Mode: read-only foundation

Physical server:
  Frankie....................... OK

Virtual machines:
  srv-servicios................. OK
  srv-recursos.................. WARNING

Core services:
  Docker........................ OK
  Portainer..................... WARNING
  PostgreSQL.................... OK
  n8n........................... OK
  Samba......................... WARNING

Security:
  UFW........................... OK
  Fail2ban...................... OK
  PostgreSQL exposure........... OK

Backups:
  srv-servicios backups......... OK
  srv-recursos backups.......... UNKNOWN

Evidence:
  srv-servicios audit........... OK
  srv-recursos audit............ OK
  Audit report.................. OK
  Windows/SMB validation........ PENDING

Overall status: WARNING
```

El resultado es coherente con la información documentada: hay estado general utilizable, pero sigue habiendo advertencias y validaciones pendientes.

## Tabla de validaciones

| Área | Resultado | Observación |
| --- | --- | --- |
| Comando `status` disponible | OK | El comando se ejecuta desde `python -m frankie status`. |
| Modo solo lectura | OK | No se detectan acciones de modificación ni conexiones externas. |
| Separación de responsabilidades | OK | CLI, lógica, modelos, rutas y salida están separados. |
| Uso de evidencias locales | OK | Lee documentación y logs versionados/locales. |
| Ausencia de secretos | OK | No se detectan secretos embebidos en el flujo revisado. |
| Manejo de evidencias faltantes | OK | Usa estados `MISSING EVIDENCE` y `UNKNOWN`. |
| Renderizado en consola | OK | Salida clara, agrupada por secciones. |
| Tests automatizados | OK | La suite local pasa correctamente. |
| Compilación Python | OK | `compileall` finaliza sin errores. |
| Documentación de `status` | OK | Existe documento específico en `docs/frankie-core/status.md`. |
| Ayuda de CLI | OK | Corregida para mostrar `status` como comando disponible. |
| Changelog | OK | Corregido para no listar `status` como comando futuro no implementado. |
| Prioridad de estado global | Menor | La prioridad interna sitúa `MISSING EVIDENCE` antes de `PENDING`; conviene revisar si se desea otro criterio. |

## Pruebas ejecutadas

Comandos locales ejecutados durante la revisión:

```bash
python -m frankie status
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

Resultado:

- `python -m frankie status`: correcto.
- `python -m frankie version`: correcto.
- `python -m frankie help`: correcto tras ajuste de mensaje.
- `python -m unittest discover -s tests`: `Ran 11 tests ... OK`.
- `python -m compileall frankie`: correcto.

También se ejecutó una búsqueda estática local de operaciones potencialmente peligrosas en el paquete `frankie/`. No se detectaron acciones incompatibles con el modo solo lectura en el flujo de `status`.

## Correcciones menores realizadas

Se realizaron únicamente ajustes de coherencia:

- `frankie/commands/help.py`: `frankie status` pasa a mostrarse como comando disponible.
- `docs/frankie-core/README.md`: la salida de ejemplo para comandos planificados deja de usar `status` y pasa a usar `inventory`.
- `CHANGELOG.md`: la lista de comandos futuros no implementados ya no incluye `status`.

No se añadieron nuevas funcionalidades.

## Riesgos detectados

### Riesgo menor: prioridad de estado global

La prioridad de cálculo del estado global está definida como:

```text
ERROR > WARNING > MISSING EVIDENCE > UNKNOWN > PENDING > OK
```

Puede valorarse en una iteración posterior si `PENDING` debe tener más peso que `UNKNOWN` o `MISSING EVIDENCE`, según el criterio operativo del proyecto.

Clasificación: menor.

### Riesgo menor: detección basada en texto

El MVP detecta estados mediante expresiones textuales sobre evidencias documentales. Es suficiente para la foundation, pero a futuro convendría normalizar las evidencias a un formato más estructurado.

Clasificación: menor.

### Riesgo esperado: no es monitorización en tiempo real

`frankie status` no consulta servidores en vivo. Esto es deliberado en `0.6.0-dev`, pero debe seguir comunicándose claramente para evitar malinterpretaciones.

Clasificación: mejora futura.

## Recomendaciones

- Mantener `status` como comando de solo lectura hasta cerrar formalmente `v0.6.0`.
- Considerar una salida `--format json` en una iteración posterior, sin cambiar el comportamiento base.
- Definir un esquema de evidencia estructurada para futuras auditorías.
- Extraer las reglas de detección textual a una capa declarativa si crece el número de servicios.
- Revisar explícitamente la prioridad de estados antes de construir un dashboard.
- Mantener tests de ausencia de efectos colaterales cuando se añadan nuevos comandos.

## Decisión final

El MVP de `frankie status` es apto para cierre de WO-0002.

No se han detectado riesgos críticos ni importantes. Las desviaciones identificadas son menores o mejoras futuras, y no bloquean el cierre de la Work Order.
