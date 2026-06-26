# Informe de mantenimiento - Paso 6

## Fecha

2026-06-26

## Objetivo

Actualizar, optimizar y validar las dos VMs principales del proyecto Frankie:

- `srv-servicios`
- `srv-recursos`

## Alcance ejecutado

- Comprobación de conectividad SSH.
- Auditoría previa básica.
- Simulación de actualización con APT.
- Actualización conservadora con `apt-get upgrade`.
- Limpieza prudente con `apt-get autoremove` y `apt-get autoclean`.
- Optimización Docker segura en `srv-servicios`.
- Validación posterior de servicios.

No se ejecutó:

- `full-upgrade`.
- Cambio de versión de Ubuntu.
- Reinicio de VMs.
- Eliminación de volúmenes Docker.
- Cambios de contraseñas.
- Cambios de configuración Samba.
- Cambios de firewall.

## srv-servicios

### Estado previo

- Sistema sin unidades fallidas.
- Docker activo.
- Contenedores activos:
  - `n8n`
  - `postgres`
  - `portainer`
- UFW activo.
- Fail2ban activo.
- PostgreSQL no expuesto al host por el puerto `5432`.
- Espacio en disco correcto.

### Backup

Se ejecutó el script real de backup:

```bash
sudo /srv/docker/scripts/backup.sh
```

Resultado:

- Backup ejecutado sin error.
- Se generaron nuevas copias de n8n, PostgreSQL y stacks.

### Actualización

Se ejecutó:

```bash
sudo apt update
sudo apt-get upgrade -y
```

Resultado:

- 10 paquetes actualizados.
- 0 paquetes eliminados.
- 0 paquetes nuevos instalados.
- 3 metapaquetes de kernel quedaron retenidos.
- No fue necesario reiniciar servicios.
- No fue necesario reiniciar contenedores.
- No fue necesario reiniciar la VM.

Paquetes actualizados:

- `bpftool`
- `gir1.2-packagekitglib-1.0`
- `libpackagekit-glib2-18`
- `libsgutils2-1.48`
- `linux-libc-dev`
- `linux-perf`
- `linux-tools-common`
- `packagekit`
- `sg3-utils`
- `sg3-utils-udev`

### Optimización

Se ejecutó limpieza prudente:

```bash
sudo apt-get autoremove -y
sudo apt-get autoclean
docker container prune -f
docker image prune -f
docker network prune -f
```

Resultado:

- No había paquetes APT para retirar.
- Se eliminaron 2 contenedores Docker detenidos.
- Se eliminó una red Docker no usada.
- No se eliminaron volúmenes Docker.
- Los contenedores activos siguieron operativos.

### Validación posterior

Resultado:

- Sin unidades systemd fallidas.
- `n8n`, `postgres` y `portainer` activos.
- Red `aula-network` presente.
- n8n responde correctamente en local.
- PostgreSQL sigue sin escuchar en el host por `5432`.
- UFW activo.
- Fail2ban activo.
- Disco raíz al 25% de uso.

## srv-recursos

### Estado previo

- Sistema sin unidades fallidas.
- Samba activo.
- `testparm -s` correcto.
- UFW activo.
- Permisos principales correctos.
- Espacio en disco correcto.

### Backup preventivo

Se realizó copia preventiva de:

- `/etc/samba/smb.conf`
- listado básico de `/srv/recursos`

No se encontró script real de backup de recursos instalado en la VM.

### Actualización

Se ejecutó:

```bash
sudo apt update
sudo apt-get upgrade -y
```

Resultado:

- 11 paquetes actualizados.
- 0 paquetes eliminados.
- 0 paquetes nuevos instalados.
- 3 metapaquetes de kernel quedaron retenidos.
- No fue necesario reiniciar servicios.
- No fue necesario reiniciar la VM.

Paquetes actualizados:

- `tar`
- `bpftool`
- `gir1.2-packagekitglib-1.0`
- `libpackagekit-glib2-18`
- `libsgutils2-1.48`
- `linux-libc-dev`
- `linux-perf`
- `linux-tools-common`
- `packagekit`
- `sg3-utils`
- `sg3-utils-udev`

### Optimización

Se ejecutó:

```bash
sudo apt-get autoremove -y
sudo apt-get autoclean
```

Resultado:

- No había paquetes para retirar.
- No se modificaron recursos compartidos.
- No se modificó Samba.

### Validación posterior

Resultado:

- Sin unidades systemd fallidas.
- `smbd` activo.
- `testparm -s` correcto.
- Puertos Samba escuchando.
- UFW activo.
- Permisos principales intactos:
  - `/srv/recursos`
  - `/srv/recursos/02_ISOS`
  - `/srv/recursos/99_PROFESORADO`
- Disco raíz al 17% de uso.

## Riesgos y observaciones

- Los metapaquetes de kernel quedaron retenidos en ambas VMs. No se forzó su instalación para evitar introducir reinicio o cambio de kernel sin ventana específica.
- `srv-servicios` sigue publicando el puerto Docker `8000` de Portainer, aunque UFW no lo permite. Se mantiene como observación conocida.
- En `srv-recursos` no se encontró script real de backup de recursos instalado. Conviene abordarlo en una fase posterior.
- No se ejecutó validación SMB desde cliente Windows real durante esta intervención.

## Decisión final

```text
mantenimiento correcto con observaciones
```

Las dos VMs quedaron operativas después de la actualización y optimización conservadora.
