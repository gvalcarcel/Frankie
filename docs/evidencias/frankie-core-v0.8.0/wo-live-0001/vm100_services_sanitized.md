# VM100: servicios saneados

- Identidad lógica confirmada: VM100 `srv-servicios`; hostname efectivo divergente documentado y aceptado por el propietario.
- Sistema: Ubuntu 26.04 LTS.
- Uptime: casi cuatro días; carga baja.
- Filesystem raíz: 48 GiB, 26 % utilizado.
- Disco virtual: 100 GiB; volumen lógico raíz de aproximadamente 48,5 GiB.
- Docker: activo.
- Fail2ban: activo.
- Red Docker `aula-network`: presente.
- Volúmenes Docker nombrados: uno; los bind mounts no aparecen en este recuento.

## Contenedores

| Contenedor | Imagen | Estado | Publicación observada |
| --- | --- | --- | --- |
| n8n | imagen oficial latest | activo durante casi cuatro días | `5678` publicado |
| PostgreSQL | `postgres:17` | activo durante casi cuatro días | `5432` solo interno, sin publicación al host |
| Portainer CE | imagen latest | activo durante casi cuatro días | `8000` y `9443` publicados; `9000` solo interno |

No se inspeccionaron variables de entorno, secretos, volúmenes de contenido o logs.
