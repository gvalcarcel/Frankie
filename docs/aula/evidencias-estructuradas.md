# Actividad: evidencias estructuradas

## Objetivo

Aprender a localizar, validar e interpretar evidencias técnicas sin conectarse a la infraestructura.

## Práctica

1. Ejecuta `python -m frankie evidence list`.
2. Identifica una evidencia con estado `OK` y otra con estado `WARNING`.
3. Ejecuta `python -m frankie evidence validate`.
4. Anota cuántas fichas son válidas y si existe alguna incidencia de carga.
5. Ejecuta `python -m frankie evidence show samba-validation-current`.
6. Repite el comando con `--json`.
7. Compara el componente, estado, severidad, origen y recomendación en ambos formatos.

## Evidencia a entregar

- Identificador de dos fichas.
- Resultado de la validación.
- Una diferencia entre la salida de consola y JSON.
- Una explicación breve de por qué una evidencia debe conservar fecha, origen y recomendación.

## Seguridad

Estos comandos solo leen archivos versionados del repositorio. No acceden a Frankie, no cambian servicios y no requieren credenciales.
