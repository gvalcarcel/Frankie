# Auditoría de implementación de salida JSON

Fecha: 2026-06-27

Tipo de Work Order: `OFFLINE`

Decisión final: `listo para revisión`

## 1. Alcance

WO-0009 implementa salida JSON para los comandos activos:

```bash
python -m frankie status --json
python -m frankie audit --json
python -m frankie audit --verbose --json
```

La salida de consola existente se conserva. `inventory --json` y `doctor --json` no forman parte del alcance y se rechazan explícitamente.

## 2. Versión

```text
Versión anterior: 0.6.0
Versión actual:   0.7.0-dev
Versión PEP 440:  0.7.0.dev0
```

No se creó tag ni release. `0.7.0-dev` identifica un ciclo de desarrollo en curso.

## 3. Archivos modificados

- `CHANGELOG.md`
- `README.md`
- `ROADMAP.md`
- `docs/frankie-core/README.md`
- `docs/frankie-core/status.md`
- `docs/frankie-core/inventory.md`
- `docs/frankie-core/audit.md`
- `docs/frankie-core/doctor.md`
- `frankie/app.py`
- `frankie/cli/parser.py`
- `frankie/commands/status.py`
- `frankie/commands/audit.py`
- `frankie/commands/help.py`
- `frankie/core/constants.py`
- `frankie/output/json_output.py`
- `pyproject.toml`
- `tests/test_version.py`
- `tests/test_status.py`
- `tests/test_inventory.py`
- `tests/test_audit.py`
- `tests/test_doctor.py`
- `tests/test_help.py`

## 4. Archivos creados

- `tests/test_json_output.py`
- `docs/aula/json-en-frankie-core.md`
- `docs/evidencias/frankie-core-v0.7.0/json_output_implementation_audit.md`

## 5. Diseño de salida JSON

La implementación añade un adaptador dedicado en `frankie/output/json_output.py`.

Flujo de Status:

```text
status command
-> build_status_report()
-> StatusReport
-> console renderer o JSON renderer
```

Flujo de Audit:

```text
audit command
-> run_audit()
-> AuditReport
-> console renderer o JSON renderer
```

No se analiza la salida de consola y no se duplican reglas de negocio. Ambos formatos reciben los mismos modelos internos.

El contrato inicial usa:

```text
schema_version: 1.0
mode: offline
data_source: documented_evidence
```

JSON se serializa con la biblioteca estándar, usa Unicode y se escribe únicamente por `stdout`.

## 6. Validación de status --json

Resultado:

```text
Código de salida: 0
JSON válido: sí
command: status
frankie_core_version: 0.7.0-dev
mode: offline
overall_status: WARNING
components: 17
Samba: OK / INFO
Portainer: WARNING / LOW
```

La salida pudo procesarse con `json.loads` sin texto adicional antes o después.

## 7. Validación de audit --json

Resultado:

```text
Código de salida: 0
JSON válido: sí
command: audit
frankie_core_version: 0.7.0-dev
mode: offline
overall_result: WARN
checks: 7
PASS: 6
WARN: 1
AUD-SAMBA-001: PASS / INFO
AUD-SERVICES-PORTAINER-001: WARN / LOW
```

La salida pudo procesarse con `json.loads` sin texto adicional antes o después.

## 8. Validación de audit --verbose --json

La combinación está implementada y produce JSON válido.

Cada check conserva los campos del modo normal y añade:

- `category`;
- `description`;
- `limitation`.

No se mezclan encabezados, colores ni texto de consola.

## 9. Compatibilidad con modo texto

Se validaron correctamente:

- `python -m frankie`;
- `python -m frankie version`;
- `python -m frankie help`;
- `python -m frankie status`;
- `python -m frankie inventory`;
- `python -m frankie audit`;
- `python -m frankie audit --verbose`;
- `python -m frankie doctor`;
- `python -m frankie doctor --verbose`.

Los resultados funcionales siguen siendo:

```text
status: WARNING
audit: WARN
doctor: ACTIONS_RECOMMENDED
```

## 10. Resultado de tests

Comando:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 45 tests
OK
```

## 11. Resultado de compileall

Comando:

```bash
python -m compileall frankie
```

Resultado: `OK`.

## 12. Seguridad y modo operativo

- No se tocó el servidor físico Frankie.
- No se conectó con Proxmox ni con las máquinas virtuales.
- No se usó SSH.
- No se ejecutaron Docker, Samba ni comandos live.
- No se ejecutan subprocess en el runtime JSON.
- No se leen ficheros `.env`.
- No se escriben ficheros en runtime.
- No se requieren credenciales.
- No se incluyeron secretos ni IPs reales nuevas.
- No se modificó la carpeta histórica `cli/`.

## 13. Estado SMB

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO
```

## 14. Estado Portainer

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN / LOW
```

El hallazgo del puerto `8000` permanece visible y no fue corregido ni ocultado.

## 15. Riesgos

| Riesgo | Estado | Tratamiento |
| --- | --- | --- |
| Contrato JSON inicial | Abierto | Mantener `schema_version` y añadir tests antes de cambiar claves. |
| IDs derivados de nombres en Status | Aceptado para v1 | Sustituir por IDs de dominio explícitos si los modelos evolucionan. |
| Diferencia entre modo normal y verbose | Controlado | Tests verifican que verbose solo añade detalle. |
| Comandos sin JSON | Intencionado | `inventory` y `doctor` se rechazan hasta una Work Order posterior. |
| Estado basado en documentos | Conocido | `mode` y `data_source` lo declaran de forma explícita. |

## 16. Decisión final

```text
listo para revisión
```

La salida JSON de Status y Audit cumple el contrato inicial, mantiene compatibilidad con consola y conserva las garantías offline y de solo lectura.
