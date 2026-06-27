# Frankie Audit

## Propósito

`python -m frankie audit` ejecuta el primer motor de auditoría reutilizable de Frankie Core.

El comando lee evidencias locales del repositorio, evalúa comprobaciones documentadas y muestra hallazgos técnicos con estado, severidad, evidencias y recomendaciones.

Su objetivo no es reparar el sistema ni descubrir servicios en vivo. Su objetivo es enseñar y aplicar una auditoría basada en evidencias.

## Diferencia entre `status`, `inventory` y `audit`

`status` responde a:

```text
¿Cómo está Frankie según la información disponible?
```

`inventory` responde a:

```text
¿Qué compone Frankie según la información disponible?
```

`audit` responde a:

```text
¿Qué comprobaciones podemos validar, con qué evidencias y qué hallazgos aparecen?
```

Por tanto:

- `status` resume estado general.
- `inventory` enumera componentes conocidos.
- `audit` evalúa checks y produce hallazgos.

## Fuentes leídas

El comando usa fuentes locales de solo lectura:

- `docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt`
- `docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt`
- `docs/evidencias/paso-5-auditorias/informe_auditoria.md`
- `docs/evidencias/frankie-core-v0.6.0/pre_release_live_evidence_check.md`
- `docs/evidencias/frankie-core-v0.6.0/status_mvp_audit.md`
- `docs/evidencias/frankie-core-v0.6.0/status_mvp_architecture_review.md`
- `docs/evidencias/frankie-core-v0.6.0/inventory_mvp_audit.md`
- `docs/evidencias/frankie-core-v0.6.0/inventory_mvp_architecture_review.md`
- `docs/frankie-core/status.md`
- `docs/frankie-core/inventory.md`
- `knowledge/SERVIDORES.md`
- `knowledge/SERVICIOS.md`
- `knowledge/DOCKER.md`
- `knowledge/SAMBA.md`
- `knowledge/BACKUPS.md`
- `knowledge/RED.md`

Si alguna fuente falta, el comando no debe fallar. La comprobación afectada se marcará como `UNKNOWN` o `MISSING_EVIDENCE`.

El motor conserva la evidencia histórica y prioriza evidencias posteriores cuando resuelven un pendiente anterior. Por ejemplo, la validación SMB aparecía como pendiente en el Paso 5, pero la revisión pre-release documentó `SMB validation: OK`, por lo que el estado actual de `AUD-SAMBA-001` pasa a `PASS`.

## Qué no hace

`audit` no realiza ninguna de estas acciones:

- No modifica servidores.
- No se conecta al servidor físico Frankie.
- No usa SSH.
- No consulta Proxmox.
- No ejecuta Docker.
- No ejecuta Samba.
- No ejecuta scripts Bash.
- No ejecuta comandos externos.
- No escribe ficheros.
- No borra ficheros.
- No lee `.env`.
- No usa credenciales.
- No accede a Internet.
- No accede a GitHub API.
- No cambia configuraciones Docker, Samba ni backups.

## Estados de auditoría

- `PASS`: comprobación validada correctamente.
- `WARN`: hay una desviación o riesgo no crítico.
- `FAIL`: hay una condición bloqueante o crítica.
- `UNKNOWN`: no hay información suficiente.
- `PENDING`: la validación está pendiente.
- `MISSING_EVIDENCE`: falta una evidencia esperada.

## Severidades

- `INFO`: resultado informativo o correcto.
- `LOW`: riesgo bajo o mejora no urgente.
- `MEDIUM`: riesgo que debe revisarse antes de avanzar.
- `HIGH`: riesgo importante.
- `CRITICAL`: riesgo crítico.

En `Audit Engine v1` no todas las severidades aparecen necesariamente en la salida, pero el modelo ya está preparado.

## Checks iniciales

El MVP incluye estas comprobaciones:

- `AUD-EVIDENCE-001`: evidencias de auditoría disponibles.
- `AUD-REPORT-001`: informe apto para dry-run.
- `AUD-SERVICES-PORTAINER-001`: desviación conocida de Portainer en puerto 8000.
- `AUD-SAMBA-001`: validación SMB desde cliente real; históricamente pendiente, validada por evidencia pre-release.
- `AUD-POSTGRES-001`: PostgreSQL sin exposición externa en 5432.
- `AUD-CORE-READONLY-001`: modo solo lectura de Frankie Core.
- `AUD-CONCEPTS-001`: distinción Frankie / Frankie Core / Repositorio.

## Ejemplo de uso

Desde la raíz del repositorio:

```bash
python -m frankie audit
```

Salida orientativa:

```text
Frankie Audit
Version: 0.7.0-dev
Mode: read-only foundation

Scope:
  Source........................ repository evidence
  Live connection............... no
  Writes files.................. no
  Executes commands............. no

Summary:
  Checks total.................. 7
  PASS.......................... 6
  WARN.......................... 1
  PENDING....................... 0
  UNKNOWN....................... 0
  MISSING_EVIDENCE.............. 0
  FAIL.......................... 0

Findings:

[WARN] AUD-SERVICES-PORTAINER-001
  Known Portainer port deviation
  Severity: LOW
  Message:
    Portainer publishes port 8000 although it is documented as not allowed by UFW.
  Evidence:
    docs/evidencias/paso-5-auditorias/informe_auditoria.md
  Recommendation:
    Revisar si el puerto 8000 debe mantenerse publicado o eliminarse del compose si no es necesario.

[PASS] AUD-SAMBA-001
  SMB Windows client validation
  Severity: INFO
  Message:
    Historical SMB validation was pending, but pre-release evidence validates SMB from a real client.
  Evidence:
    docs/evidencias/paso-5-auditorias/informe_auditoria.md
    docs/evidencias/frankie-core-v0.6.0/pre_release_live_evidence_check.md

Overall audit result: WARN
```

## Modo verbose

`Audit Engine v1` implementa:

```bash
python -m frankie audit --verbose
```

Este modo muestra más contexto por hallazgo:

- categoría;
- descripción;
- evidencias;
- recomendación;
- limitación, si existe.

## Resultado global

El resultado global se calcula con prioridad prudente:

```text
FAIL > WARN > PENDING > UNKNOWN > MISSING_EVIDENCE > PASS
```

Si existe al menos un `WARN` y ningún `FAIL`, el resultado global será `WARN`.

## Limitaciones del MVP

- No es una auditoría en vivo.
- No valida el estado actual de Proxmox.
- No consulta servicios reales.
- No comprueba puertos en tiempo real.
- No valida permisos Samba desde Windows por sí mismo; interpreta la evidencia documentada por revisiones reales.
- No repara hallazgos.
- No genera ficheros de salida.
- La evaluación se basa en evidencias documentadas.

## Uso pedagógico

Este comando puede utilizarse en clase para explicar:

- qué es una auditoría técnica;
- qué diferencia hay entre observar, evaluar y reparar;
- por qué una conclusión debe basarse en evidencias;
- qué es un check;
- qué es un hallazgo;
- qué significa severidad;
- qué es una recomendación;
- por qué una auditoría segura no debe modificar el sistema auditado.

## Próximos pasos

- Evolucionar el contrato JSON junto con evidencias estructuradas versionadas.
- Definir evidencias estructuradas.
- Ampliar checks por área: Docker, Samba, backups, seguridad y documentación.
- Preparar un futuro modo live explícitamente separado y protegido.
- Integrar resultados con dashboard o módulo IA sin cambiar el modo seguro por defecto.

## Salida JSON

Desde `0.7.0-dev`, Audit Engine puede devolver datos estructurados:

```bash
python -m frankie audit --json
python -m frankie audit --verbose --json
```

Ejemplo reducido:

```json
{
  "schema_version": "1.0",
  "command": "audit",
  "frankie_core_version": "0.7.0-dev",
  "mode": "offline",
  "data_source": "structured_and_documented_evidence",
  "structured_evidence": {"available": true, "loaded": 6, "issues": 0},
  "overall_result": "WARN",
  "counts": {"total": 7, "pass": 6, "warn": 1},
  "checks": [
    {"id": "AUD-SAMBA-001", "status": "PASS", "severity": "INFO"},
    {"id": "AUD-SERVICES-PORTAINER-001", "status": "WARN", "severity": "LOW"}
  ]
}
```

`--verbose --json` conserva JSON puro y añade `category`, `description` y `limitation` a cada check. No mezcla encabezados ni mensajes de consola con el documento JSON.

Ambas variantes serializan el mismo `AuditReport` que la salida humana. No ejecutan comandos live, no usan credenciales y no escriben ficheros.

Las fichas estructuradas son complementarias. Audit Engine conserva sus checks Markdown actuales y no depende exclusivamente de JSON.
## Referencia relacionada

Consulta la [referencia completa de Frankie CLI](cli.md) para opciones, formatos y códigos de salida.
