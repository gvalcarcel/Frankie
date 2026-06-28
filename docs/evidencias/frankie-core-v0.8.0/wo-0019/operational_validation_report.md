# Validación operativa de evidencias e informes

## Identificación

- Work Order: `WO-0019`.
- Fecha: 2026-06-28.
- Versión: `0.8.0-dev`.
- Tipo: `OFFLINE`.
- Resultado: `PASS`.
- Impacto en Frankie físico y VMs: ninguno.

## Agentes aplicados

- Evidence Engineer.
- QA Engineer.
- Security Reviewer.
- System Auditor.
- Technical Writer.
- Repository Maintainer.

## Objetivo

Comprobar mediante un flujo realista de repositorio que Frankie Core puede registrar una evidencia estructurada saneada, localizarla, validarla, resumirla y utilizarla para exportar informes consolidados en Markdown y JSON.

Esta validación no observa el estado actual del servidor físico Frankie ni de sus máquinas virtuales. Evalúa exclusivamente el flujo OFFLINE introducido en `WO-0018`.

## Escenario

1. Verificar la línea base de seis evidencias estructuradas.
2. Registrar la ficha `wo-0019-evidence-report-validation`.
3. Cargar, validar, consultar y resumir las siete fichas.
4. Exportar un informe consolidado en Markdown.
5. Exportar el mismo contrato de datos en JSON.
6. Analizar el JSON y comprobar campos críticos de ambos formatos.
7. Confirmar que rutas, extensiones y sobrescrituras no autorizadas se rechazan.
8. Conservar los artefactos y sus hashes para revisión posterior.

## Entrada registrada

La ficha estructurada se conserva en:

`docs/evidencias/structured/wo_0019_operational_validation.json`

Metadatos verificados:

| Campo | Valor |
| --- | --- |
| `evidence_id` | `wo-0019-evidence-report-validation` |
| `evidence_type` | `operational_validation` |
| `status` | `PASS` |
| `severity` | `INFO` |
| `mode` | `offline` |
| `data_source` | `operational_cli_validation` |
| `created_at` | `2026-06-28T11:41:34+02:00` |
| `updated_at` | `2026-06-28T11:41:34+02:00` |

La ficha declara cero secretos, credenciales, direcciones internas, conexiones LIVE, cambios de configuración o impacto sobre servidores.

## Comandos ejecutados

```bash
python -m frankie evidence list
python -m frankie evidence validate
python -m frankie evidence summary
python -m frankie evidence summary --json
python -m frankie evidence show wo-0019-evidence-report-validation
python -m frankie report
python -m frankie report --json
python -m frankie report --markdown --output docs/evidencias/frankie-core-v0.8.0/wo-0019/consolidated_report.md
python -m frankie report --json --output docs/evidencias/frankie-core-v0.8.0/wo-0019/consolidated_report.json
```

También se ejecutaron pruebas negativas de sobrescritura, ruta fuera de `docs/evidencias/` y extensión incompatible.

## Resultados

### Línea base

```text
Valid: 6
Invalid: 0
Result: PASS
```

La salida inicial identificó correctamente SMB como `OK / PASS / INFO`, Portainer como `WARNING / WARN / LOW` y el estado general como `WARNING`.

### Estado final de evidencias

```text
Valid: 7
Invalid: 0
Result: PASS
```

El resumen final contiene:

- `PASS: 1` en estados;
- `INFO: 5` y `LOW: 2` en severidades;
- `operational_validation: 1` en tipos;
- `operational_cli_validation: 1` en fuentes;
- `offline: 7` en modos.

### Informes exportados

| Formato | Ruta | Tamaño | SHA-256 |
| --- | --- | ---: | --- |
| Markdown | `docs/evidencias/frankie-core-v0.8.0/wo-0019/consolidated_report.md` | 4078 bytes | `7A73F3A63B6E3678E734897D216D5AA37F6F835305876A055510572540D2248D` |
| JSON | `docs/evidencias/frankie-core-v0.8.0/wo-0019/consolidated_report.json` | 18192 bytes | `5C7F0012D967CBFB86E2F348D41AE1133323287DFE5037215D19DCBAF988A5D5` |

El JSON se analizó correctamente y confirmó:

- `command: report`;
- `mode: offline`;
- `evidence.total: 7`;
- `evidence.invalid: 0`;
- `overall_status: WARNING`;
- SMB `OK / PASS / INFO`;
- Portainer `WARNING / WARN / LOW`.

El Markdown contiene el título, el resumen de siete evidencias, los estados conocidos y la limitación explícita de que Frankie físico no fue consultado.

## Controles de seguridad de salida

| Check | Resultado | Evidencia observada |
| --- | --- | --- |
| `WO-0019-EVIDENCE-001` | PASS | Siete fichas válidas y cero incidencias. |
| `WO-0019-REPORT-MD-001` | PASS | Markdown creado en la ruta autorizada y contenido revisable. |
| `WO-0019-REPORT-JSON-001` | PASS | JSON válido, procesable y coherente con el resumen. |
| `WO-0019-OUTPUT-SAFETY-001` | PASS | Sobrescritura, salida fuera del área y extensión incorrecta rechazadas con código `2`. |

No se creó ningún fichero en los intentos rechazados. El informe JSON existente permaneció protegido al repetir la exportación sin `--force`.

## Trazabilidad

```text
Ficha estructurada
    -> evidence list / validate / show / summary
    -> ConsolidatedReport
    -> Markdown + JSON
    -> verificación de contenido y hashes
    -> este informe de validación
```

Los artefactos se encuentran juntos bajo `docs/evidencias/frankie-core-v0.8.0/wo-0019/`, mientras que la ficha reutilizable permanece en el directorio estructurado canónico.

## Validación final

```text
python -m unittest discover -s tests
Ran 83 tests
OK

python -m compileall -q frankie
OK
```

También pasaron 14 ejecuciones de regresión de `version`, `help`, `status`, `inventory`, `audit`, `doctor`, `evidence` y `report`, incluidas sus variantes verbose o JSON aplicables. Las salidas JSON se analizaron durante la prueba.

## Limitaciones

- Las dos primeras ejecuciones de regresión detectaron nueve aserciones que fijaban el catálogo canónico en seis fichas. Se actualizaron a siete sin modificar la lógica de producción ni relajar los controles; la suite completa debe pasar antes del cierre.
- La ficha se registra manualmente; Frankie Core todavía no genera evidencias estructuradas de forma automática.
- El loader aplica su validador propio, no ejecuta directamente el JSON Schema completo.
- Los informes Markdown y JSON se generan en llamadas separadas y pueden tener timestamps distintos.
- Los hashes documentan estos artefactos versionados, pero aún no existe un manifiesto automático de integridad.
- La frescura del informe depende de las evidencias presentes en el repositorio.
- No se ha validado captura LIVE, conectividad, servicios reales ni Repair Mode.

## Mejoras futuras

1. Incorporar un manifiesto de exportación con hashes y relación entre formatos.
2. Añadir validación formal contra JSON Schema sin romper el loader tolerante.
3. Permitir un identificador de ejecución común para relacionar evidencia e informes.
4. Diseñar la captura LIVE saneada en una Work Order separada y expresamente autorizada.
5. Automatizar este escenario como prueba de aceptación sin versionar artefactos temporales.

## Decisión

```text
WO-0019 validada operativamente en modo OFFLINE: PASS
```

El sistema de evidencias e informes es coherente, localizable y útil para revisión posterior dentro del alcance de `WO-0018`. El aviso de Portainer permanece documentado y no se ha intentado corregir.
