# Validación automatizada OFFLINE

Este directorio contiene la automatización local del flujo de evidencias e informes validado en `WO-0019`.

## Ejecución

Desde la raíz del repositorio:

```bash
python scripts/validation/validate_evidence_flow.py
```

Sin argumentos crea una carpeta de ejecución con timestamp UTC dentro de:

```text
docs/evidencias/frankie-core-v0.8.0/validation-runs/
```

Para indicar una carpeta concreta:

```bash
python scripts/validation/validate_evidence_flow.py \
  --output-dir docs/evidencias/frankie-core-v0.8.0/mi-validacion
```

## Controles

- `--require-clean`: detiene el flujo si Git ya contiene cambios.
- `--force`: reemplaza exclusivamente los cuatro artefactos conocidos de la carpeta elegida.
- `--output-dir`: solo acepta rutas resueltas dentro de `docs/evidencias/`.

El script nunca usa shell, SSH, sockets o servicios externos. No instala paquetes, no cambia configuraciones y no se conecta a Frankie.

## Artefactos

Cada ejecución correcta genera:

- `consolidated_report.md`;
- `consolidated_report.json`;
- `validation_evidence.json`;
- `validation_summary.md`.

La evidencia de ejecución usa el modelo estructurado de Frankie y se valida con el loader real. Permanece junto a la ejecución y no se incorpora automáticamente al catálogo canónico.

## Repetición segura

Una carpeta con artefactos existentes se rechaza. Para repetir intencionadamente la misma ejecución:

```bash
python scripts/validation/validate_evidence_flow.py \
  --output-dir docs/evidencias/frankie-core-v0.8.0/mi-validacion \
  --force
```

Para una validación previa a release se recomienda partir de un árbol limpio y añadir `--require-clean`.
