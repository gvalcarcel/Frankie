# SMB Evidence Sync Architecture Review

Fecha: 2026-06-26

Version revisada: `0.6.0-dev`

Decision final: `apto para cierre de WO-0006C`

## 1. Alcance

Esta auditoria arquitectonica revisa la sincronizacion de Frankie Core con la evidencia pre-release de validacion SMB.

El objetivo es confirmar que Frankie Core interpreta correctamente la evidencia mas reciente sin borrar la trazabilidad historica y sin ocultar el hallazgo vigente de Portainer puerto `8000`.

La revision se ha limitado al repositorio local. No se han tocado servidores, no se ha usado SSH, no se ha ejecutado Docker, no se ha ejecutado Samba, no se han ejecutado scripts de produccion, no se ha cambiado version, no se ha creado tag y no se ha creado release.

## 2. Resumen ejecutivo

La implementacion de WO-0006C es arquitectonicamente correcta para el alcance de `0.6.0-dev`.

Frankie Core diferencia entre:

- evidencia historica, donde SMB estaba pendiente de validacion desde cliente real;
- evidencia pre-release posterior, donde SMB queda validado.

El estado actual documentado pasa a ser:

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO
```

El hallazgo de Portainer no queda rebajado ni ocultado:

```text
AUD-SERVICES-PORTAINER-001: WARN
Overall status: WARNING
Overall audit result: WARN
```

## 3. Evidencia historica revisada

Fuente:

```text
docs/evidencias/paso-5-auditorias/informe_auditoria.md
```

Estado historico documentado:

```text
Validacion de acceso SMB desde cliente real no aparece en auditoria.
```

Interpretacion:

- La evidencia historica sigue siendo valida como fotografia del momento de Paso 5.
- No debe reescribirse ni eliminarse.
- Debe conservarse como trazabilidad del pendiente original.

## 4. Evidencia pre-release revisada

Fuente:

```text
docs/evidencias/frankie-core-v0.6.0/pre_release_live_evidence_check.md
```

Evidencia clave:

```text
SMB validation: OK
Samba/SMB validation: validated
```

La evidencia tambien documenta que no se realizaron cambios de configuracion durante la validacion:

- no se modifico Samba;
- no se cambiaron permisos;
- no se crearon usuarios;
- no se reiniciaron servicios Samba;
- no se almacenaron credenciales.

## 5. Validacion de prioridad de evidencias

La prioridad temporal queda implementada de forma explicita:

- `frankie/core/paths.py` incorpora `pre_release_live_evidence_check.md` como fuente conocida.
- `frankie/core/status.py` lee la evidencia pre-release junto a la evidencia historica.
- `frankie/audit/checks.py` evalua `AUD-SAMBA-001` con la evidencia historica y la posterior.
- Si la evidencia pre-release contiene validacion SMB, el pendiente historico se considera resuelto.

La evidencia historica no se ignora completamente: sigue citada en `AUD-SAMBA-001` junto con la evidencia pre-release.

## 6. Validacion de `status`

Comando ejecutado:

```bash
python -m frankie status
```

Resultado relevante:

```text
Samba......................... OK
Windows/SMB validation........ OK
Overall status: WARNING
```

Conclusion:

- `status` ya no mantiene Samba en `WARNING` solo por el pendiente historico.
- `srv-recursos` aparece como `OK`.
- El estado global sigue en `WARNING` por Portainer.

## 7. Validacion de `audit`

Comando ejecutado:

```bash
python -m frankie audit
```

Resultado relevante:

```text
Checks total.................. 7
PASS.......................... 6
WARN.......................... 1
PENDING....................... 0

[PASS] AUD-SAMBA-001
Severity: INFO
```

`AUD-SAMBA-001` cita:

```text
docs/evidencias/paso-5-auditorias/informe_auditoria.md
docs/evidencias/frankie-core-v0.6.0/pre_release_live_evidence_check.md
```

Conclusion:

- SMB queda en `PASS`.
- La severidad `INFO` es adecuada para una validacion resuelta.
- Se conserva trazabilidad del pendiente historico.
- Portainer sigue como unico `WARN`.

## 8. Validacion de `audit --verbose`

Comando ejecutado:

```bash
python -m frankie audit --verbose
```

Resultado relevante:

```text
Historical SMB validation was pending, but pre-release evidence validates SMB from a real client.
Keep the historical pending evidence for traceability and use the pre-release validation as the current documented state.
```

Conclusion:

- El modo verbose explica la resolucion del pendiente historico.
- Cita la evidencia pre-release.
- Mantiene la recomendacion de conservar trazabilidad.
- No afirma que Frankie Core haya modificado Samba.

## 9. Validacion de `doctor`

Comando ejecutado:

```bash
python -m frankie doctor
```

Resultado relevante:

```text
Issues reviewed............... 1
[WARN] AUD-SERVICES-PORTAINER-001
Overall doctor result: ACTIONS_RECOMMENDED
```

Conclusion:

- Doctor no presenta SMB como accion pendiente.
- Doctor sigue explicando el hallazgo activo de Portainer.
- El comportamiento es coherente: Doctor consume hallazgos no satisfactorios del Audit Engine.

## 10. Validacion de `doctor --verbose`

Comando ejecutado:

```bash
python -m frankie doctor --verbose
```

Resultado relevante:

```text
[WARN] AUD-SERVICES-PORTAINER-001
Why no automatic repair:
  Frankie Doctor MVP is diagnostic only and does not modify systems.
```

Conclusion:

- SMB no aparece como pendiente activo.
- Portainer sigue documentado como accion recomendada.
- Doctor mantiene su naturaleza diagnostica y de solo lectura.

## 11. Confirmacion de nuevo estado SMB

Estado actual documentado:

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS
Severity: INFO
```

El pendiente historico queda resuelto por evidencia posterior. La historia se conserva, pero el estado actual documentado es validado.

## 12. Confirmacion de estado Portainer

Estado actual:

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN
Overall status: WARNING
Overall audit result: WARN
Overall doctor result: ACTIONS_RECOMMENDED
```

Conclusion:

La sincronizacion SMB no ha ocultado ni rebajado el hallazgo de Portainer puerto `8000`.

## 13. Validacion de separacion arquitectonica

La separacion de responsabilidades se mantiene:

- `frankie/core/status.py` calcula el estado resumido.
- `frankie/audit/checks.py` contiene la logica de evaluacion de checks.
- `frankie/audit/rules.py` mantiene la definicion declarativa de checks.
- `frankie/doctor/advice.py` filtra hallazgos no satisfactorios y no duplica la logica de SMB.
- Los comandos siguen siendo capas finas sobre los modulos de core.

No se ha detectado logica pesada nueva en `frankie/commands/`.

## 14. Validacion de seguridad y solo lectura

Se realizo busqueda estatica de terminos sensibles o peligrosos:

```text
subprocess
os.system
popen
write_text
unlink
remove
rmdir
shutil.rmtree
ssh
docker
systemctl
requests
urllib
socket
.env
password
secret
token
client_secret
private key
restart
repair
```

Resultado:

- No se detectaron escrituras ni subprocess en el flujo runtime afectado.
- Las coincidencias aparecen en tests, documentacion, placeholders futuros o mensajes explicitos de "no hacer".
- No se detecto acceso a red, SSH, Docker, Samba, `.env`, credenciales ni secretos en el flujo afectado.

La implementacion revisada sigue siendo de solo lectura.

## 15. Tests ejecutados

Comandos ejecutados:

```bash
python -m frankie status
python -m frankie inventory
python -m frankie audit
python -m frankie audit --verbose
python -m frankie doctor
python -m frankie doctor --verbose
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

Resultado:

```text
37 tests OK
compileall OK
```

## 16. Documentacion revisada

Documentos revisados:

- `docs/frankie-core/status.md`
- `docs/frankie-core/audit.md`
- `docs/frankie-core/doctor.md`
- `docs/frankie-core/README.md`
- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/evidencias/frankie-core-v0.6.0/smb_evidence_sync_audit.md`

Conclusion:

- La documentacion explica el cambio de SMB de pendiente historico a validado actual.
- Se mantiene que Portainer puerto `8000` sigue como advertencia.
- `v0.6.0` sigue sin declararse release cerrada.
- No se han detectado correcciones documentales imprescindibles durante esta auditoria.

## 17. Riesgos detectados

| Riesgo | Estado | Severidad | Recomendacion |
| --- | --- | --- | --- |
| Portainer puerto `8000` sigue publicado por Docker. | Vigente | Baja | Resolver o aceptar formalmente en una WO futura antes de release final. |
| La interpretacion de evidencias se basa en texto documental. | Aceptado para foundation | Media futura | Valorar evidencias estructuradas en una version posterior. |
| La evidencia historica sigue mencionando SMB pendiente. | Controlado | Baja | Mantenerla como trazabilidad y priorizar evidencias posteriores. |

## 18. Correcciones realizadas

No se realizaron correcciones de codigo ni cambios funcionales durante esta auditoria.

Se creo este informe de auditoria arquitectonica como evidencia nueva.

## 19. Recomendaciones futuras

1. Registrar WO-0006C y WO-0006C-A en GitHub mediante una Work Order especifica.
2. Mantener Portainer puerto `8000` como hallazgo visible hasta que exista decision tecnica.
3. Valorar un formato estructurado de evidencias en futuras versiones para reducir dependencia de texto libre.
4. Preparar WO-0007 solo despues de registrar esta sincronizacion.

## 20. Decision final

```text
apto para cierre de WO-0006C
```

La Work Order `WO-0006C - Sincronizar Frankie Core con evidencia SMB validada` puede cerrarse desde el punto de vista arquitectonico.

La siguiente Work Order recomendada es:

```text
WO-0006D - Registrar sincronizacion SMB en GitHub
```
