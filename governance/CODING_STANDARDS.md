# Coding Standards

## Bash

- Usar `#!/bin/bash`.
- Usar `set -euo pipefail`.
- Incluir `--dry-run` cuando el script modifique estado.
- Incluir funciones `log()` y `run_cmd()`.
- Validar prerrequisitos.
- Evitar secretos.
- Evitar rutas destructivas.

## Markdown

- Titulos claros.
- Tablas solo cuando aporten comparacion.
- Fechas en formato ISO cuando sea posible.
- No inventar evidencias.

## Plantillas

- Usar extension `.example`.
- Usar placeholders claros.
- No incluir configuraciones reales sensibles.

## Documentacion tecnica

- Separar hechos, interpretaciones y decisiones.
- Incluir rollback si hay cambios operativos.
- Registrar riesgos.
