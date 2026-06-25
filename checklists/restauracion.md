# Checklist de restauración basica

## Advertencia

Las restauraciónes deben probarse antes de necesitarlas. Un backup no validado no debe considerarse recuperable.

## Antes de restaurar

- [ ] Identificar incidencia.
- [ ] Avisar a usuarios afectados.
- [ ] Confirmar ultimo backup valido.
- [ ] Confirmar snapshot disponible.
- [ ] Documentar hora de inicio.

## srv-servicios

- [ ] Parar servicios si es necesario.
- [ ] Confirmar dump PostgreSQL seleccionado.
- [ ] Descomprimir dump si está en `.sql.gz`.
- [ ] Restaurar PostgreSQL desde dump validado.
- [ ] Confirmar tar.gz de `/srv/docker/n8n/data`.
- [ ] Restaurar `/srv/docker/n8n/data` si procede.
- [ ] Restaurar `/srv/docker/stacks` si procede.
- [ ] Ajustar permisos de `/srv/docker/n8n/data` si procede.
- [ ] Levantar contenedores.
- [ ] Validar acceso a n8n.
- [ ] Validar logs de PostgreSQL.
- [ ] Ejecutar backup nuevo tras restaurar.

## srv-recursos

- [ ] Restaurar `/srv/recursos` si procede.
- [ ] Restaurar `/etc/samba/smb.conf` si procede.
- [ ] Ejecutar `testparm -s`.
- [ ] Recargar `smbd`.
- [ ] Validar acceso SMB desde cliente.
- [ ] Validar lectura de `alumno`.
- [ ] Validar escritura de `profesor`.
- [ ] Validar restriccion de `99_PROFESORADO`.

## Cierre

- [ ] Documentar causa.
- [ ] Documentar backup usado.
- [ ] Documentar validaciones.
- [ ] Registrar tareas preventivas.
