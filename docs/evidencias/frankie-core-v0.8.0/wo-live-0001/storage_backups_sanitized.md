# Almacenamiento y backups saneados

## Almacenamiento

- Proxmox: dos almacenamientos activos con ocupación inferior al 4 %.
- Host: dos discos físicos de aproximadamente 931,5 GiB.
- VM100: disco virtual 100 GiB; raíz LVM 48,5 GiB, 26 % utilizado.
- VM101: disco virtual 400 GiB; raíz LVM 100 GiB, 18 % utilizado.

Existe capacidad virtual no asignada al volumen raíz en ambas VMs, especialmente en VM101. No constituye una incidencia mientras sea intencionada, pero debe documentarse antes de ampliar filesystems.

## Backups

La allowlist no incluía listado de directorios, planificadores o metadatos de copias. Por tanto:

- existencia actual de backups: no verificada;
- última ejecución: no verificada;
- retención: no verificada;
- restaurabilidad: no verificada.

No se abrió, copió, descargó o ejecutó ningún backup. Se recomienda `WO-LIVE-0004` para esta validación específica.
