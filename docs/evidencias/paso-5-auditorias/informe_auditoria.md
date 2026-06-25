# Informe de auditoría - Paso 5

## Fecha de auditoría

2026-06-25 13:17:15 +02:00

## Evidencias analizadas

- `docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt`
- `docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt`

Las auditorías fueron ejecutadas con privilegios suficientes para evitar falsos negativos en Docker, UFW, Fail2ban, Samba y permisos restringidos.

## Fuentes comparadas

- `checklists/validacion_srv-servicios.md`
- `checklists/validacion_srv-recursos.md`
- `checklists/validacion_scripts_srv-servicios.md`
- `checklists/validacion_scripts_srv-recursos.md`
- `docs/automatizacion.md`
- `docs/validacion_scripts.md`
- `docs/arquitectura.md`
- `docs/seguridad.md`
- `docs/procedimientos.md`
- `docs/incidencias.md`

## Resumen ejecutivo

Las dos VMs principales están operativas y alineadas en lo esencial con la documentación del proyecto.

`srv-servicios` confirma:

- Ubuntu Server 26.04 LTS.
- `qemu-guest-agent` activo.
- Docker activo.
- Contenedores `n8n`, `postgres` y `portainer` activos.
- Red Docker `aula-network` existente.
- PostgreSQL no expone `5432` al host.
- UFW activo con `22/tcp`, `5678/tcp` y `9443/tcp`.
- Fail2ban activo para `sshd`.
- Backups existentes y cron diario a las `02:00`.

`srv-recursos` confirma:

- Ubuntu Server 26.04 LTS.
- `qemu-guest-agent` activo.
- Samba activo.
- `/srv/recursos` existe.
- Usuarios `alumno` y `profesor` existen.
- Grupos `alumnado` y `profesorado` existen.
- Usuarios Samba `alumno` y `profesor` registrados.
- Carpeta `02_ISOS` con escritura de grupo y setgid.
- Carpeta `99_PROFESORADO` restringida.
- `testparm` valida la configuración Samba.
- UFW activo con SSH y puertos Samba.

Decision final:

```text
apto para dry-run
```

Condicion:

- Ejecutar primero solo `--dry-run`, script por script, con snapshot vigente y sin aplicar cambios reales en bloque.

## Estado de srv-servicios

| Area | Evidencia | Estado |
|---|---|---|
| Sistema operativo | Ubuntu 26.04 LTS, hostname `frankie` | OK |
| qemu-guest-agent | `active (running)` | OK |
| Docker | Docker `29.6.0`, servicio activo | OK |
| Contenedores | `n8n`, `postgres`, `portainer` activos | OK |
| Red Docker | `aula-network` existe | OK |
| Portainer | Contenedor activo, puertos `8000` y `9443` publicados | OK con observación |
| PostgreSQL | Contenedor activo, `5432/tcp` interno | OK |
| PostgreSQL no expuesto | `5432 no escucha en el host` | OK |
| n8n | Contenedor activo, `5678` publicado | OK |
| Puertos abiertos | `22`, `5678`, `9443`, también `8000` | OK con observación |
| UFW | Activo, permite `22`, `5678`, `9443` | OK |
| Fail2ban | Jail `sshd` activo, 0 baneados | OK |
| Backups | Directorio y ficheros recientes presentes | OK |
| Cron backup | `0 2 * * * /srv/docker/scripts/backup.sh` | OK |

## Estado de srv-recursos

| Area | Evidencia | Estado |
|---|---|---|
| Sistema operativo | Ubuntu 26.04 LTS, hostname `srvrecursos` | OK |
| qemu-guest-agent | `active (running)` | OK |
| Samba | `smbd` activo | OK |
| Recursos | `/srv/recursos` existe | OK |
| Arbol recursos | 10 directorios, 2 ISOs en `02_ISOS` | OK |
| Grupos | `alumnado`, `profesorado` existen | OK |
| Usuarios Linux | `alumno`, `profesor` existen | OK |
| Usuarios Samba | `alumno:1001`, `profesor:1002` | OK |
| Permisos `/srv/recursos` | `drwxr-xr-x root:profesorado` | OK |
| Permisos `02_ISOS` | `drwxrwsr-x root:profesorado` | OK |
| Permisos `99_PROFESORADO` | `drwxrwx--- root:profesorado` | OK |
| Samba config | `testparm` carga correctamente | OK |
| Puertos Samba | `139/tcp`, `445/tcp` escuchando | OK |
| UFW | Activo, permite SSH y Samba | OK |

## Tabla de validaciones

| Validacion | Esperado | Evidencia real | Resultado |
|---|---|---|---|
| srv-servicios Ubuntu | 26.04 LTS | Ubuntu 26.04 LTS | OK |
| srv-servicios Docker | Activo | Docker 29.6.0 activo | OK |
| srv-servicios aula-network | Existe | `OK: aula-network existe` | OK |
| srv-servicios Portainer | Activo, 9443 | `portainer` activo, `9443` publicado | OK |
| srv-servicios PostgreSQL | Activo, sin 5432 host | `postgres` activo, `5432 no escucha en el host` | OK |
| srv-servicios n8n | Activo, 5678 | `n8n` activo, `5678` publicado | OK |
| srv-servicios UFW | 22/5678/9443 | Reglas presentes | OK |
| srv-servicios Fail2ban | sshd activo | Jail `sshd` activo | OK |
| srv-servicios backups | Cron y ficheros | Cron 02:00 y backups presentes | OK |
| srv-recursos Ubuntu | 26.04 LTS | Ubuntu 26.04 LTS | OK |
| srv-recursos Samba | smbd activo | `active (running)` | OK |
| srv-recursos usuarios | alumno/profesor | Ambos existen | OK |
| srv-recursos grupos | alumnado/profesorado | Ambos existen | OK |
| srv-recursos usuarios Samba | alumno/profesor | Ambos registrados | OK |
| srv-recursos recursos | arbol completo | Arbol presente | OK |
| srv-recursos ISOs | profesor escritura | `drwxrwsr-x root:profesorado` | OK |
| srv-recursos profesorado | restringido | `drwxrwx--- root:profesorado` | OK |
| srv-recursos UFW | SSH/Samba | Reglas presentes | OK |

## Desviaciones detectadas

### D-001 - Portainer pública el puerto 8000 aunque UFW no lo permite

Clasificacion: menor.

Evidencia:

- `docker ps` muestra Portainer con `0.0.0.0:8000->8000/tcp`.
- UFW no permite `8000/tcp`; solo permite `22/tcp`, `5678/tcp`, `9443/tcp`.

Interpretacion:

- La exposición Docker existe, pero el firewall bloquea acceso externo salvo reglas adicionales.
- La documentación ya indicaba que `8000` no era prioritario.

Accion recomendada:

- Mantener documentado.
- En una fase futura, valorar eliminar la publicación `8000` del despliegue de Portainer si no se usa Edge/Agent.

### D-002 - Backups PostgreSQL reales siguen en `.sql`, plantilla propone `.sql.gz`

Clasificacion: mejora futura.

Evidencia:

- Auditoria muestra backups como `postgres_YYYYMMDD_HHMMSS.sql`.
- La plantilla `backup-servicios.sh.example` del Paso 2 propone mejora con `gzip`.

Interpretacion:

- No es fallo operativo; los backups existen.
- Hay divergencia entre script real actual y plantilla mejorada.

Accion recomendada:

- No cambiar ahora.
- En Paso posterior, aplicar la mejora de compresión solo tras prueba de restauración.

### D-003 - Validacion de acceso SMB desde cliente real no aparece en auditoría

Clasificacion: importante.

Evidencia:

- Auditoria valida Samba, usuarios, permisos y puertos.
- No incluye prueba desde Windows o cliente SMB real.

Interpretacion:

- El estado del servidor es correcto, pero falta validar experiencia real de usuario `alumno` y `profesor` desde un equipo del aula.

Accion recomendada:

- Ejecutar checklist manual desde Windows:
  - `alumno` puede leer.
  - `alumno` no escribe en `isos`.
  - `profesor` escribe en `isos`.
  - `alumno` no accede a `profesorado`.

### D-004 - Los scripts de auditoría requieren sudo para evitar falsos negativos

Clasificacion: menor.

Evidencia:

- La primera ejecución sin sudo produjo falsos avisos por permisos en Docker/UFW/Fail2ban y carpetas restringidas.
- La ejecución con sudo produjo evidencias completas.

Interpretacion:

- Los scripts son de solo lectura, pero deben ejecutarse con `sudo` para auditar servicios protegidos.

Accion recomendada:

- Actualizar documentación de auditoría para recomendar:

```bash
sudo ./scripts/auditoria/auditar_srv-servicios.sh
sudo ./scripts/auditoria/auditar_srv-recursos.sh
```

## Coincidencias principales con la documentación

- La arquitectura de dos VMs queda confirmada funcionalmente.
- `srv-servicios` aloja Docker, Portainer, PostgreSQL y n8n.
- `srv-recursos` aloja Samba y recursos docentes.
- PostgreSQL no expone `5432`.
- n8n expone `5678`.
- Portainer expone `9443`.
- UFW y Fail2ban están activos en `srv-servicios`.
- UFW y Samba están activos en `srv-recursos`.
- El modelo `alumno`/`profesor` y `alumnado`/`profesorado` existe.
- La carpeta `02_ISOS` queda preparada para escritura de profesorado.

## Acciones recomendadas

1. Autorizar revisión de `--dry-run` de scripts, empezando por los de menor riesgo.
2. Ejecutar dry-run en este orden:
   - Auditoria.
   - Dependencias.
   - Red Docker / estructura recursos.
   - Backups.
   - Seguridad.
   - Despliegues Docker.
   - Samba.
3. Actualizar documentación para indicar que auditorías completas requieren `sudo`.
4. Validar Samba desde un cliente Windows real.
5. Decidir si Portainer debe seguir publicando `8000`.
6. No aplicar cambios reales hasta tener snapshot vigente.

## Propuestas de correccion en repositorio

### Documentación

- Actualizar `docs/validacion_scripts.md` y `scripts/README.md` para recomendar auditorías con `sudo`.
- Registrar esta auditoría como evidencia base de Paso 5.

### Scripts

- Mantener scripts de auditoría como solo lectura.
- Opcional: añadir aviso al inicio si no se ejecutan como root, indicando que algunas comprobaciones pueden ser parciales.

### Checklists

- Añadir punto explicito: auditoría ejecutada con `sudo`.
- Añadir punto manual para validación SMB desde cliente real.

## Decision final

```text
apto para dry-run
```

Condiciones:

- Solo dry-run, no ejecución real todavía.
- Ejecutar de uno en uno.
- Mantener snapshots disponibles.
- Revisar salida de cada dry-run antes de pasar al siguiente.
- No pasar a ejecución real hasta cerrar la validación SMB desde cliente o aceptar formalmente ese riesgo.
