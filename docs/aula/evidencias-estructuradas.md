# Actividad: evidencias estructuradas

## Objetivo

Aprender a localizar, validar e interpretar evidencias técnicas sin conectarse a la infraestructura.

## Material necesario

Repositorio Frankie, Python, una terminal y esta guía.

## Práctica

1. Ejecuta `python -m frankie evidence list`.
2. Identifica una evidencia con estado `OK` y otra con estado `WARNING`.
3. Ejecuta `python -m frankie evidence validate`.
4. Anota cuántas fichas son válidas y si existe alguna incidencia de carga.
5. Ejecuta `python -m frankie evidence show samba-validation-current`.
6. Repite el comando con `--json`.
7. Compara el componente, estado, severidad, origen y recomendación en ambos formatos.

## Resultado esperado

La validación informa de seis fichas válidas y ninguna inválida. La evidencia SMB aparece como `OK / INFO`.

## Evidencia a entregar

- Identificador de dos fichas.
- Resultado de la validación.
- Una diferencia entre la salida de consola y JSON.
- Una explicación breve de por qué una evidencia debe conservar fecha, origen y recomendación.

## Preguntas de repaso

1. ¿Por qué una evidencia necesita referencias?
2. ¿Qué diferencia hay entre validar una ficha y comprobar un servidor en directo?
3. ¿Por qué una evidencia pública no debe contener secretos?

## Mini rúbrica

- Lista y valida las evidencias: 1 punto.
- Interpreta correctamente la ficha SMB: 1 punto.
- Explica la importancia de la trazabilidad: 1 punto.

## Seguridad

Estos comandos solo leen archivos versionados del repositorio. No acceden a Frankie, no cambian servicios y no requieren credenciales.
