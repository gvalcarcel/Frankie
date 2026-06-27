# Cómo leer un Status

## Qué es Status

Status es una vista rápida del estado conocido de Frankie.

```bash
python -m frankie status
```

No consulta el servidor en directo. Resume la documentación y las evidencias que ya existen en el repositorio.

## Orden de lectura

1. Mira `Version` y `Mode`.
2. Revisa el servidor físico.
3. Revisa las máquinas virtuales.
4. Observa servicios, seguridad y backups.
5. Lee las evidencias disponibles.
6. Termina con `Overall status`.

## Estados habituales

### OK

La evidencia disponible indica un estado correcto.

### WARNING

Hay algo que conviene revisar. No significa que el servicio esté roto ni que debamos cambiarlo inmediatamente.

### UNKNOWN

No hay información suficiente para afirmar un estado.

## Ejemplo actual

- Samba aparece como `OK` porque existe evidencia que valida SMB.
- Portainer aparece como `WARNING` por la publicación documentada del puerto `8000`.
- El estado global es `WARNING` porque conserva ese aviso.

## Una comparación sencilla

Status se parece al cuadro de instrumentos de un vehículo. Resume señales importantes, pero no sustituye una revisión completa.

## Límites

- Un `OK` puede quedar antiguo si no se actualizan las evidencias.
- Un `WARNING` necesita análisis, no una reacción automática.
- Status no ejecuta reparaciones.

Prácticas relacionadas: actividades 2, 3 y 7 de [Actividades Frankie Core](actividades-frankie-core.md).
