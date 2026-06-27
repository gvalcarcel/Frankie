# Auditoría del modelo inicial de evidencias estructuradas

Fecha: 2026-06-27

Tipo de Work Order: `OFFLINE`

Decisión final: `listo para revisión`

## 1. Alcance

WO-0010 introduce un contrato JSON, seis fichas saneadas y un loader de solo lectura para evidencias estructuradas.

La integración es complementaria: Status y Audit Engine conservan las reglas y evidencias Markdown actuales. La ausencia de la carpeta estructurada no impide su funcionamiento.

## 2. Archivos creados

- `docs/evidencias/structured/README.md`
- `docs/evidencias/structured/frankie_core.json`
- `docs/evidencias/structured/samba_validation.json`
- `docs/evidencias/structured/portainer_warning.json`
- `docs/evidencias/structured/audit_summary.json`
- `docs/evidencias/structured/release_v0.6.0.json`
- `docs/evidencias/structured/offline_live_strategy.json`
- `docs/schemas/frankie_evidence.schema.json`
- `docs/frankie-core/evidence.md`
- `frankie/evidence/__init__.py`
- `frankie/evidence/models.py`
- `frankie/evidence/loader.py`
- `tests/test_structured_evidence.py`
- `docs/evidencias/frankie-core-v0.7.0/structured_evidence_model_audit.md`

## 3. Archivos modificados

- `CHANGELOG.md`
- `ROADMAP.md`
- `docs/aula/json-en-frankie-core.md`
- `docs/frankie-core/README.md`
- `docs/frankie-core/status.md`
- `docs/frankie-core/audit.md`
- `frankie/commands/status.py`
- `frankie/commands/audit.py`
- `frankie/output/json_output.py`
- `tests/test_json_output.py`

## 4. Diseño del modelo

Cada ficha contiene:

- versión de esquema e identificador;
- tipo de evidencia;
- componente;
- estado y severidad;
- modo y fuente;
- resumen y detalles;
- referencias;
- impacto sobre servidores;
- declaración de seguridad;
- recomendación.

El contrato documental se encuentra en `docs/schemas/frankie_evidence.schema.json` y usa JSON Schema Draft 2020-12.

El loader aplica además una validación mínima con biblioteca estándar para mantener cero dependencias externas.

## 5. Evidencias creadas

| Evidencia | Estado |
| --- | --- |
| Frankie Core | `0.7.0-dev`, `OK / INFO`. |
| Samba / SMB | `OK / INFO`; conserva el pendiente histórico en detalles. |
| Portainer 8000 | `WARNING / LOW`; no resuelto y pendiente de WO LIVE. |
| Audit summary | `WARN / LOW`; 6 PASS y 1 WARN. |
| Release estable | `v0.6.0`, `RELEASED / INFO`. |
| Estrategia operativa | OFFLINE por defecto; LIVE explícito, `ACTIVE / INFO`. |

## 6. Integración con Frankie Core

El paquete nuevo `frankie/evidence/` separa modelos y carga.

`status --json` y `audit --json` exponen únicamente metadatos de disponibilidad:

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

No se añadió un comando `evidence` y no se reescribieron Status ni Audit Engine.

## 7. Validación del loader

Resultado sobre el repositorio:

```text
directory_available: true
available: true
loaded: 6
issues: 0
```

Los tests también validan:

- carpeta ausente;
- archivo JSON inválido;
- campo obligatorio ausente;
- rechazo de evidencia que declara secretos;
- conservación de archivos válidos cuando otro falla.

## 8. Validación de status --json

```text
JSON válido: sí
overall_status: WARNING
structured_evidence.available: true
structured_evidence.loaded: 6
structured_evidence.issues: 0
```

Status en modo texto sigue funcionando.

## 9. Validación de audit --json

```text
JSON válido: sí
overall_result: WARN
AUD-SAMBA-001: PASS / INFO
AUD-SERVICES-PORTAINER-001: WARN / LOW
structured_evidence.available: true
structured_evidence.loaded: 6
structured_evidence.issues: 0
```

Audit y Audit verbose en modo texto siguen funcionando.

## 10. Compatibilidad con Markdown

- No se borró ninguna evidencia histórica.
- Status conserva su interpretación documental.
- Audit Engine conserva sus checks actuales.
- Las fichas incluyen referencias a documentos Markdown.
- Si falta `docs/evidencias/structured/`, el loader devuelve un resultado vacío y controlado.
- Las salidas JSON vuelven a `documented_evidence` cuando no hay fichas válidas.

## 11. Resultado de tests

```text
python -m unittest discover -s tests
Ran 53 tests
OK
```

## 12. Resultado de compileall

```text
python -m compileall frankie
OK
```

## 13. Seguridad y operación

- No se tocó el servidor físico Frankie.
- No se conectó a Proxmox ni a las VMs.
- No se ejecutaron comandos live.
- No se usó SSH, Docker ni Samba.
- No se modificaron configuraciones reales.
- El loader no ejecuta subprocess ni escribe ficheros.
- El loader no lee `.env` ni usa red.
- No se incluyeron secretos, credenciales o IPs internas.
- No se implementó Live Mode ni Repair Mode.
- No se modificó la carpeta histórica `cli/`.

## 14. Estado SMB

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO
```

## 15. Estado Portainer

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN / LOW
resolved: false
requires_future_live_review: true
```

El hallazgo del puerto `8000` permanece visible y no se corrigió.

## 16. Riesgos

| Riesgo | Estado | Tratamiento |
| --- | --- | --- |
| Validación parcial del esquema en runtime | Aceptado | Mantener JSON Schema y ampliar validación en una WO futura si aporta valor. |
| Divergencia entre Markdown y JSON | Abierto | Referencias, tests y revisión humana obligatoria. |
| Falta de fecha de captura | Conocido | Definir temporalidad y expiración en la siguiente evolución del contrato. |
| Precedencia de fuentes no automatizada | Intencionado | JSON es complementario durante la transición. |
| Publicación accidental de datos raw | Alto | Loader rechaza declaraciones sensibles y Git requiere revisión previa. |

## 17. Decisión final

```text
listo para revisión
```

El modelo inicial es válido, testeable y compatible con el comportamiento anterior. Puede registrarse como avance de `0.7.0-dev`.
