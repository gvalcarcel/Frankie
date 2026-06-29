# Informes consolidados en Frankie Core

## Objetivo

El comando `report` reúne en un único documento el estado, inventario, auditoría, diagnóstico y resumen de evidencias disponibles en el repositorio.

El informe es OFFLINE. No consulta el servidor físico Frankie, no abre conexiones y no modifica servicios.

## Comandos

```bash
python -m frankie report
python -m frankie report --markdown
python -m frankie report --json
```

La salida predeterminada es Markdown. `--markdown` permite solicitarla de forma explícita. `--json` produce exclusivamente JSON válido.

## Contenido

- título, versión, modo y fecha de generación;
- resumen ejecutivo;
- estado global;
- inventario resumido;
- hallazgos de Audit Engine;
- diagnóstico de Doctor;
- resumen de evidencias;
- riesgos conocidos;
- estados de SMB y Portainer;
- limitaciones;
- próximos pasos recomendados.

Los datos se construyen desde los modelos internos. Frankie Core no analiza su propia salida de consola.

## Exportación a fichero

```bash
python -m frankie report --markdown --output docs/evidencias/frankie-core-v0.8.0/generated_report.md
python -m frankie report --json --output docs/evidencias/frankie-core-v0.8.0/generated_report.json
```

Reglas de seguridad:

- solo se permiten destinos resueltos dentro de `docs/evidencias/`;
- Markdown requiere extensión `.md` y JSON requiere `.json`;
- los directorios intermedios se crean cuando hacen falta;
- un fichero existente no se sobrescribe;
- `--force` debe indicarse junto con `--output` para reemplazarlo;
- las rutas fuera del área de evidencias se bloquean;
- sin `--output` no se escribe ningún fichero.

Ejemplo de reemplazo explícito:

```bash
python -m frankie report --json --output docs/evidencias/frankie-core-v0.8.0/generated_report.json --force
```

## Contrato JSON

La raíz incluye:

```json
{
  "schema_version": "1.0",
  "command": "report",
  "frankie_core_version": "0.8.0-dev",
  "mode": "offline",
  "generated_at": "<ISO-8601>",
  "status": {},
  "inventory": {},
  "audit": {},
  "doctor": {},
  "evidence": {}
}
```

## Limitaciones

- La fecha indica cuándo se generó el documento, no cuándo se observó el servidor.
- La frescura depende de las evidencias versionadas.
- Live Mode no está implementado.
- Repair Mode no está implementado.
- Exportar no convierte una evidencia offline en una captura real.

## Estado de evidencias LIVE

Los informes incluyen `Live evidence status` en Markdown y `live_evidence` en JSON. El bloque resume las capturas saneadas, la retirada de accesos y si existe alguna conexión nueva asociada a la generación del informe.

En el estado actual:

- existe una captura LIVE saneada y de solo lectura;
- no se hicieron cambios durante esa captura;
- el acceso temporal fue retirado mediante una intervención controlada posterior;
- no hay acceso temporal activo documentado;
- generar el informe no conecta de nuevo con Frankie.

El campo `changes_scope` evita confundir la retirada del acceso con una modificación de Docker, Samba, Proxmox u otros servicios.
