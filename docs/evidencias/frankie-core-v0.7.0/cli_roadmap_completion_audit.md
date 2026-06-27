# Auditoría de finalización del roadmap CLI

## Identificación

- Work Order: `WO-0012`.
- Versión evaluada: `0.7.0-dev`.
- Fecha: 2026-06-27.
- Alcance: Frankie Core en modo offline y de solo lectura.
- Servidores contactados: ninguno.

## Resultado ejecutivo

El roadmap CLI previsto para `v0.7.0-dev` queda implementado y validado. `inventory` y `doctor` disponen de salida JSON; las evidencias estructuradas pueden enumerarse, validarse y consultarse; la ayuda documenta la interfaz completa y los errores de uso se gestionan mediante códigos de salida controlados.

**Decisión:** listo para revisión.

## Capacidades verificadas

| Capacidad | Resultado |
|---|---|
| `inventory --json` | PASS |
| `doctor --json` | PASS |
| `doctor --verbose --json` | PASS |
| `evidence list` | PASS |
| `evidence validate` | PASS: 6 válidas, 0 inválidas |
| `evidence show <id>` | PASS |
| `evidence show <id> --json` | PASS |
| Ayuda unificada | PASS |
| Errores de argumentos controlados | PASS |
| Modo offline y de solo lectura | PASS |

## Comandos no implementados

- Live Mode: excluido expresamente por requerir acceso a infraestructura real.
- Repair Mode: excluido expresamente porque esta versión es de solo lectura.
- Creación, edición y borrado de evidencias: pospuestos para preservar el modelo offline sin escritura runtime.

## Archivos creados

- `frankie/commands/evidence.py`.
- `tests/test_cli_roadmap.py`.
- `docs/frankie-core/cli.md`.
- `docs/aula/evidencias-estructuradas.md`.
- `docs/evidencias/frankie-core-v0.7.0/cli_roadmap_completion_audit.md`.

## Archivos modificados

- `frankie/app.py`.
- `frankie/cli/parser.py`.
- `frankie/commands/help.py`.
- `frankie/commands/inventory.py`.
- `frankie/commands/doctor.py`.
- `frankie/doctor/doctor_engine.py`.
- `frankie/output/console.py`.
- `frankie/output/json_output.py`.
- `tests/test_json_output.py`.
- `README.md`.
- `ROADMAP.md`.
- `CHANGELOG.md`.
- `docs/frankie-core/README.md`.
- `docs/frankie-core/status.md`.
- `docs/frankie-core/inventory.md`.
- `docs/frankie-core/audit.md`.
- `docs/frankie-core/doctor.md`.
- `docs/frankie-core/evidence.md`.
- `docs/aula/json-en-frankie-core.md`.
- `docs/aula/doctor-como-diagnostico.md`.

## Validación técnica

Se ejecutaron correctamente los comandos `version`, `help`, `status`, `inventory`, `audit`, `doctor` y `evidence` en todas las variantes exigidas por la Work Order. Las salidas JSON se analizaron como documentos JSON válidos.

```text
python -m unittest discover -s tests
Ran 68 tests
OK

python -m compileall frankie
OK
```

También se comprobaron los casos de comando desconocido, opción inválida, acción de evidencia ausente o desconocida, identificador obligatorio ausente y evidencia inexistente. Los errores esperables no producen traceback.

## Estado funcional observado

- Frankie Core: `0.7.0-dev`.
- Evidencias estructuradas: 6 válidas y 0 inválidas.
- Audit Engine: 7 checks, 6 `PASS` y 1 `WARN`.
- SMB: `PASS / INFO`.
- Portainer: `WARN / LOW` por la desviación documentada del puerto 8000.
- Resultado global de Status: `WARNING`.
- Resultado global de Audit: `WARN`.

## Seguridad

- No se realizaron conexiones con Frankie ni con sus máquinas virtuales.
- No se ejecutaron scripts de administración o producción.
- No se instalaron paquetes ni se modificaron servicios.
- La CLI no necesita credenciales para estas operaciones.
- No se implementaron modos live o repair.

## Riesgos y límites conocidos

- Los resultados dependen de la actualidad de la documentación y las evidencias versionadas.
- La validación de evidencias no sustituye todavía una validación completa contra JSON Schema.
- El warning de Portainer permanece abierto y correctamente visible.
- Los contratos JSON deberán mantenerse compatibles o versionarse cuando evolucionen.

## Conclusión

WO-0012 completa la interfaz CLI planificada para `v0.7.0-dev` sin alterar el modelo de seguridad offline y de solo lectura. El conjunto está cubierto por pruebas automatizadas, documentación técnica y material pedagógico, y queda **listo para revisión**.
