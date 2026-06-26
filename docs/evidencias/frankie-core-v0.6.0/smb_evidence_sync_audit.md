# SMB Evidence Sync Audit

Fecha: 2026-06-26

Version revisada: `0.6.0-dev`

Decision final: `listo para auditoria arquitectonica`

## 1. Alcance

Esta auditoria documenta la sincronizacion de Frankie Core con la evidencia pre-release que valida correctamente SMB desde un cliente real.

La revision se limita al repositorio local. No se han tocado servidores, no se ha usado SSH, no se ha ejecutado Docker, no se ha ejecutado Samba, no se han modificado evidencias historicas y no se ha cambiado la version.

## 2. Evidencia historica revisada

Fuente historica principal:

```text
docs/evidencias/paso-5-auditorias/informe_auditoria.md
```

Estado historico:

```text
Validacion SMB desde cliente Windows/SMB real pendiente
```

Interpretacion:

- La evidencia historica se conserva.
- No se elimina ni se reescribe el resultado anterior.
- Se mantiene como trazabilidad del estado en el momento de aquella auditoria.

## 3. Evidencia pre-release revisada

Fuente posterior:

```text
docs/evidencias/frankie-core-v0.6.0/pre_release_live_evidence_check.md
```

Evidencia clave:

```text
SMB validation: OK
Samba/SMB validation: validated
```

Interpretacion:

- La validacion SMB fue confirmada desde cliente real.
- No se modifico Samba durante la validacion.
- No se cambiaron permisos.
- No se crearon usuarios.
- No se almacenaron credenciales.

## 4. Cambios realizados

Se actualizaron los modulos de interpretacion de evidencias para priorizar la evidencia posterior cuando resuelve un pendiente historico:

- `frankie/core/paths.py`: anade la evidencia pre-release a las fuentes conocidas.
- `frankie/audit/checks.py`: `AUD-SAMBA-001` pasa a `PASS` si existe evidencia pre-release valida.
- `frankie/core/status.py`: `Samba` y `Windows/SMB validation` pasan a `OK` si existe evidencia pre-release valida.
- Tests de `audit`, `status` y `doctor`: cubren la resolucion del pendiente historico.

Tambien se actualizo documentacion de Frankie Core para explicar la diferencia entre evidencia historica y evidencia actual.

## 5. Validacion de `status`

Comando:

```bash
python -m frankie status
```

Resultado relevante:

```text
Samba......................... OK
Windows/SMB validation........ OK
Overall status: WARNING
```

Interpretacion:

- SMB deja de aparecer como pendiente real.
- El estado global sigue en `WARNING` por Portainer puerto `8000`.

## 6. Validacion de `audit`

Comando:

```bash
python -m frankie audit
```

Resultado relevante:

```text
PASS.......................... 6
WARN.......................... 1
PENDING....................... 0

[PASS] AUD-SAMBA-001
Historical SMB validation was pending, but pre-release evidence validates SMB from a real client.

Overall audit result: WARN
```

Interpretacion:

- `AUD-SAMBA-001` queda validado.
- Portainer sigue siendo el unico `WARN`.
- El resultado global sigue siendo `WARN`.

## 7. Validacion de `doctor`

Comando:

```bash
python -m frankie doctor
```

Resultado relevante:

```text
Issues reviewed............... 1
[WARN] AUD-SERVICES-PORTAINER-001
Overall doctor result: ACTIONS_RECOMMENDED
```

Interpretacion:

- Doctor ya no presenta SMB como accion pendiente.
- Doctor sigue centrado en hallazgos no satisfactorios.
- Portainer puerto `8000` sigue como hallazgo principal.

## 8. Confirmacion de SMB validado

Estado actual documentado:

```text
SMB validation: OK
Samba/SMB validation: validated
AUD-SAMBA-001: PASS
```

Conclusion:

El pendiente historico queda resuelto por evidencia posterior. La historia se conserva, pero el estado actual documentado es OK.

## 9. Confirmacion de Portainer como WARN

Portainer no se ha corregido ni modificado.

Estado actual:

```text
AUD-SERVICES-PORTAINER-001: WARN
Overall audit result: WARN
Overall doctor result: ACTIONS_RECOMMENDED
```

## 10. Tests ejecutados

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

## 11. Riesgos

| Riesgo | Estado | Recomendacion |
| --- | --- | --- |
| Portainer puerto `8000` sigue como desviacion conocida. | Vigente | Decidir en una WO posterior si se elimina o se documenta como necesario. |
| La evidencia historica sigue mencionando SMB pendiente. | Aceptado | No reescribir; interpretar con prioridad temporal. |
| La logica de evidencias sigue basada en texto documental. | Aceptado para foundation | Valorar evidencias estructuradas en versiones futuras. |

## 12. Confirmacion de solo lectura

Durante esta Work Order:

- no se tocaron servidores;
- no se uso SSH;
- no se ejecuto Docker;
- no se ejecuto Samba;
- no se ejecutaron scripts Bash;
- no se modificaron evidencias historicas;
- no se borraron archivos;
- no se crearon tags;
- no se creo release;
- no se cambio version.

## 13. Decision final

```text
listo para auditoria arquitectonica
```
