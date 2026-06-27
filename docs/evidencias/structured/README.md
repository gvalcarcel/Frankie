# Evidencias estructuradas de Frankie

## Propósito

Este directorio contiene fichas JSON saneadas que describen el estado conocido del proyecto y sus componentes.

Las fichas permiten que Frankie Core y otras herramientas lean campos estables sin interpretar párrafos de texto libre.

## Convivencia con Markdown

Las evidencias JSON no sustituyen las evidencias Markdown históricas.

```text
Markdown = contexto, explicación y trazabilidad humana
JSON     = campos estructurados y reutilizables por programas
```

Durante esta transición, JSON es una fuente complementaria. Status y Audit conservan sus reglas basadas en documentación y continúan funcionando si este directorio no existe.

## Fichas iniciales

| Archivo | Contenido |
| --- | --- |
| `frankie_core.json` | Versión de desarrollo y release estable. |
| `samba_validation.json` | Validación SMB actual y trazabilidad histórica. |
| `portainer_warning.json` | Advertencia conocida del puerto `8000`. |
| `audit_summary.json` | Resumen actual de Audit Engine. |
| `release_v0.6.0.json` | Estado de la primera release estable. |
| `offline_live_strategy.json` | Política OFFLINE por defecto y LIVE explícito. |

## Contrato

El esquema documental se encuentra en:

`docs/schemas/frankie_evidence.schema.json`

Campos comunes obligatorios:

- `schema_version`;
- `evidence_id`;
- `evidence_type`;
- `component`;
- `status`;
- `severity`;
- `mode`;
- `data_source`;
- `summary`;
- `references`;
- `server_impact`;
- `security`;
- `recommendation`.

## Seguridad

Toda ficha versionable debe declarar:

```json
{
  "security": {
    "contains_secrets": false,
    "contains_credentials": false,
    "contains_internal_ips": false
  }
}
```

El loader rechaza fichas que declaren cualquiera de estos valores como `true`.

No se deben copiar capturas raw a este directorio. Toda evidencia debe revisarse y sanearse antes de versionarse.

## Modo operativo

Estas fichas son offline y documentales. No ejecutan comprobaciones, no conectan con Frankie y no cambian configuraciones.

El hallazgo Portainer `8000` permanece abierto. SMB permanece validado por las evidencias pre-release referenciadas.
