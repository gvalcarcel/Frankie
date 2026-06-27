# Cómo usar Frankie Core

## Requisitos

- Python 3 instalado.
- Una copia del repositorio Frankie.
- Una terminal abierta en la raíz del repositorio.

No necesitas credenciales ni conexión con el servidor.

## Primer comando

```bash
python -m frankie help
```

Este comando muestra las opciones disponibles. Si ejecutas solo `python -m frankie`, aparece la misma ayuda.

## Comandos principales

```bash
python -m frankie version
python -m frankie status
python -m frankie inventory
python -m frankie audit
python -m frankie doctor
python -m frankie evidence list
```

## Salida para personas y para programas

La salida normal está pensada para leerla en pantalla:

```bash
python -m frankie status
```

La opción `--json` crea una salida estructurada:

```bash
python -m frankie status --json
```

JSON no cambia el resultado. Solo cambia la forma de presentarlo.

## Cómo trabajar con seguridad

1. Lee el comando antes de ejecutarlo.
2. Comprueba que estás en el repositorio correcto.
3. Empieza por `help`.
4. Distingue datos offline de datos live.
5. No conviertas una recomendación en un cambio sin autorización.
6. Si aparece un error, léelo completo y no pruebes opciones al azar.

## Códigos de salida

- `0`: el comando terminó correctamente.
- `1`: la consulta terminó, pero encontró una condición no satisfactoria.
- `2`: el comando o sus argumentos no son válidos.

## Siguiente paso

Continúa con [Cómo leer un Status](como-leer-un-status.md) y realiza las actividades de [Frankie Core](actividades-frankie-core.md).
