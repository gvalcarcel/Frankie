# Estado saneado de Proxmox

- Captura: 2026-06-29.
- Modo: LIVE de solo lectura mediante clave temporal y wrapper forzado.
- Sistema: Debian 13, kernel Proxmox `7.0.6-2-pve`.
- Proxmox VE: `9.2.3`.
- Servicios `pveproxy`, `pvedaemon` y `pvestatd`: activos.
- VM100 `srv-servicios`: ejecutándose, 8 GiB RAM y disco virtual de 100 GiB.
- VM101 `srv-recursos`: ejecutándose, 4 GiB RAM y disco virtual de 400 GiB.
- Almacenamientos `local` y `local-zfs`: activos.
- Uso observado: `local` 0,31 %; `local-zfs` 3,60 %.
- Host: dos discos físicos de aproximadamente 931,5 GiB.
- Uptime: superior a cuatro días; carga baja durante la captura.

No se ejecutaron `zpool status`, SMART o pruebas de integridad; “activo” no demuestra salud física ni restaurabilidad.
