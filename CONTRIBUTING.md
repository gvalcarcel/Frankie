# Contributing

## Estado actual del proyecto

Frankie es un repositorio publico, pero no es actualmente un proyecto comunitario abierto.

El repositorio se publica con finalidad documental, educativa y de portfolio tecnico. El codigo, la documentacion y las decisiones tecnicas son visibles publicamente, pero la gestion del proyecto corresponde exclusivamente al propietario del repositorio.

No se aceptan contribuciones externas no solicitadas por defecto. Las issues, pull requests, propuestas de cambios o solicitudes externas podran cerrarse sin revision si no han sido solicitadas expresamente por el propietario.

## Gobierno del repositorio

El propietario mantiene el control sobre:

- Roadmap.
- Prioridades.
- Cambios aceptados.
- Versiones.
- Releases.
- Publicacion de evidencias.
- Criterios de seguridad.

Las contribuciones futuras podran valorarse si el propietario decide abrir esa posibilidad para un caso concreto.

## Forks

Cualquier fork de Frankie es responsabilidad de quien lo mantenga.

Un fork no representa necesariamente el estado, las decisiones, la seguridad ni la direccion oficial del proyecto original.

## Propuestas externas

Si en el futuro se solicita una colaboracion concreta, cualquier propuesta debera:

1. Estar alineada con el roadmap aprobado por el propietario.
2. Respetar la arquitectura y las reglas de gobierno del proyecto.
3. Mantener la documentacion actualizada.
4. Evitar cambios innecesarios sobre servidores, scripts o configuraciones.
5. Ser revisable, trazable y limitada en alcance.

## Contribuciones con IA

Las contribuciones asistidas por IA solo se consideraran cuando hayan sido solicitadas por el propietario.

En ese caso, deben:

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
- IPs reales o internas no autorizadas,
- evidencias internas,
- configuraciones privadas,
- datos personales innecesarios.

## Cambios sobre scripts

Los scripts deben:

- soportar `--dry-run`,
- ser idempotentes,
- incluir validaciones,
- evitar cambios destructivos,
- documentar rollback si aplica.

## Pull Requests

Actualmente los Pull Requests externos no solicitados no se aceptan por defecto.

Si el propietario solicita expresamente un Pull Request, este debe explicar:

- objetivo,
- alcance,
- riesgos,
- pruebas realizadas,
- impacto en documentacion.
