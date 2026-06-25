# Seguridad

## Principios

- No versionar secretos.
- Minimizar puertos expuestos.
- Separar usuarios de alumnado y profesorado.
- Mantener backups y snapshots antes de cambios relevantes.
- Documentar riesgos aceptados.

## Puertos previstos

### srv-servicios

- `22/tcp`: SSH.
- `5678/tcp`: n8n.
- `9443/tcp`: Portainer.

### srv-recursos

- `22/tcp`: SSH.
- `139/tcp`, `445/tcp`: Samba.
- `137/udp`, `138/udp`: Samba/NetBIOS si se mantiene habilitado.

## Secretos

Nunca incluir en Git:

- `.env` reales.
- Passwords SMTP.
- Passwords PostgreSQL.
- Tokens OAuth.
- Claves privadas SSH.

## Pendientes

- Reservas DHCP.
- Estrategia HTTPS para n8n.
- Validacion de restauracion.
- Politica de rotacion de credenciales.
