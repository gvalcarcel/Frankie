# Auditoría inicial - Frankie Status MVP

## Alcance

Auditoría inicial del comando:

```bash
python -m frankie status
```

El comando debe leer únicamente evidencias documentadas dentro del repositorio local y mostrar un resumen de estado.

## Comandos ejecutados

```bash
python -m frankie status
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

## Resultado de `python -m frankie status`

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

## Tests ejecutados

```text
Ran 11 tests

OK
```

## Resultado

- `status` devuelve código `0`.
- La salida contiene `Frankie Status`.
- La salida contiene `0.6.0-dev`.
- La salida contiene `read-only foundation`.
- Detecta evidencias presentes.
- Detecta warning conocido de Portainer.
- Detecta validación Windows/SMB pendiente.
- Detecta exposición PostgreSQL como OK.
- No falla si faltan evidencias en pruebas simuladas.

## Confirmación de solo lectura

El comando:

- No conecta por SSH.
- No ejecuta scripts.
- No ejecuta comandos externos.
- No instala paquetes.
- No reinicia servicios.
- No borra archivos.
- No escribe ficheros.
- No lee `.env`.
- No usa credenciales.
- No accede a servicios externos.

## Riesgos detectados

### R-001 - Parsing todavía simple

Clasificación: menor.

El MVP usa detección textual sencilla sobre evidencias conocidas.

Recomendación:

- Evolucionar hacia un parser más estructurado cuando existan evidencias normalizadas.

### R-002 - Estado basado en evidencias, no en tiempo real

Clasificación: esperada.

El comando no consulta servidores en vivo.

Recomendación:

- Mantener mensajes claros sobre el origen documental del estado.

### R-003 - `srv-recursos backups` queda `UNKNOWN`

Clasificación: menor.

No existe evidencia suficiente de backup real de recursos.

Recomendación:

- Implementar o documentar backup real de `srv-recursos` en una Work Order posterior.

## Decisión final provisional

```text
listo para auditoría externa
```
