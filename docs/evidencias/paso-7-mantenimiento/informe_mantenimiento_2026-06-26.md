# Informe de mantenimiento - Paso 7

## Fecha

2026-06-26

## Objetivo

Revisar el estado actual de las VMs principales de Frankie, aplicar mantenimiento conservador y corregir una carencia operativa detectada previamente: ausencia de backup real instalado en `srv-recursos`.

## Alcance ejecutado

- Comprobacion de conectividad SSH.
- Auditoria previa de bajo riesgo.
- Actualizacion de indices APT.
- Simulacion de actualizacion con `apt-get -s upgrade`.
- Limpieza prudente con `apt-get autoremove` y `apt-get autoclean`.
- Limpieza Docker no destructiva en `srv-servicios`.
- Instalacion de backup diario en `srv-recursos`.
- Ejecucion manual de una primera copia de backup en `srv-recursos`.
- Validacion posterior de servicios.

No se ejecuto:

- `full-upgrade`.
- Cambio de version de Ubuntu.
- Reinicio de VMs.
- Reinicio de servicios de aula.
- Eliminacion de volumenes Docker.
- Cambios de contrasenas.
- Cambios de firewall.
- Cambios funcionales de Samba.

## srv-servicios

### Estado previo

- Hostname observado: `frankie`.
- Ubuntu Server 26.04 LTS.
- Sin unidades systemd fallidas.
- Docker activo.
- Contenedores activos:
  - `n8n`
  - `postgres`
  - `portainer`
- PostgreSQL no expone `5432` al host.
- n8n responde localmente en `5678`.
- UFW activo.
- Fail2ban activo.
- Backups de servicios presentes.
- Disco raiz al 25% de uso.

### Actualizacion

Se ejecuto:

```bash
sudo apt-get update
sudo apt-get -s upgrade
```

Resultado:

- 0 paquetes pendientes de actualizacion normal.
- 0 paquetes nuevos.
- 0 paquetes eliminados.
- 3 metapaquetes de kernel retenidos:
  - `linux-generic`
  - `linux-headers-generic`
  - `linux-image-generic`

No se forzo la actualizacion de kernel porque requiere una ventana especifica y plan de reinicio.

### Optimizacion

Se ejecuto:

```bash
sudo apt-get autoremove -y
sudo apt-get autoclean
docker image prune -f
docker container prune -f
docker network prune -f
```

Resultado:

- No habia paquetes APT para retirar.
- Docker no recupero espacio adicional.
- No se eliminaron volumenes Docker.
- Los contenedores activos siguieron operativos.

### Validacion posterior

Resultado:

- Sin unidades systemd fallidas.
- `n8n`, `postgres` y `portainer` activos.
- PostgreSQL sigue sin publicar `5432` hacia el host.
- n8n responde por HTTP en local.
- UFW activo.
- Fail2ban activo.
- Disco raiz al 25% de uso.

## srv-recursos

### Estado previo

- Hostname observado: `srvrecursos`.
- Ubuntu Server 26.04 LTS.
- Sin unidades systemd fallidas.
- Samba activo.
- `testparm -s` correcto.
- Puertos Samba `139/tcp` y `445/tcp` escuchando.
- UFW activo.
- Permisos principales correctos:
  - `/srv/recursos`
  - `/srv/recursos/02_ISOS`
  - `/srv/recursos/99_PROFESORADO`
- Disco raiz al 17% de uso.

### Actualizacion

Se ejecuto:

```bash
sudo apt-get update
sudo apt-get -s upgrade
```

Resultado:

- 0 paquetes pendientes de actualizacion normal.
- 0 paquetes nuevos.
- 0 paquetes eliminados.
- 3 metapaquetes de kernel retenidos:
  - `linux-generic`
  - `linux-headers-generic`
  - `linux-image-generic`

No se forzo la actualizacion de kernel.

### Backup de recursos

Se reviso el script:

```text
scripts/srv-recursos/07_configurar_backup_recursos.sh
```

Dry-run correcto:

- creacion prevista de `/srv/backups/recursos/logs`;
- creacion prevista de `/srv/scripts/backup-recursos.sh`;
- instalacion prevista de cron diario;
- sin cambios inesperados.

Tamanos observados antes de ejecutar:

- `/srv/recursos`: 8,8 GB.
- `/srv/recursos` excluyendo `/srv/recursos/02_ISOS`: 36 KB.

Se ejecuto el script real con la configuracion por defecto:

```bash
sudo bash /tmp/07_configurar_backup_recursos.sh
```

Resultado:

- Script instalado en `/srv/scripts/backup-recursos.sh`.
- Cron instalado:

```text
0 2 * * * /srv/scripts/backup-recursos.sh
```

- Directorio de backups creado:

```text
/srv/backups/recursos
```

- Primera copia manual ejecutada correctamente:

```text
recursos_20260626_120732.tar.gz
smb.conf_20260626_120732
```

El backup excluye ISOs por defecto mediante `BACKUP_ISOS=false`, para evitar copias pesadas innecesarias.

### Optimizacion

Se ejecuto:

```bash
sudo apt-get autoremove -y
sudo apt-get autoclean
```

Resultado:

- No habia paquetes APT para retirar.
- No se modificaron recursos compartidos.
- No se modifico la configuracion funcional de Samba.

### Validacion posterior

Resultado:

- Sin unidades systemd fallidas.
- Samba activo.
- `testparm -s` correcto.
- Puertos Samba escuchando.
- UFW activo.
- Backup real de recursos instalado.
- Cron diario de backup de recursos activo.
- Primera copia de backup generada.
- Disco raiz al 17% de uso.

## Riesgos y observaciones

- Los metapaquetes de kernel siguen retenidos en ambas VMs. Se recomienda planificar una ventana especifica si se decide actualizar kernel.
- `srv-servicios` mantiene el puerto Docker `8000` publicado en Portainer, aunque UFW no lo permite. Se conserva como observacion conocida.
- La validacion SMB desde un cliente Windows real sigue siendo recomendable para cerrar por completo la evidencia de uso en aula.
- El backup de `srv-recursos` excluye ISOs por defecto. Si en el futuro se quieren respaldar ISOs, debe revisarse capacidad y retencion antes de cambiar `BACKUP_ISOS=true`.

## Cambios reflejados en el repositorio

- Se documenta esta intervencion en `docs/evidencias/paso-7-mantenimiento/`.
- Frankie Core incorpora esta evidencia como fuente local.
- `frankie status` puede reflejar `srv-recursos backups` como `OK`.
- `frankie inventory` puede reflejar el backup de `srv-recursos` como conocido.

## Decision final

```text
mantenimiento correcto con mejora aplicada
```

Las dos VMs quedaron operativas tras la intervencion. La mejora principal es que `srv-recursos` dispone ahora de backup diario instalado y validado con una primera copia manual.
