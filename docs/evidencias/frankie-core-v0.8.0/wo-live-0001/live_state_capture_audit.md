# Auditoría de captura LIVE de solo lectura

## Identificación

- Work Order: `WO-LIVE-0001`.
- Fecha: 2026-06-29.
- Tipo: `LIVE`, solo lectura.
- Versión Frankie Core: `0.8.0-dev`.
- Cambios realizados por el agente: ninguno.

## Alcance y agentes

Se contactaron el host Proxmox, VM100 y VM101. Se aplicaron LIVE Operations Controller, Proxmox Administrator, Network Administrator, Service Administrator, Storage/Backup Administrator, Security Reviewer, System Auditor, Technical Writer, Evidence Engineer y Repository Maintainer.

## Accesos usados

- Proxmox: clave temporal con huella verificada y `authorized_keys` restringido a un wrapper fijo de lectura.
- VMs: autenticación autorizada y elevación no interactiva limitada por sudoers a comandos concretos de lectura.
- Las credenciales, direcciones, huellas y outputs brutos no se versionan.

La preparación de permisos fue ejecutada por el propietario. Durante la captura, el agente no editó configuración, reinició servicios, instaló paquetes o activó Live Mode.

## Comandos ejecutados

Host: `hostnamectl`, `pveversion`, `qm list`, `qm status 100`, `qm status 101`, `pvesm status`, `lsblk`, `df -h`, `uptime`, `systemctl is-active pveproxy pvedaemon pvestatd`, `ss -tulpen` e `ip -br addr`.

VM100: `hostnamectl`, `cat /etc/os-release`, `uptime`, `df -h`, `lsblk`, `docker ps`, `docker network ls`, `docker volume ls`, estados de Docker y Fail2ban, `ufw status verbose` y `ss -tulpen`.

VM101: `hostnamectl`, `cat /etc/os-release`, `uptime`, `df -h`, `lsblk`, estados de `smbd` y `nmbd`, `testparm -s`, `smbstatus`, `ufw status verbose` y `ss -tulpen`.

## Estado observado

### Proxmox

- Proxmox VE `9.2.3` sobre Debian 13.
- Servicios principales activos.
- VM100 y VM101 ejecutándose con recursos coherentes con la documentación.
- Almacenamientos `local` y `local-zfs` activos, ambos por debajo del 4 % de uso.

### VM100

- Ubuntu 26.04 LTS; Docker y Fail2ban activos.
- n8n, PostgreSQL 17 y Portainer activos durante casi cuatro días.
- `aula-network` presente.
- n8n publica `5678`; Portainer publica `8000` y `9443`.
- PostgreSQL no publica `5432` al host.
- UFW activo con entrada denegada por defecto; permite SSH, n8n y Portainer `9443`, no `8000`.

### VM101

- Ubuntu 26.04 LTS; `smbd` activo y `nmbd` inactivo.
- Comparticiones docentes esperadas presentes, además de recursos estándar de impresión.
- UFW activo; permite SSH y puertos Samba.
- No había ficheros bloqueados durante la captura.

## Red y puertos

- El warning histórico de Portainer `8000` queda confirmado.
- PostgreSQL continúa sin exposición externa.
- Samba escucha en `139/445`; sus reglas UFW aceptan cualquier origen alcanzable.
- Proxmox expone su interfaz `8006` y servicios auxiliares; varios puertos quedan pendientes de justificación documental, sin evidencia de incidencia.

## Backups y almacenamiento

La capacidad y ocupación general se observaron correctamente. La allowlist no permitió listar metadatos de backups o planificadores, por lo que existencia, frescura, retención y restaurabilidad quedan como `UNKNOWN` para `WO-LIVE-0004`.

No se abrieron o copiaron backups ni se ejecutaron pruebas de integridad o restauración.

## Hallazgos

| ID | Severidad | Resultado |
| --- | --- | --- |
| `LIVE-PORTAINER-8000` | baja | warning histórico confirmado |
| `LIVE-SAMBA-SCOPE` | media | revisar si UFW debe limitar Samba a la red docente |
| `LIVE-BACKUPS-MISSING` | media | evidencia actual insuficiente |
| `LIVE-LVM-CAPACITY` | informativa | capacidad virtual no asignada al root en ambas VMs |

No se realizó ninguna reparación. Cada recomendación requiere una WO independiente.

## Saneamiento

- IPs internas eliminadas: sí.
- MACs e identificadores de máquina eliminados: sí.
- Usuarios, correos y credenciales eliminados: sí.
- Outputs brutos versionados: no.
- Contenido de backups o variables de entorno leído: no.

## Validación Frankie Core

```text
python -m frankie version          PASS (0.8.0-dev)
python -m frankie evidence validate PASS (7 válidas, 0 inválidas)
python -m frankie report --json    PASS
python -m unittest discover -s tests PASS (98 tests)
python -m compileall -q frankie    PASS
```

## Confirmaciones

- Captura exclusivamente de lectura: sí.
- Servicios reiniciados o detenidos: ninguno.
- Configuración modificada por el agente: ninguna.
- Live Mode de Frankie Core activado: no.
- Repair Mode usado: no.
- Frankie físico contactado: sí, mediante wrapper restringido.
- VM100 y VM101 contactadas: sí, con comandos allowlist.

## Riesgos y pendientes

- Retirar la clave temporal de Proxmox y los sudoers temporales tras confirmar el cierre.
- El usuario creado manualmente en Proxmox no fue necesario para la captura y debe revisarse o eliminarse por el propietario.
- Limitar Samba y servicios web a redes autorizadas requiere análisis separado.
- La evidencia LIVE aún no está integrada automáticamente en Status o Audit.

## Decisión final

```text
captura live de solo lectura completada
```

La captura se considera completa para el alcance autorizado, con backups expresamente marcados como no verificados.
