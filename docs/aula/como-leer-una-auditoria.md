# Cómo leer una auditoría

## Qué hace Audit

Audit aplica comprobaciones a la evidencia disponible.

```bash
python -m frankie audit
```

Cada comprobación tiene un identificador. Por ejemplo: `AUD-SAMBA-001`.

## Partes de un hallazgo

- **Estado:** resultado de la comprobación.
- **Severidad:** importancia técnica.
- **Mensaje:** explicación breve.
- **Evidencia:** documentos que justifican el resultado.
- **Recomendación:** siguiente paso sugerido cuando hace falta.

## Estados de Audit

### PASS

La comprobación cumple el criterio con la evidencia disponible.

### WARN

Existe una desviación que debe estudiarse.

### FAIL

La comprobación no cumple un criterio importante.

### UNKNOWN o MISSING_EVIDENCE

No hay datos suficientes o falta una evidencia necesaria.

## Estado y severidad no son lo mismo

`WARN` es el resultado de un check. `LOW` es su severidad.

Un check puede ser `WARN / LOW`: hay algo que revisar, pero el riesgo conocido es bajo.

## Ejemplo actual

- `AUD-SAMBA-001`: `PASS / INFO`.
- `AUD-SERVICES-PORTAINER-001`: `WARN / LOW`.

Audit no abre puertos, no cambia Samba y no se conecta a Frankie. Trabaja con información local.

Prácticas relacionadas: actividades 4 y 7 de [Actividades Frankie Core](actividades-frankie-core.md).
