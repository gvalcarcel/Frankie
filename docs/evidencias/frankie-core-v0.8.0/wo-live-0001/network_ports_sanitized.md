# Red y puertos saneados

No se versionan direcciones o MACs. Se conservan únicamente puertos escuchando y su interpretación lógica.

## Host Proxmox

Puertos observados: `22`, `25`, `68`, `85`, `111`, `323`, `3128` y `8006`.

- `8006`: interfaz Proxmox.
- `3128`: proxy SPICE de Proxmox.
- `22`: administración SSH.
- `25`, `85`, `111`, `323` y `68`: requieren mantener trazabilidad de propósito y exposición, sin clasificarlos automáticamente como incidencia.

## VM100

Puertos observados: `22`, `53`, `68`, `323`, `5678`, `8000` y `9443`.

- UFW activo; entrada denegada por defecto.
- UFW permite `22`, `5678` y `9443` para IPv4 e IPv6.
- Portainer publica y escucha `8000`, pero UFW no lo permite. Se confirma el warning histórico.
- PostgreSQL `5432` no aparece publicado ni escuchando en el host.

## VM101

Puertos observados: `22`, `53`, `68`, `139`, `323` y `445`.

- UFW activo; entrada denegada por defecto.
- UFW permite SSH y los puertos Samba `137/udp`, `138/udp`, `139/tcp` y `445/tcp` para IPv4 e IPv6.
- Las reglas Samba aceptan origen `Anywhere`; conviene revisar en otra WO si deben limitarse a la red docente.

## Riesgo

- Portainer `8000`: bajo, warning conocido.
- Samba desde cualquier origen alcanzable: medio hasta confirmar segmentación efectiva.
- Puertos de infraestructura Proxmox no explicados en esta captura: revisión futura, sin cambio recomendado todavía.
