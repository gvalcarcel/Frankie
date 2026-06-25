# Validacion de scripts - srv-recursos

## 01_instalar_samba.sh

Objetivo: instalar Samba y utilidades base.

Comando dry-run:

```bash
./01_instalar_samba.sh --dry-run
```

Debe mostrar:

- `apt update`.
- Instalacion de Samba, UFW y tree si faltan.
- Activacion de `smbd`.

No debe hacer:

- Modificar `smb.conf`.
- Crear usuarios.

Validaciones posteriores:

- `systemctl status smbd --no-pager`.

Riesgo: bajo.

Decision final: apto / revisar / no ejecutar.

## 02_crear_usuarios_samba.sh

Objetivo: crear grupos y usuarios funcionales.

Comando dry-run:

```bash
./02_crear_usuarios_samba.sh --dry-run
```

Debe mostrar:

- Creacion de grupos si faltan.
- Creacion de usuarios si faltan.
- Instrucciones `smbpasswd`.

No debe hacer:

- Escribir contrasenas reales.
- Duplicar usuarios o grupos.
- Cambiar usuarios existentes sin revision.

Validaciones posteriores:

- `id alumno`.
- `id profesor`.
- `pdbedit -L`.

Riesgo: medio.

Decision final: apto / revisar / no ejecutar.

## 03_crear_estructura_recursos.sh

Objetivo: crear arbol `/srv/recursos`.

Comando dry-run:

```bash
./03_crear_estructura_recursos.sh --dry-run
```

Debe mostrar:

- Creacion de carpetas esperadas.
- Creacion de README si falta.

No debe hacer:

- Borrar contenido existente.
- Cambiar permisos.

Validaciones posteriores:

- `tree -L 2 /srv/recursos`.

Riesgo: bajo.

Decision final: apto / revisar / no ejecutar.

## 04_aplicar_permisos.sh

Objetivo: aplicar permisos de lectura/escritura.

Comando dry-run:

```bash
./04_aplicar_permisos.sh --dry-run
```

Debe mostrar:

- `chown` a `root:profesorado`.
- Permisos para ISOs, entregas y profesorado.

No debe hacer:

- Aplicar `777`.
- Borrar archivos.
- Cambiar usuarios o grupos.

Validaciones posteriores:

- `ls -ld /srv/recursos /srv/recursos/02_ISOS /srv/recursos/99_PROFESORADO`.
- Prueba de escritura controlada con `profesor`.
- Prueba de bloqueo con `alumno`.

Riesgo: alto.

Decision final: apto / revisar / no ejecutar.

## 05_configurar_smb_conf.sh

Objetivo: insertar bloque Samba gestionado por Frankie.

Comando dry-run:

```bash
./05_configurar_smb_conf.sh --dry-run
```

Debe mostrar:

- Backup de `smb.conf`.
- Insercion o sustitucion entre marcadores.
- Validacion `testparm`.

No debe hacer:

- Duplicar bloques.
- Borrar configuracion global.
- Reiniciar Samba si no hay cambios.

Validaciones posteriores:

- `testparm -s`.
- `systemctl status smbd --no-pager`.
- Acceso SMB desde cliente.

Riesgo: alto.

Decision final: apto / revisar / no ejecutar.

## 06_configurar_firewall.sh

Objetivo: configurar UFW para SSH y Samba.

Comando dry-run:

```bash
./06_configurar_firewall.sh --dry-run
```

Debe mostrar:

- Reglas `22/tcp`, `445/tcp`, `139/tcp`, `137/udp`, `138/udp`.

No debe hacer:

- Cerrar SSH.
- Abrir puertos innecesarios.

Validaciones posteriores:

- `ufw status verbose`.
- Acceso SMB desde red permitida.

Riesgo: alto.

Decision final: apto / revisar / no ejecutar.

## 07_configurar_backup_recursos.sh

Objetivo: preparar backups de recursos y Samba.

Comando dry-run:

```bash
./07_configurar_backup_recursos.sh --dry-run
```

Debe mostrar:

- Estructura de backup.
- Script de backup.
- Entrada cron sin duplicados.
- Uso de `BACKUP_ISOS=false` por defecto.

No debe hacer:

- Borrar recursos.
- Incluir ISOs si `BACKUP_ISOS=false`.
- Duplicar cron.

Validaciones posteriores:

- `crontab -l`.
- Revision del script generado.
- Prueba manual en entorno controlado.

Riesgo: medio.

Decision final: apto / revisar / no ejecutar.
