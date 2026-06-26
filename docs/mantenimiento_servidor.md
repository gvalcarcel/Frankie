# Mantenimiento, actualización y optimización del servidor

## Objetivo

Definir un procedimiento controlado para actualizar, optimizar y validar la plataforma Frankie sin perder trazabilidad ni poner en riesgo los servicios de aula.

Este documento no sustituye a los snapshots, backups ni validaciones manuales. Toda intervención real sobre `srv-servicios` o `srv-recursos` debe ejecutarse de forma planificada, una VM cada vez y con evidencias posteriores.

## Alcance

Aplica a:

- VM100 `srv-servicios`: Docker, Portainer, PostgreSQL, n8n, UFW, Fail2ban y backups.
- VM101 `srv-recursos`: Samba, `/srv/recursos`, usuarios, grupos, permisos y firewall.
- Documentación, evidencias y checklists del repositorio Frankie.

No incluye:

- Cambios destructivos.
- Rotación de contraseñas.
- Publicación de secretos.
- Automatización sin revisión humana.
- Actualizaciones masivas sin snapshot.

## Principios de mantenimiento

- No ejecutar cambios reales sin snapshot vigente.
- No actualizar ambas VMs a la vez.
- No reiniciar servicios críticos sin comprobar usuarios conectados.
- No aplicar cambios si las IPs actuales no están confirmadas.
- No mezclar diagnóstico, actualización y corrección de incidencias en una sola ejecución.
- Documentar siempre fecha, VM, comandos ejecutados, resultado y desviaciones.

## Requisitos previos

Antes de intervenir:

1. Confirmar IP actual de cada VM desde Proxmox o consola.
2. Confirmar acceso SSH.
3. Crear snapshot Proxmox de la VM afectada.
4. Confirmar backup reciente.
5. Ejecutar auditoría de solo lectura.
6. Revisar servicios activos.
7. Avisar si hay usuarios usando n8n o recursos Samba.

## Orden recomendado

### 1. srv-servicios

1. Ejecutar auditoría de solo lectura.
2. Confirmar backups de PostgreSQL, n8n y stacks.
3. Actualizar paquetes del sistema.
4. Revisar reinicio pendiente.
5. Actualizar imágenes Docker solo si hay rollback claro.
6. Revisar contenedores.
7. Limpiar recursos Docker no usados con prudencia.
8. Validar n8n, PostgreSQL, Portainer, UFW y Fail2ban.
9. Documentar evidencias.

### 2. srv-recursos

1. Ejecutar auditoría de solo lectura.
2. Confirmar backup de `/srv/recursos` y `/etc/samba/smb.conf`.
3. Actualizar paquetes del sistema.
4. Revisar reinicio pendiente.
5. Validar Samba con `testparm -s`.
6. Revisar permisos principales.
7. Validar acceso de `alumno` y `profesor`.
8. Validar firewall.
9. Documentar evidencias.

## Comandos de diagnóstico previos

### Comunes

```bash
hostnamectl
ip -br addr
uptime
df -h
free -h
systemctl --failed
sudo apt update
apt list --upgradable
```

### srv-servicios

```bash
sudo ./scripts/auditoria/auditar_srv-servicios.sh
docker ps
docker network ls
docker volume ls
sudo ufw status verbose
sudo fail2ban-client status sshd
ls -lah /srv/docker/backups
```

### srv-recursos

```bash
sudo ./scripts/auditoria/auditar_srv-recursos.sh
systemctl status smbd --no-pager
testparm -s
sudo ufw status verbose
getent group alumnado
getent group profesorado
id alumno
id profesor
ls -ld /srv/recursos /srv/recursos/02_ISOS /srv/recursos/99_PROFESORADO
```

## Actualización segura del sistema

Ejecutar solo después de snapshot y backup:

```bash
sudo apt update
sudo apt upgrade
```

Si se desea una ejecución no interactiva, debe revisarse antes:

```bash
sudo apt upgrade --dry-run
```

No ejecutar `dist-upgrade`, `full-upgrade` ni cambios de versión de Ubuntu sin plan específico.

## Optimización prudente

### Sistema

```bash
sudo apt autoremove --dry-run
sudo apt autoclean --dry-run
```

Ejecutar la acción real solo si el dry-run muestra paquetes esperados:

```bash
sudo apt autoremove
sudo apt autoclean
```

### Docker en srv-servicios

Revisar primero:

```bash
docker system df
docker image ls
docker container ls -a
```

No usar `docker system prune -a` sin revisar el impacto.

Limpieza prudente:

```bash
docker container prune
docker image prune
docker network prune
```

No eliminar volúmenes Docker sin backup y confirmación explícita.

### Samba en srv-recursos

Validar configuración antes de recargar:

```bash
testparm -s
```

Recargar solo si la validación es correcta:

```bash
sudo systemctl reload smbd
```

## Validación posterior

### srv-servicios

```bash
docker ps
docker inspect postgres --format '{{json .NetworkSettings.Ports}}'
ss -tlnp
curl -I http://127.0.0.1:5678
sudo ufw status verbose
sudo fail2ban-client status sshd
```

Criterios mínimos:

- `n8n`, `postgres` y `portainer` están activos.
- PostgreSQL no publica `5432` hacia el host.
- n8n responde en `5678`.
- Portainer responde en `9443`.
- UFW sigue activo.
- Fail2ban sigue activo.
- Backups siguen presentes.

### srv-recursos

```bash
systemctl status smbd --no-pager
testparm -s
ss -tlnp
sudo ufw status verbose
ls -ld /srv/recursos /srv/recursos/02_ISOS /srv/recursos/99_PROFESORADO
```

Criterios mínimos:

- Samba está activo.
- `testparm -s` no muestra errores.
- Puertos `139/tcp` y `445/tcp` escuchan.
- `alumno` mantiene lectura.
- `profesor` mantiene escritura donde corresponde.
- `99_PROFESORADO` sigue restringida.

## Criterios de parada

Detener la intervención si ocurre cualquiera de estos casos:

- La VM cambia de IP y no se puede confirmar la nueva.
- Falla el backup.
- No existe snapshot reciente.
- Hay servicios fallidos antes de actualizar.
- `apt upgrade --dry-run` propone eliminar paquetes críticos.
- Docker muestra contenedores detenidos inesperadamente.
- Samba no valida con `testparm -s`.
- UFW queda inactivo.
- Aparecen secretos o rutas sensibles en la salida que no deban documentarse.

## Rollback

Orden recomendado:

1. Detener la intervención.
2. Guardar evidencias del fallo.
3. No ejecutar más cambios.
4. Si el fallo es de configuración, restaurar backup específico.
5. Si el fallo afecta a servicios críticos, revertir snapshot Proxmox.
6. Documentar la incidencia en `docs/incidencias.md`.

## Evidencias a conservar

Guardar en `docs/evidencias/` si son publicables:

- Auditoría previa.
- Lista de paquetes actualizados.
- Validación posterior.
- Incidencias detectadas.
- Decisión final: correcto, revertido o pendiente.

Si contienen IPs internas, usuarios reales, nombres sensibles o datos privados, deben mantenerse fuera del repositorio público.
