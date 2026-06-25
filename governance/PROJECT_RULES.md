# Project Rules

## Reglas generales

- El repositorio es la fuente unica de verdad.
- No se ejecutan cambios en produccion sin snapshot.
- No se documentan secretos.
- No se inventan estados.
- Toda automatizacion debe poder revisarse antes de ejecutarse.

## Reglas para IA

- No asumir datos no presentes en evidencias.
- No proponer cambios destructivos sin advertencia.
- No mezclar diagnostico y correccion.
- Mantener trazabilidad.

## Reglas de produccion

Antes de tocar servidores:

1. Diagnostico.
2. Backup o snapshot.
3. Plan.
4. Dry-run.
5. Ejecucion controlada.
6. Validacion.
7. Documentacion.
