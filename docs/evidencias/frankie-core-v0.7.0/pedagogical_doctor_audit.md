# Auditoría de Doctor con enfoque pedagógico

Fecha: 2026-06-27

Tipo de Work Order: `OFFLINE`

Decisión final: `listo para revisión`

## 1. Alcance

WO-0011 mejora la interpretación y comunicación de hallazgos existentes en Doctor. No añade checks a Audit Engine ni cambia el estado conocido de la infraestructura.

Doctor sigue siendo diagnóstico offline de solo lectura y no implementa reparación.

## 2. Archivos creados

- `docs/aula/doctor-como-diagnostico.md`
- `docs/evidencias/frankie-core-v0.7.0/pedagogical_doctor_audit.md`

## 3. Archivos modificados

- `CHANGELOG.md`
- `README.md`
- `ROADMAP.md`
- `docs/frankie-core/README.md`
- `docs/frankie-core/doctor.md`
- `frankie/core/models.py`
- `frankie/doctor/rules.py`
- `frankie/doctor/doctor_engine.py`
- `frankie/output/console.py`
- `tests/test_doctor.py`

## 4. Diseño del Doctor pedagógico

`DoctorAdvice` representa ahora de forma explícita:

- `issue_id`;
- `title`;
- `status`;
- `severity`;
- `urgency`;
- `impact`;
- `why_it_matters`;
- `recommended_action`;
- `safe_next_steps`;
- `do_not`;
- `student_explanation`;
- `evidence`;
- `result`;
- `limitation`.

El modelo queda preparado para una futura serialización sin implementar todavía `doctor --json`.

## 5. Diferencia entre Audit y Doctor

Audit Engine conserva la responsabilidad de ejecutar checks sobre evidencias y producir hallazgos con estado y severidad.

Doctor recibe esos hallazgos en memoria, descarta los `PASS` como incidencias activas y añade interpretación, urgencia, impacto y orientación segura.

Doctor no invoca el comando Audit mediante subprocess y Audit no depende de Doctor.

## 6. Validación de Portainer

La única incidencia activa es:

```text
Issue: AUD-SERVICES-PORTAINER-001
Title: Portainer port 8000 remains published
Severity: LOW
Urgency: LOW
Overall doctor result: ACTIONS_RECOMMENDED
```

La recomendación remite a una futura Work Order LIVE autorizada. La salida prohíbe reiniciar Portainer, retirar mappings o cambiar firewall desde una tarea offline.

## 7. Confirmación de SMB validado

SMB no aparece como incidencia activa.

En modo verbose se presenta como contexto resuelto:

```text
AUD-SAMBA-001 (PASS; no active action)
```

No se recupera el pendiente histórico como problema actual.

## 8. Validación de doctor

```text
Código de salida: 0
Versión: 0.7.0-dev
Incidencias revisadas: 1
Evidencias estructuradas: 6 loaded
Resultado: ACTIONS_RECOMMENDED
```

La salida contiene `Impact`, `Why it matters`, `Recommended action`, `Safe next steps`, `Do not` y `Student explanation`.

## 9. Validación de doctor --verbose

```text
Código de salida: 0
Incidencia principal: AUD-SERVICES-PORTAINER-001
SMB: PASS; no active action
Modo: read-only foundation
Conexión live: no
Reparaciones: no
```

Verbose añade checks resueltos, estado/severidad, resultado y razón de ausencia de reparación automática sin cambiar el diagnóstico.

## 10. Compatibilidad

- `status` mantiene `WARNING`.
- `status --json` sigue siendo JSON válido.
- `audit` mantiene `WARN`.
- `audit --json` sigue siendo JSON válido y conserva SMB `PASS` y Portainer `WARN`.
- `inventory` sigue funcionando.
- `help` sigue funcionando.
- `version` mantiene `0.7.0-dev`.

## 11. Resultado de tests

```text
python -m unittest discover -s tests
Ran 54 tests
OK
```

Los tests comprueban campos pedagógicos, Portainer, SMB resuelto, evidencia estructurada, compatibilidad JSON y ausencia de operaciones de sistema o red en el flujo Doctor.

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
- Doctor no usa subprocess, `os.system` ni conexiones de red.
- Doctor no lee `.env` ni escribe ficheros.
- No se implementó Live Mode.
- No se implementó Repair Mode.
- No se incluyeron secretos, credenciales o IPs internas.

## 14. Estado SMB

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO / no active action
```

## 15. Estado Portainer

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN / LOW
Doctor urgency: LOW
Doctor result: ACTIONS_RECOMMENDED
```

El puerto `8000` sigue visible y no fue corregido.

## 16. Riesgos

| Riesgo | Estado | Tratamiento |
| --- | --- | --- |
| Explicaciones demasiado extensas | Controlado | Salida base acotada y contexto adicional en verbose. |
| Confundir recomendación con autorización | Controlado | Toda acción real se remite a una WO LIVE explícita. |
| Urgencia y severidad divergentes | Esperado | Documentar que responden a preguntas distintas. |
| Reglas pedagógicas específicas por check | Abierto | Mantener fallback genérico y añadir reglas solo con tests. |
| Futuro JSON de Doctor | Pendiente | El modelo está preparado, pero el flag queda fuera de alcance. |

## 17. Decisión final

```text
listo para revisión
```

Doctor mejora su capacidad de explicar diagnósticos técnicos sin ampliar permisos ni introducir acciones sobre infraestructura.
