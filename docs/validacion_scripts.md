# Validacion controlada de scripts

## Objetivo

Definir un procedimiento seguro para revisar y validar los scripts de automatizacion del proyecto Frankie antes de permitir su ejecucion real sobre las VMs `srv-servicios` y `srv-recursos`.

Este documento no autoriza la ejecucion directa en produccion. Sirve para decidir si cada script esta listo, requiere revision o no debe ejecutarse.

## Requisitos previos

- Acceso administrativo controlado a Proxmox.
- Snapshots recientes de las VMs implicadas.
- Backup logico validado de n8n/PostgreSQL antes de tocar `srv-servicios`.
- Backup de `/srv/recursos` y `/etc/samba/smb.conf` antes de tocar `srv-recursos`.
- IPs actuales conocidas o reserva DHCP aplicada.
- Lectura completa de cada script antes de ejecutarlo.
- `.env` reales preparados fuera de Git, solo si el script los requiere.

## Advertencia principal

No ejecutar scripts reales sin snapshot previo.

Antes de una ejecucion real:

1. Crear snapshot Proxmox.
2. Confirmar backup.
3. Ejecutar auditoria de solo lectura.
4. Ejecutar `--dry-run`.
5. Revisar salida.
6. Ejecutar solo un script cada vez.
7. Validar.
8. Documentar resultado.

## Orden recomendado de pruebas

### srv-servicios

```bash
cd scripts/srv-servicios
./01_instalar_dependencias.sh --dry-run
./02_instalar_docker.sh --dry-run
./03_crear_red_docker.sh --dry-run
./04_desplegar_portainer.sh --dry-run
./05_desplegar_postgres.sh --dry-run
./06_desplegar_n8n.sh --dry-run
./07_configurar_backup.sh --dry-run
./08_configurar_seguridad.sh --dry-run
```

### srv-recursos

```bash
cd scripts/srv-recursos
./01_instalar_samba.sh --dry-run
./02_crear_usuarios_samba.sh --dry-run
./03_crear_estructura_recursos.sh --dry-run
./04_aplicar_permisos.sh --dry-run
./05_configurar_smb_conf.sh --dry-run
./06_configurar_firewall.sh --dry-run
./07_configurar_backup_recursos.sh --dry-run
```

## Auditoria previa de solo lectura

Los scripts de auditoria no modifican el sistema.

```bash
./scripts/auditoria/auditar_srv-servicios.sh
./scripts/auditoria/auditar_srv-recursos.sh
```

## Comandos de validacion manual

### srv-servicios

```bash
hostnamectl
docker ps
docker network ls
docker volume ls
ss -tlnp
ufw status verbose
fail2ban-client status sshd
crontab -l
ls -lah /srv/docker/backups
curl -I http://localhost:5678
```

### srv-recursos

```bash
hostnamectl
systemctl status smbd --no-pager
testparm -s
ss -tlnp
ufw status verbose
getent group alumnado
getent group profesorado
id alumno
id profesor
pdbedit -L
ls -ld /srv/recursos /srv/recursos/02_ISOS /srv/recursos/99_PROFESORADO
```

## Criterios para considerar un script validado

- El dry-run muestra solo acciones esperadas.
- No aparecen rutas destructivas inesperadas.
- No aparecen contrasenas, tokens ni secretos.
- El script comprueba prerrequisitos.
- El script no duplica recursos existentes.
- La validacion posterior es clara.
- Existe rollback documentado.

## Criterios para detener la ejecucion

Detener si aparece cualquiera de estas condiciones:

- El script intenta borrar datos sin confirmacion.
- El script usa `rm -rf` sobre rutas variables o ambiguas.
- El script muestra secretos.
- El script cambia firewall de forma no prevista.
- El script reinicia servicios criticos sin estar documentado.
- Falta snapshot.
- Falta backup.
- Faltan `.env` reales requeridos.
- La IP actual no coincide con la documentada.
- La auditoria previa muestra servicios fallidos.

## Estrategia de rollback

### Preferente

Revertir snapshot Proxmox de la VM afectada.

### Configuracion

Restaurar backups de configuracion:

- Samba: `/etc/samba/smb.conf.*.bak`.
- Docker Compose: copia previa del stack.
- Backups: restaurar script anterior si existia.

### Datos

Restaurar desde backup validado:

- PostgreSQL desde dump.
- n8n desde tar.gz de `/srv/docker/n8n/data`.
- stacks desde tar.gz de `/srv/docker/stacks`.
- recursos desde backup de `/srv/recursos`.

## Registro

Cada prueba debe documentar:

- Fecha.
- VM.
- Script.
- Modo `--dry-run` o real.
- Resultado.
- Evidencias.
- Decision: apto, revisar o no ejecutar.
