# Frankie Status MVP

## Propósito

`python -m frankie status` muestra una visión resumida del estado conocido de Frankie usando únicamente información ya documentada dentro del repositorio.

El objetivo del MVP es ofrecer una primera lectura útil del estado del servidor físico, las VMs, servicios principales, seguridad, backups y evidencias, sin consultar sistemas reales en vivo.

## Fuentes leídas

El comando usa fuentes locales de solo lectura:

```text
docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt
docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt
docs/evidencias/paso-5-auditorias/informe_auditoria.md
docs/evidencias/paso-7-mantenimiento/informe_mantenimiento_2026-06-26.md
docs/evidencias/frankie-core-v0.6.0/pre_release_live_evidence_check.md
knowledge/SERVIDORES.md
knowledge/SERVICIOS.md
knowledge/DOCKER.md
knowledge/SAMBA.md
knowledge/BACKUPS.md
docs/arquitectura.md
```

Si alguna fuente falta, el comando no debe fallar. Debe informar `UNKNOWN` o `MISSING EVIDENCE`.

Si una evidencia historica documenta una validacion pendiente y una evidencia posterior la valida correctamente, Frankie Core conserva el historial pero usa la evidencia mas reciente como estado actual documentado.

## Qué no hace

`frankie status` no:

- conecta por SSH;
- consulta Proxmox;
- consulta Docker real;
- ejecuta `systemctl`;
- ejecuta scripts Bash;
- instala paquetes;
- reinicia servicios;
- modifica ficheros;
- lee `.env`;
- usa credenciales;
- accede a Internet;
- accede a GitHub API.

## Estados

| Estado | Significado |
|---|---|
| `OK` | Existe evidencia suficiente y positiva |
| `WARNING` | Existe evidencia, pero hay desviación no crítica |
| `ERROR` | Existe evidencia de problema grave |
| `UNKNOWN` | No hay información suficiente |
| `PENDING` | Tarea documentada como pendiente |
| `MISSING EVIDENCE` | Falta una evidencia esperada |

## Ejemplo de salida

```text
Frankie Status
Version: 0.8.0-dev
Mode: read-only foundation

Physical server:
  Frankie....................... OK

Virtual machines:
  srv-servicios................. OK
  srv-recursos.................. OK

Core services:
  Docker........................ OK
  Portainer..................... WARNING
  PostgreSQL.................... OK
  n8n........................... OK
  Samba......................... OK

Security:
  UFW........................... OK
  Fail2ban...................... OK
  PostgreSQL exposure........... OK

Backups:
  srv-servicios backups......... OK
  srv-recursos backups.......... OK

Evidence:
  srv-servicios audit........... OK
  srv-recursos audit............ OK
  Audit report.................. OK
  Windows/SMB validation........ OK

Overall status: WARNING
```

## Limitaciones del MVP

- No realiza parsing avanzado.
- No consulta estado en vivo.
- No valida acceso SMB real desde Windows por si mismo; solo interpreta evidencias documentadas.
- No calcula antigüedad de evidencias.
- No emite Markdown; JSON está disponible mediante `--json`.
- No diferencia todavía entre warning operativo y warning documental.

## Próximos pasos

- Evolucionar el contrato JSON junto con evidencias estructuradas versionadas.
- Añadir antigüedad de evidencias.
- Mejorar parsing semántico de informes.
- Integrar `inventory` con knowledge base.
- Implementar `doctor` como diagnóstico local de repositorio.
- Añadir auditoría externa del comando `status`.

## Salida JSON

Desde `v0.7.0`, `status` puede devolver datos estructurados:

```bash
python -m frankie status --json
```

Ejemplo reducido:

```json
{
  "schema_version": "1.0",
  "command": "status",
  "frankie_core_version": "0.8.0-dev",
  "mode": "offline",
  "data_source": "structured_and_documented_evidence",
  "structured_evidence": {"available": true, "loaded": 6, "issues": 0},
  "overall_status": "WARNING",
  "components": [
    {"id": "samba", "status": "OK", "severity": "INFO"},
    {"id": "portainer", "status": "WARNING", "severity": "LOW"}
  ]
}
```

La salida JSON se construye desde el mismo `StatusReport` que la consola. No consulta Frankie físico, no ejecuta comandos externos y no escribe ficheros.

Las fichas estructuradas son complementarias. Si no están disponibles, Status mantiene el cálculo documental existente y marca `structured_evidence.available` como `false`.
## Referencia relacionada

Consulta la [referencia completa de Frankie CLI](cli.md) para opciones, formatos y códigos de salida.
