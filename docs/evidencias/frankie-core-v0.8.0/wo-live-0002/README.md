# WO-LIVE-0002: retirada del acceso temporal LIVE

Evidencia saneada de la retirada controlada, realizada el 2026-06-29, de los accesos temporales habilitados para WO-LIVE-0001.

## Alcance

- Clave temporal autorizada en el host Proxmox.
- Fichero temporal `frankie-live-readonly` de `sudoers` en VM100.
- Fichero temporal `frankie-live-readonly` de `sudoers` en VM101.

No se reiniciaron sistemas ni se modificaron servicios. Este paquete no contiene direcciones internas, usuarios, claves, credenciales ni salidas brutas.

## Resultado

Los tres accesos temporales quedaron fuera de sus ubicaciones activas. La configuración SSH del host y la configuración global de `sudoers` de ambas VMs superaron sus validaciones sintácticas.

La decisión final es: **acceso temporal retirado correctamente**.

