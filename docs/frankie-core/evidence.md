# Evidencias estructuradas en Frankie Core

## Objetivo

Frankie Core incorpora un modelo inicial para localizar, cargar y validar fichas JSON desde:

```text
docs/evidencias/structured/
```

El modelo reduce la dependencia futura del texto libre sin borrar ni invalidar las evidencias Markdown existentes.

## Arquitectura

```text
docs/evidencias/structured/*.json
        |
        v
frankie/evidence/loader.py
        |
        v
EvidenceLoadResult
        |
        +--> status --json
        +--> audit --json
```

Módulos:

- `frankie/evidence/models.py`: modelos inmutables de evidencia, incidencias y resultado de carga;
- `frankie/evidence/loader.py`: localización, lectura JSON y validación mínima;
- `frankie/output/json_output.py`: exposición de metadatos de disponibilidad.

## Comportamiento del loader

El loader:

- usa únicamente la biblioteca estándar;
- procesa los ficheros `.json` en orden determinista;
- valida campos comunes y estructuras anidadas mínimas;
- devuelve una lista vacía si la carpeta no existe;
- conserva las fichas válidas aunque otra sea inválida;
- devuelve incidencias controladas con ruta y mensaje;
- rechaza fichas que declaren secretos, credenciales o IPs internas;
- no escribe ficheros;
- no ejecuta comandos;
- no lee `.env`;
- no usa red.

## Integración inicial

Cuando existen fichas válidas, `status --json` y `audit --json` incluyen:

```json
{
  "data_source": "structured_and_documented_evidence",
  "structured_evidence": {
    "available": true,
    "path": "docs/evidencias/structured",
    "loaded": 6,
    "issues": 0
  }
}
```

Si la carpeta falta o no contiene fichas válidas, los comandos siguen funcionando con evidencia documentada y muestran `available: false`.

## Prioridad de fuentes

En esta primera versión, las fichas estructuradas son complementarias. No cambian por sí solas los estados calculados por Status ni los checks de Audit Engine.

Una Work Order futura podrá definir reglas explícitas de precedencia basadas en tipo, fecha y versión de esquema. Hasta entonces:

```text
Markdown mantiene la lógica histórica.
JSON aporta contrato, disponibilidad y datos reutilizables.
```

## Estado conocido

- Frankie Core: `0.8.0-dev`.
- Release estable: `v0.7.0`.
- SMB: `OK / PASS / INFO`.
- Portainer puerto `8000`: `WARNING / WARN / LOW`.
- Modo predeterminado: OFFLINE.
- Live Mode: no implementado.
- Repair Mode: no implementado.

## Limitaciones

- La validación del loader es mínima y no sustituye todavía una validación completa contra JSON Schema.
- No existen comandos para crear, editar o borrar evidencias.
- No se generan fichas automáticamente.
- No se capturan datos live.
- No hay política automática de expiración o precedencia.

## Consulta desde Frankie CLI

```bash
python -m frankie evidence list
python -m frankie evidence validate
python -m frankie evidence show samba-validation-current
python -m frankie evidence show samba-validation-current --json
```

`list` enumera las fichas cargadas, `validate` resume su validez y estados, y `show` presenta una ficha concreta. Todos son comandos offline y de solo lectura.

## Uso didáctico

La guía [Evidencias estructuradas](../aula/evidencias-estructuradas.md) propone una práctica guiada para listar, validar e interpretar fichas sin conectarse a Frankie.

Una futura captura LIVE deberá conservar la evidencia raw fuera del repositorio hasta completar su saneamiento. El diseño se describe en [Live Mode](live-mode-design.md).
