# Checklist de validacion - srv-recursos

## Identificacion

- [ ] La VM arranca correctamente.
- [ ] La IP responde desde la red del centro.
- [ ] El hostname es el esperado.

## Samba

- [ ] `01_instalar_samba.sh --dry-run` muestra acciones esperadas.
- [ ] `01_instalar_samba.sh` deja `smbd` activo.
- [ ] `smbd` esta activo.
- [ ] `testparm -s` no muestra errores.
- [ ] Los puertos SMB estan accesibles desde la red permitida.
- [ ] Las comparticiones esperadas aparecen configuradas.

## Recursos

- [ ] Existe `/srv/recursos`.
- [ ] Existe `/srv/recursos/02_ISOS`.
- [ ] Existe `/srv/recursos/99_PROFESORADO`.
- [ ] La estructura coincide con `samba/estructura-recursos.example.txt`.

## Usuarios

- [ ] `02_crear_usuarios_samba.sh --dry-run` muestra creacion esperada.
- [ ] `02_crear_usuarios_samba.sh` no duplica usuarios ni grupos.
- [ ] Las contrasenas Samba se configuran manualmente con `smbpasswd`.
- [ ] Existe usuario `alumno`.
- [ ] Existe usuario `profesor`.
- [ ] `alumno` pertenece a `alumnado`.
- [ ] `profesor` pertenece a `profesorado`.
- [ ] `pdbedit -L` muestra usuarios Samba esperados.

## Permisos

- [ ] `03_crear_estructura_recursos.sh --dry-run` muestra arbol previsto.
- [ ] `03_crear_estructura_recursos.sh` crea estructura idempotente.
- [ ] `04_aplicar_permisos.sh --dry-run` muestra permisos esperados.
- [ ] `04_aplicar_permisos.sh` aplica permisos sin errores.
- [ ] `profesor` puede escribir en `02_ISOS`.
- [ ] `alumno` no puede escribir en `02_ISOS`.
- [ ] `profesor` puede acceder a `99_PROFESORADO`.
- [ ] `alumno` no puede acceder a `99_PROFESORADO`.

## Validacion desde cliente

- [ ] Un equipo del aula ve las comparticiones.
- [ ] Desde Windows, `\\IP_DEL_SERVIDOR\recursos` abre correctamente.
- [ ] Desde Windows, `alumno` puede leer recursos.
- [ ] Desde Windows, `alumno` no puede escribir en `isos`.
- [ ] Desde Windows, `profesor` puede subir una ISO.
- [ ] Desde Windows, `alumno` no ve o no accede a `profesorado`.

## Firewall

- [ ] `05_configurar_smb_conf.sh --dry-run` muestra bloque gestionado.
- [ ] `05_configurar_smb_conf.sh` valida con `testparm`.
- [ ] `06_configurar_firewall.sh --dry-run` muestra reglas esperadas.
- [ ] `06_configurar_firewall.sh` no duplica reglas.
- [ ] UFW esta activo.
- [ ] SSH esta permitido.
- [ ] Samba esta permitido solo si procede en la red del centro.
- [ ] No hay puertos innecesarios abiertos.

## Backups

- [ ] `07_configurar_backup_recursos.sh --dry-run` muestra acciones esperadas.
- [ ] `07_configurar_backup_recursos.sh` crea script y cron sin duplicados.
- [ ] Si `BACKUP_ISOS=false`, las ISOs quedan excluidas del tar de recursos.
