# Backups

## Proposito

Documentar estrategias de copia y restauración.

## Estructura sugerida

```markdown
## Backup

- Origen:
- Destino:
- Frecuencia:
- Retencion:
- Validacion:
- Restauracion:
```

## Regla

Un backup no probado no debe considerarse recuperable.

## Estado conocido

### srv-servicios

- Origen: PostgreSQL, datos de n8n y stacks Docker.
- Destino documentado: `/srv/docker/backups`.
- Frecuencia documentada: diaria.
- Evidencia: auditorias y mantenimientos documentados en `docs/evidencias/`.

### srv-recursos

- Origen: `/srv/recursos` y `/etc/samba/smb.conf`.
- Destino documentado: `/srv/backups/recursos`.
- Script instalado: `/srv/scripts/backup-recursos.sh`.
- Frecuencia documentada: diaria mediante cron.
- ISOs: excluidas por defecto para evitar backups pesados.
- Evidencia: `docs/evidencias/paso-7-mantenimiento/informe_mantenimiento_2026-06-26.md`.
