# Flujo automatizado de validación y evidencias

## Objetivo

`WO-0020` convierte el procedimiento operativo de `WO-0019` en un flujo OFFLINE ejecutable mediante un único comando.

La automatización valida el repositorio y sus evidencias documentadas. No consulta el servidor físico Frankie ni sus máquinas virtuales.

## Comando

Desde la raíz del repositorio:

```bash
python scripts/validation/validate_evidence_flow.py
```

Para conservar una ejecución en una ruta concreta:

```bash
python scripts/validation/validate_evidence_flow.py \
  --output-dir docs/evidencias/frankie-core-v0.8.0/validation-runs/revision-01
```

## Flujo

1. Descubre y verifica la raíz de Frankie.
2. Comprueba el estado Git inicial.
3. Ejecuta `python -m unittest discover -s tests`.
4. Ejecuta `python -m compileall -q frankie`.
5. Ejecuta 14 variantes de regresión de Frankie CLI.
6. Analiza las salidas JSON aplicables.
7. Comprueba que las evidencias estructuradas son válidas.
8. Exporta el informe consolidado en Markdown y JSON.
9. Verifica contenido, recuentos y hashes SHA-256.
10. Construye una evidencia estructurada de la ejecución.
11. Valida esa evidencia mediante el loader real en un entorno temporal.
12. Genera el resumen final y comprueba el delta Git.

## Regresión CLI

La matriz incluye:

- `version` y `help`;
- `status` e `inventory`;
- `audit` normal y verbose;
- `doctor` normal y verbose;
- `evidence list`, `validate`, `summary` y `summary --json`;
- `report` y `report --json`.

Los comandos JSON deben producir objetos analizables. La validación falla ante cualquier código de salida distinto de cero, timeout, JSON inválido o recuento incoherente.

## Seguridad e idempotencia

- Solo escribe dentro de `docs/evidencias/`.
- No sobrescribe sin `--force`.
- `--force` afecta únicamente a cuatro nombres de artefacto conocidos.
- No usa `shell=True`, red, SSH, credenciales o variables `.env`.
- Cada proceso tiene timeout.
- No elimina archivos ni modifica evidencias históricas.
- Preserva cambios Git anteriores y rechaza cualquier fichero nuevo fuera del conjunto esperado.
- `--require-clean` permite exigir una línea base completamente limpia.

## Resultado

Una ejecución correcta produce:

```text
Frankie automated validation: PASS
Artifacts: <ruta>
```

Los cuatro artefactos generados son:

| Archivo | Finalidad |
| --- | --- |
| `consolidated_report.md` | Informe legible para revisión humana. |
| `consolidated_report.json` | Contrato procesable por automatizaciones futuras. |
| `validation_evidence.json` | Evidencia estructurada y saneada de la ejecución. |
| `validation_summary.md` | Resultado, checks, hashes, seguridad y limitaciones. |

## Errores

El flujo termina con código `1` y un mensaje controlado si falla una precondición, comando, validación o exportación. No publica automáticamente un resultado `PASS` parcial.

No se genera una evidencia `PASS` cuando el flujo falla. Una futura Work Order podrá diseñar evidencias de fallo parciales sin exponer salida sensible.

## Limitaciones

- Sigue siendo una validación OFFLINE basada en el repositorio.
- No comprueba el estado actual de servicios reales.
- La evidencia de ejecución no se añade al catálogo canónico para evitar que cada ejecución cambie sus fixtures y recuentos.
- No existe workflow de integración continua todavía.
- La salida resumida no conserva stdout o stderr completos para reducir el riesgo de publicar datos inesperados.

## Referencias

- [Evidencias estructuradas](evidence.md).
- [Informes consolidados](reports.md).
- [Resultado operativo de WO-0019](../evidencias/frankie-core-v0.8.0/wo-0019/operational_validation_report.md).
- [Ejecución automatizada de WO-0020](../evidencias/frankie-core-v0.8.0/wo-0020/validation_summary.md).
