# Auditoría de la automatización de validación

## Identificación

- Work Order: `WO-0020`.
- Fecha: 2026-06-28.
- Versión: `0.8.0-dev`.
- Tipo: `OFFLINE`.
- Decisión: `PASS`.

## Alcance validado

- script Python ejecutable mediante un único comando;
- tests y compilación;
- regresión de 14 comandos CLI;
- validación de siete evidencias canónicas;
- exportación Markdown y JSON;
- evidencia estructurada de la ejecución;
- resumen con hashes;
- rutas seguras y control de delta Git;
- rechazo de sobrescritura accidental.

## Implementación

El flujo se encuentra en:

`scripts/validation/validate_evidence_flow.py`

Usa exclusivamente la biblioteca estándar y los módulos existentes de Frankie. La automatización permanece fuera del paquete de producto para no convertir la CLI de solo lectura en un ejecutor de tests o Git.

## Ejecuciones realizadas

### Primera ejecución

```bash
python scripts/validation/validate_evidence_flow.py \
  --output-dir docs/evidencias/frankie-core-v0.8.0/wo-0020
```

Resultado: `PASS`.

### Repetición sin autorización

El mismo comando se rechazó con código `1` porque los artefactos ya existían. No se modificó ningún fichero.

### Repetición explícita

```bash
python scripts/validation/validate_evidence_flow.py \
  --output-dir docs/evidencias/frankie-core-v0.8.0/wo-0020 \
  --force
```

Resultado: `PASS`. Solo se reemplazaron los cuatro artefactos conocidos.

### Línea base Git estricta

Una ejecución de prueba con `--require-clean` sobre el árbol de desarrollo modificado se detuvo con código `1` antes de crear la carpeta de salida. El control puede utilizarse como gate previo a release.

## Resultado final

| Validación | Resultado |
| --- | --- |
| Tests | `90 OK` |
| Compilación | `PASS` |
| Regresión CLI | `14/14 PASS` |
| Evidencias canónicas | `7 válidas / 0 inválidas` |
| Evidencia de ejecución | Validada por el loader real |
| Informe Markdown | Exportado y verificado |
| Informe JSON | Exportado, analizado y verificado |
| Delta Git | Solo artefactos esperados |
| Conexiones LIVE | Ninguna |

El resultado detallado y los hashes vigentes están en [validation_summary.md](validation_summary.md).

## Pruebas añadidas

`tests/test_validation_flow.py` cubre:

- confinamiento de rutas;
- nombre UTC de ejecución predeterminado;
- protección de sobrescritura y `--force`;
- validación de la evidencia generada;
- opciones de seguridad;
- ausencia de shell y llamadas de red.

## Seguridad

- No se encontraron secretos, credenciales o direcciones internas.
- No se accedió a Frankie, VM100 o VM101.
- No se instalaron paquetes ni se modificaron servicios.
- No se crearon tags o releases.
- La salida persistente omite stdout y stderr completos.

## Limitaciones y mejoras futuras

- Diseñar un resultado de fallo saneado sin etiquetarlo como `PASS`.
- Integrar el script en CI únicamente tras definir permisos y retención de artefactos.
- Evitar recuentos fijos del catálogo canónico en pruebas futuras mediante un manifiesto explícito.
- Definir una política de conservación para carpetas de `validation-runs/`.
- Mantener cualquier captura LIVE en una Work Order separada.

## Decisión final

```text
WO-0020 automatizada y validada operativamente: PASS
```
