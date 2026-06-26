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
knowledge/SERVIDORES.md
knowledge/SERVICIOS.md
knowledge/DOCKER.md
knowledge/SAMBA.md
knowledge/BACKUPS.md
docs/arquitectura.md
```

Si alguna fuente falta, el comando no debe fallar. Debe informar `UNKNOWN` o `MISSING EVIDENCE`.

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
Version: 0.6.0-dev
Mode: read-only foundation

Physical server:
  Frankie....................... OK

Virtual machines:
  srv-servicios................. OK
  srv-recursos.................. WARNING

Core services:
  Docker........................ OK
  Portainer..................... WARNING
  PostgreSQL.................... OK
  n8n........................... OK
  Samba......................... WARNING

Security:
  UFW........................... OK
  Fail2ban...................... OK
  PostgreSQL exposure........... OK

Backups:
  srv-servicios backups......... OK
  srv-recursos backups.......... UNKNOWN

Evidence:
  srv-servicios audit........... OK
  srv-recursos audit............ OK
  Audit report.................. OK
  Windows/SMB validation........ PENDING

Overall status: WARNING
```

## Limitaciones del MVP

- No realiza parsing avanzado.
- No consulta estado en vivo.
- No valida acceso SMB real desde Windows.
- No calcula antigüedad de evidencias.
- No emite JSON ni Markdown.
- No diferencia todavía entre warning operativo y warning documental.

## Próximos pasos

- Añadir salida JSON.
- Añadir antigüedad de evidencias.
- Mejorar parsing semántico de informes.
- Integrar `inventory` con knowledge base.
- Implementar `doctor` como diagnóstico local de repositorio.
- Añadir auditoría externa del comando `status`.
