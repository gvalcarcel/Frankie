# VM101: Samba saneado

- Identidad lógica confirmada: VM101 `srv-recursos`; hostname efectivo sin guion documentado y aceptado.
- Sistema: Ubuntu 26.04 LTS.
- Uptime: casi cuatro días; carga baja.
- Filesystem raíz: 98 GiB, 18 % utilizado.
- Disco virtual: 400 GiB; volumen lógico raíz de 100 GiB.
- `smbd`: activo.
- `nmbd`: inactivo.
- Samba: `4.23.6` del repositorio Ubuntu.
- Sesiones: sin ficheros bloqueados durante la captura.

## Comparticiones declaradas

- `recursos`, `instalables`, `isos`, `material`, `plantillas`, `practicas` y `profesorado`.
- También existen las comparticiones de impresión estándar `printers` y `print$`.

No se registraron usuarios, grupos, direcciones de clientes, rutas reales o credenciales. Esta captura no repite pruebas de escritura desde Windows.
