# Línea base de seguridad saneada

| Componente | Estado observado |
| --- | --- |
| Proxmox core services | activos |
| VM100 Docker | activo |
| VM100 Fail2ban | activo |
| VM100 UFW | activo, entrada denegada por defecto |
| VM101 Samba | `smbd` activo |
| VM101 UFW | activo, entrada denegada por defecto |
| PostgreSQL externo | no expuesto en `5432` |
| Repair Mode | no usado |

## Observaciones

- Portainer `8000` continúa publicado, aunque UFW no lo permite.
- n8n `5678` y Portainer `9443` están permitidos desde cualquier origen alcanzable.
- Los puertos Samba están permitidos desde cualquier origen alcanzable.
- `nmbd` está inactivo; SMB directo por `139/445` permanece operativo.
- La captura no evaluó parches pendientes, configuración SSH, jails Fail2ban, certificados o contenido de logs.

La preparación de acceso temporal fue realizada por el propietario. El agente no cambió servicios ni configuraciones durante la captura.
