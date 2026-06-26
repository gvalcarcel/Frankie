# Checklist de mantenimiento del servidor

## Antes de empezar

- [ ] Confirmada la VM afectada.
- [ ] Confirmada la IP actual.
- [ ] Confirmado acceso SSH.
- [ ] Snapshot Proxmox creado.
- [ ] Backup reciente confirmado.
- [ ] Usuarios avisados si procede.
- [ ] Auditoría de solo lectura ejecutada.
- [ ] Servicios fallidos revisados con `systemctl --failed`.

## srv-servicios

- [ ] `docker ps` muestra `n8n`, `postgres` y `portainer` activos.
- [ ] PostgreSQL no expone `5432` al host.
- [ ] n8n responde en `5678`.
- [ ] Portainer responde en `9443`.
- [ ] UFW está activo.
- [ ] Fail2ban está activo.
- [ ] Backups existen en `/srv/docker/backups`.
- [ ] `apt upgrade --dry-run` revisado.
- [ ] Actualización ejecutada solo si el dry-run era seguro.
- [ ] Limpieza Docker revisada antes de ejecutar.
- [ ] No se han eliminado volúmenes Docker.
- [ ] Validación posterior completada.

## srv-recursos

- [ ] `smbd` está activo.
- [ ] `/srv/recursos` existe.
- [ ] Usuarios `alumno` y `profesor` existen.
- [ ] Grupos `alumnado` y `profesorado` existen.
- [ ] Usuarios Samba registrados.
- [ ] `testparm -s` valida la configuración.
- [ ] `02_ISOS` permite escritura a profesorado.
- [ ] `99_PROFESORADO` sigue restringida.
- [ ] UFW está activo.
- [ ] Puertos Samba esperados escuchan.
- [ ] `apt upgrade --dry-run` revisado.
- [ ] Actualización ejecutada solo si el dry-run era seguro.
- [ ] Validación posterior completada.

## Documentación

- [ ] Fecha de intervención registrada.
- [ ] VM afectada registrada.
- [ ] Comandos relevantes documentados.
- [ ] Resultado final documentado.
- [ ] Incidencias añadidas a `docs/incidencias.md` si procede.
- [ ] Evidencias publicables guardadas en `docs/evidencias/`.
- [ ] Evidencias sensibles mantenidas fuera del repositorio público.

## Decisión final

- [ ] Mantenimiento correcto.
- [ ] Mantenimiento correcto con observaciones.
- [ ] Requiere revisión.
- [ ] Revertido mediante rollback.
