# Auditoría de retirada del acceso temporal

## Identificación

- Fecha: 2026-06-29.
- Tipo: LIVE controlado.
- Objetivo: retirar exclusivamente los accesos temporales habilitados para la captura de WO-LIVE-0001.
- Decisión final: **acceso temporal retirado correctamente**.

## Agentes aplicados

- Live Operations Controller.
- Proxmox Virtualization Administrator.
- Service Administrator.
- Security Reviewer.
- System Auditor.
- Technical Writer.
- Repository Maintainer.

## Alcance y ejecución

En el host Proxmox se localizó una única clave autorizada con el marcador temporal previsto. Se creó una copia de seguridad local del fichero afectado, se eliminó únicamente la línea identificada y se comprobó que el marcador ya no aparecía. `sshd -t` finalizó correctamente.

En VM100 y VM101 se comprobó la existencia del fichero temporal `frankie-live-readonly`, se validó antes de retirarlo y se trasladó fuera del directorio activo de `sudoers` a una ubicación de cuarentena restringida a administración. En ambas VMs, `visudo -c` finalizó correctamente y la comprobación posterior confirmó que el fichero ya no estaba activo.

Las operaciones empleadas se limitaron a búsqueda exacta del marcador, copia preventiva, eliminación de la línea identificada, traslado de los ficheros temporales y validaciones sintácticas de SSH y `sudoers`.

## Validaciones

| Componente | Retirada | Validación | Resultado |
|---|---|---|---|
| Host Proxmox | Clave temporal eliminada de `authorized_keys` | Marcador ausente y `sshd -t` correcto | OK |
| VM100 | Fichero temporal fuera de `sudoers.d` | Ausencia confirmada y `visudo -c` correcto | OK |
| VM101 | Fichero temporal fuera de `sudoers.d` | Ausencia confirmada y `visudo -c` correcto | OK |

La clave privada temporal ya había sido destruida al cerrar WO-LIVE-0001. Por ello no se recreó para efectuar una prueba negativa de autenticación; la verificación se basó en la ausencia inequívoca de su marcador en el fichero autorizado y en la validación de SSH.

## Límites respetados

- Sin reinicios de máquinas o servicios.
- Sin cambios en Docker, Samba, Proxmox, UFW, n8n, PostgreSQL o backups.
- Sin activación de Live Mode funcional.
- Sin ejecución de Repair Mode.
- Sin instalación, actualización o eliminación de paquetes.

## Saneamiento

La evidencia conserva únicamente resultados normalizados. Se excluyen direcciones internas, nombres de usuario, material criptográfico, credenciales, datos personales, identificadores de máquina y salidas brutas.

## Riesgos residuales

- La copia preventiva del fichero de claves permanece en almacenamiento local restringido del host para recuperación administrativa. Contiene material público retirado, no una clave privada.
- Las copias desactivadas de `sudoers` permanecen en cuarentena administrativa, fuera de la ruta activa y con permisos restringidos.
- La eliminación definitiva de estos respaldos debe regirse por la política de retención del centro y no forma parte de esta Work Order.

## Conclusión

La clave temporal del host y los permisos temporales de ambas VMs fueron retirados de sus ubicaciones activas. Las configuraciones resultantes son sintácticamente válidas y no se detectaron efectos sobre los servicios de la plataforma.

**Decisión final: acceso temporal retirado correctamente.**

