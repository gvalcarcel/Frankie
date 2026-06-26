# Pre-release Live Evidence Check

Fecha de revision: 2026-06-26

Version revisada: `0.6.0-dev`

Decision final: `apto para continuar con preparacion de release`

## 1. Alcance

Esta revision realiza una comprobacion real, controlada y de solo lectura contra las VMs principales de Frankie antes de preparar `v0.6.0`.

La revision se centra en:

- documentar la validacion SMB confirmada por el usuario desde un cliente real;
- comprobar la publicacion del puerto `8000` de Portainer;
- comprobar estado basico de Samba;
- dejar evidencia saneada en el repositorio;
- confirmar que no se han realizado cambios de configuracion ni acciones de reparacion.

Esta Work Order no prepara release, no cambia version, no crea tag y no crea release.

## 2. Entorno revisado

Entorno revisado:

- VM de servicios: `srv-servicios` / hostname observado `frankie`.
- VM de recursos: `srv-recursos` / hostname observado `srvrecursos`.

Datos saneados:

- IPs: no documentadas por seguridad.
- Credenciales: no documentadas.
- Usuarios personales: no documentados.
- Tokens o secretos: no incluidos.

## 3. Comandos de solo lectura ejecutados

En `srv-servicios`:

```bash
hostname
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
docker inspect portainer --format '{{json .NetworkSettings.Ports}}'
ss -tulpn
ufw status verbose
```

En `srv-recursos`:

```bash
hostname
systemctl is-active smbd
testparm -s
ls -ld /srv/recursos /srv/recursos/01_INSTALABLES /srv/recursos/02_ISOS /srv/recursos/04_MATERIAL_CLASE /srv/recursos/05_PLANTILLAS /srv/recursos/06_PRACTICAS /srv/recursos/99_PROFESORADO
ss -tulpn
ufw status verbose
```

Nota: los comandos se usaron unicamente para observacion. No se ejecutaron acciones de correccion ni modificacion.

## 4. Resultado Portainer / puerto 8000

Resultado:

```text
Confirmado
```

Evidencia saneada:

```text
Contenedor: portainer
Estado: activo
Puerto 8000: publicado por Docker en IPv4 e IPv6
Puerto 9443: publicado por Docker en IPv4 e IPv6
Puerto 9000: expuesto internamente por el contenedor, no publicado al host
```

Comprobacion de escucha:

```text
0.0.0.0:8000  LISTEN  docker-proxy
[::]:8000     LISTEN  docker-proxy
0.0.0.0:9443  LISTEN  docker-proxy
[::]:9443     LISTEN  docker-proxy
```

Comprobacion UFW:

```text
UFW: active
Reglas permitidas: 22/tcp, 5678/tcp, 9443/tcp
Regla 8000/tcp: no permitida explicitamente
```

Conclusion:

Portainer sigue publicando el puerto `8000` en Docker y el puerto esta escuchando en el host mediante `docker-proxy`, pero UFW no lo permite explicitamente. El hallazgo historico queda confirmado por evidencia actual.

No se ha modificado Docker Compose, Portainer ni UFW durante esta comprobacion.

## 5. Resultado Samba / SMB

Resultado:

```text
Samba service: active
testparm: OK
```

Comparticiones documentadas y presentes en la configuracion efectiva:

```text
[recursos]
[instalables]
[isos]
[material]
[plantillas]
[practicas]
[profesorado]
```

Permisos principales observados:

```text
/srv/recursos                    root:profesorado  drwxr-xr-x
/srv/recursos/01_INSTALABLES     root:profesorado  drwxr-xr-x
/srv/recursos/02_ISOS            root:profesorado  drwxrwsr-x
/srv/recursos/04_MATERIAL_CLASE  root:profesorado  drwxr-xr-x
/srv/recursos/05_PLANTILLAS      root:profesorado  drwxr-xr-x
/srv/recursos/06_PRACTICAS       root:profesorado  drwxr-xr-x
/srv/recursos/99_PROFESORADO     root:profesorado  drwxrwx---
```

Puertos Samba observados:

```text
139/tcp LISTEN
445/tcp LISTEN
```

UFW en `srv-recursos`:

```text
UFW: active
Reglas permitidas: 22/tcp, 139/tcp, 445/tcp, 137/udp, 138/udp
```

No se han cambiado permisos, no se han creado usuarios, no se ha modificado Samba y no se han reiniciado servicios.

## 6. Validacion SMB desde cliente real

Durante la revision pre-release, el usuario ha confirmado que la conexion por SMB funciona correctamente desde un cliente real del entorno disponible.

Resultado:

```text
SMB validation: OK
```

Esta validacion resuelve el pendiente historico detectado en auditorias anteriores, donde Samba aparecia como configurado pero pendiente de validacion desde cliente real.

Datos saneados:

```text
Cliente: cliente real del entorno disponible
Resultado: conexion SMB correcta
Credenciales: no documentadas por seguridad
IP: no documentada por seguridad
```

No se han realizado cambios de configuracion durante la prueba.

No se han modificado permisos.

No se han creado usuarios.

No se han reiniciado servicios Samba.

No se han almacenado credenciales, contrasenas ni datos sensibles en la evidencia.

Conclusion:

```text
Samba/SMB validation: validated
```

## 7. Evidencias saneadas

Las evidencias se han resumido para evitar incluir:

- IPs internas;
- credenciales;
- tokens;
- nombres de usuario personales;
- rutas con datos privados;
- capturas no revisadas.

Marcadores usados conceptualmente:

```text
[REDACTED_IP]
[REDACTED_SECRET]
```

No fue necesario incluir valores sensibles.

## 8. Riesgos detectados

| Riesgo | Estado | Severidad | Recomendacion |
| --- | --- | --- | --- |
| Portainer publica `8000` en Docker, aunque UFW no lo permite. | Confirmado | Menor | Decidir en WO futura si se elimina la publicacion del puerto o se documenta como necesaria. |
| SMB ya validado por cliente real, pero Frankie Core `audit` aun refleja el pendiente historico desde evidencias anteriores. | Documental | Menor | En una WO posterior, actualizar las reglas/evidencias de Audit Engine para consumir esta evidencia pre-release. |
| Evidencias reales contienen informacion de infraestructura si se guardan sin sanear. | Controlado | Menor | Mantener solo informes saneados en repositorio publico. |

## 9. Pendientes reales antes de release

Pendientes recomendados antes de preparar `v0.6.0`:

1. Decidir tratamiento del puerto `8000` de Portainer.
2. Actualizar, en una WO posterior, la evidencia consumida por Audit Engine para que `AUD-SAMBA-001` pueda pasar de `PENDING` a `PASS`.
3. Revisar si la carpeta historica `cli/` debe mantenerse o explicarse antes de release.
4. Ejecutar revision final de secretos antes del tag.
5. Preparar `WO-0006B` para registrar readiness y evidencias pre-release en GitHub.

## 10. Confirmacion de no modificacion

Durante esta Work Order:

- no se reiniciaron servicios;
- no se modificaron servicios;
- no se cambiaron permisos;
- no se cambiaron configuraciones;
- no se modifico Docker Compose;
- no se modifico UFW;
- no se modifico Samba;
- no se modifico PostgreSQL;
- no se modifico n8n;
- no se crearon usuarios;
- no se almacenaron secretos;
- no se ejecutaron acciones destructivas.

## 11. Decision final

```text
apto para continuar con preparacion de release
```

Esta decision no declara `v0.6.0` como release final. Solo confirma que se puede continuar con la preparacion controlada de la release.
