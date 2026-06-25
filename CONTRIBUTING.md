# Contributing

## Principios

- Frankie es un producto software, no una carpeta de scripts.
- El repositorio es la fuente unica de verdad.
- Todo cambio debe ser revisable, trazable y documentado.
- No se deben subir secretos reales.

## Contribuciones humanas

Antes de proponer cambios:

1. Leer `README.md`.
2. Revisar `governance/PROJECT_RULES.md`.
3. Crear una rama descriptiva.
4. Hacer cambios pequenos y revisables.
5. Actualizar documentacion si cambia comportamiento.
6. Abrir Pull Request.

## Contribuciones con IA

Las contribuciones asistidas por IA deben:

- indicar que han sido generadas o asistidas por IA,
- no inventar estado de servidores,
- no incluir secretos,
- mantener lenguaje tecnico claro,
- respetar estructura del repositorio,
- incluir evidencias cuando se hable de estado real.

## Reglas de seguridad

No subir:

- `.env` reales,
- contrasenas,
- tokens,
- claves privadas,
- dumps reales,
- backups reales,
- datos personales innecesarios.

## Cambios sobre scripts

Los scripts deben:

- soportar `--dry-run`,
- ser idempotentes,
- incluir validaciones,
- evitar cambios destructivos,
- documentar rollback si aplica.

## Pull Requests

Todo PR debe explicar:

- objetivo,
- alcance,
- riesgos,
- pruebas realizadas,
- impacto en documentacion.
