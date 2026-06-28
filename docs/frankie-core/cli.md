# Referencia de Frankie CLI

## Alcance

Frankie CLI `0.8.0-dev` conserva las capacidades publicadas en `v0.7.0`. Consulta conocimiento y evidencias versionadas, funciona offline, no se conecta al servidor físico Frankie ni a sus máquinas virtuales y no modifica el sistema.

## Comandos

| Comando | Finalidad | JSON |
|---|---|---|
| `python -m frankie version` | Mostrar la versión | No |
| `python -m frankie help` | Mostrar ayuda | No |
| `python -m frankie status` | Resumir el estado conocido | `--json` |
| `python -m frankie inventory` | Mostrar el inventario documentado | `--json` |
| `python -m frankie audit` | Evaluar reglas sobre evidencias | `--json` |
| `python -m frankie doctor` | Explicar incidencias y pasos seguros | `--json` |
| `python -m frankie evidence list` | Enumerar evidencias estructuradas | No |
| `python -m frankie evidence validate` | Validar las evidencias cargadas | No |
| `python -m frankie evidence summary` | Resumir las evidencias cargadas | `--json` |
| `python -m frankie evidence show <id>` | Mostrar una evidencia | `--json` |
| `python -m frankie report` | Generar un informe consolidado en Markdown | `--json` |

`audit` y `doctor` admiten `--verbose`. La combinación `doctor --verbose --json` conserva el contexto pedagógico y añade detalles técnicos.

## Errores y códigos de salida

- `0`: ejecución correcta.
- `1`: resultado operativo no satisfactorio, como una evidencia inexistente o una validación con incidencias.
- `2`: uso incorrecto de la CLI, comando desconocido o argumentos incompatibles.

Los errores se escriben en la salida de error y no generan trazas internas para fallos de uso esperables.

## Exportación de informes

`report` admite `--markdown`, `--json`, `--output <ruta>` y `--force`. La escritura queda limitada a `docs/evidencias/` y no sobrescribe sin confirmación explícita mediante `--force`.

Referencia: [reports.md](reports.md).

## Garantías de seguridad

- Solo lectura.
- Sin conexión a servidores.
- Sin instalación de paquetes.
- Sin reinicios ni cambios de servicios.
- Sin necesidad de credenciales.
- Sin modos live o repair en esta versión.

## Modos futuros

`live-status` y `live-audit` existen únicamente como propuesta de diseño. No son comandos disponibles en `0.8.0-dev`.

Una tarea LIVE futura necesitará autorización expresa del usuario, objetivos definidos y controles de solo lectura. Repair Mode permanece fuera de alcance.

Consulta el [diseño seguro de Live Mode](live-mode-design.md).

## Documentación relacionada

- [Status](status.md)
- [Inventory](inventory.md)
- [Audit](audit.md)
- [Doctor](doctor.md)
- [Evidencias estructuradas](evidence.md)
- [Material didáctico](../aula/README.md)

## Comandos Live preparados y bloqueados

```bash
python -m frankie live-status [--json] [--simulate]
python -m frankie live-audit [--json] [--simulate]
```

Sin simulación devuelven `BLOCKED`. Con `--simulate` prueban el contrato mediante datos ficticios. Ambos caminos mantienen `enabled=false` y `server_contacted=false`.
