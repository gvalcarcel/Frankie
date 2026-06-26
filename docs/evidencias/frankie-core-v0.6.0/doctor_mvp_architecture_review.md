# Frankie Doctor MVP - Architectural Review

Fecha de revisión: 2026-06-26

Work Order revisada: WO-0005 - Frankie Doctor MVP

Versión del proyecto: 0.6.0-dev

Decisión final: apto para cierre de WO-0005

## Alcance

Esta revisión valida la arquitectura del comando:

```bash
python -m frankie doctor
python -m frankie doctor --verbose
```

La revisión se limita al repositorio local. No se han ejecutado comandos contra servidores reales, no se han modificado sistemas, no se han creado tags y no se ha publicado ninguna release.

## Resumen ejecutivo

Frankie Doctor MVP queda implementado como una capa de diagnóstico asistido de solo lectura sobre Audit Engine v1.

El diseño es coherente con la arquitectura actual de Frankie Core: el comando no obtiene datos en vivo, no ejecuta acciones de reparación, no escribe ficheros, no instala paquetes, no reinicia servicios y no necesita secretos.

Doctor interpreta hallazgos del Audit Engine y los convierte en explicaciones operativas, impacto probable, pasos seguros y acciones que no deben realizarse todavía. Esta separación mantiene a Audit Engine como fuente de evaluación técnica y a Doctor como capa de orientación.

## Validaciones arquitectónicas

| Área | Resultado | Observación |
| --- | --- | --- |
| Integración CLI | PASS | `frankie doctor` está integrado en el despachador principal y acepta `--verbose`. |
| Relación con Audit Engine | PASS | Doctor consume `run_audit()` y no duplica comprobaciones de auditoría. |
| Solo lectura | PASS | El alcance del reporte declara sin conexión en vivo, sin reparaciones, sin escritura y sin ejecución de comandos. |
| Reparación automática | PASS | No existe mecanismo de autocorrección ni ejecución de acciones. |
| Modelos internos | PASS | `DoctorReport`, `DoctorFinding` y `DoctorAdvice` encapsulan resultado, evidencias, severidad y pasos. |
| Reglas de diagnóstico | PASS | Las reglas convierten hallazgos `AUD-*` en explicaciones y recomendaciones seguras. |
| Salida normal | PASS | La salida muestra resumen, hallazgos explicados, evidencias, pasos seguros y resultado global. |
| Salida verbose | PASS | La salida detallada añade check de auditoría, estado/severidad, resultado y limitaciones. |
| Compatibilidad con comandos previos | PASS | `status`, `inventory`, `audit`, `version` y `help` siguen funcionando. |
| Tests | PASS | La suite cubre ejecución normal, verbose, modo solo lectura y ausencia de comandos pendientes como placeholder. |
| Documentación | PASS | Existe documentación específica de `doctor` y el índice de Frankie Core ya no lo presenta como placeholder. |

## Flujo interno

El flujo validado es:

```text
python -m frankie doctor
  -> frankie.app
  -> frankie.commands.doctor.run()
  -> frankie.doctor.doctor_engine.run_doctor()
  -> frankie.audit.audit_engine.run_audit()
  -> frankie.doctor.advice.build_doctor_findings()
  -> frankie.output.console.render_doctor()
```

La dependencia directa de Doctor hacia Audit Engine es aceptable para este MVP porque evita crear una segunda fuente de verdad. Las reglas de diagnóstico trabajan sobre hallazgos ya evaluados.

## Relación con Audit Engine

Doctor no sustituye a Audit Engine.

Audit Engine:

- evalúa evidencias;
- produce estados, severidades y recomendaciones;
- mantiene identificadores `AUD-*`.

Doctor:

- interpreta hallazgos no satisfactorios;
- explica el significado operativo;
- propone pasos manuales seguros;
- explicita qué no debe hacerse todavía.

Esta separación es correcta para una plataforma educativa porque permite enseñar la diferencia entre auditar, diagnosticar y reparar.

## Garantías de solo lectura

La revisión no ha encontrado llamadas de riesgo en el flujo productivo de Doctor:

- no usa SSH;
- no usa sockets;
- no usa peticiones HTTP;
- no usa `subprocess`;
- no usa `os.system`;
- no instala paquetes;
- no reinicia servicios;
- no borra archivos;
- no escribe archivos;
- no consume credenciales.

Las apariciones de términos como `repair`, `restart`, `Docker` o `systemctl` son texto explicativo o recomendaciones de no actuación, no llamadas ejecutables.

## Resultado global

El resultado global de Doctor se calcula a partir de los hallazgos interpretados:

- `CRITICAL` para fallos de severidad alta o crítica;
- `INSUFFICIENT_EVIDENCE` cuando predominan estados sin evidencia suficiente;
- `ACTIONS_RECOMMENDED` cuando hay fallos, avisos o pendientes;
- `HEALTHY` cuando no quedan hallazgos accionables y Audit Engine pasa.

El valor `ATTENTION_REQUIRED` está reservado en el modelo, pero no se utiliza todavía en el algoritmo actual. Se considera una mejora futura menor, no bloqueante.

## Revisión de tests

Se han validado los comandos principales:

```bash
python -m frankie doctor
python -m frankie doctor --verbose
python -m frankie audit
python -m frankie audit --verbose
python -m frankie status
python -m frankie inventory
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

La suite de tests queda sin tests omitidos tras sustituir el antiguo test de placeholder por una comprobación explícita de que no quedan comandos foundation pendientes.

## Correcciones menores aplicadas

Durante la revisión se han aplicado correcciones menores permitidas por la Work Order:

- `docs/frankie-core/README.md`: se eliminó la referencia obsoleta que presentaba `doctor` como comando no implementado.
- `CHANGELOG.md`: se sustituyó la entrada obsoleta de `doctor` como comando futuro por una descripción coherente con el estado actual.
- `tests/test_not_implemented_commands.py`: se reemplazó un `skipTest` por una validación real de que `status`, `inventory`, `audit` y `doctor` ya no son placeholders.

No se ha modificado la funcionalidad de Frankie Doctor.

## Riesgos detectados

| Riesgo | Severidad | Estado | Recomendación |
| --- | --- | --- | --- |
| `ATTENTION_REQUIRED` existe en el modelo pero no se emite todavía. | Menor | Aceptado | Definir su semántica en una Work Order futura si se necesita un estado intermedio. |
| Doctor depende completamente de evidencias documentales. | Menor | Aceptado | Mantenerlo explícito hasta que exista una capa controlada de recolección en vivo. |
| No existe salida estructurada JSON/Markdown para Doctor. | Mejora futura | Aceptado | Evaluar cuando Frankie Core incorpore formatos de salida comunes. |
| No hay reparación automática. | No aplica | Por diseño | Mantener así hasta una fase futura de autocuración con controles estrictos. |

## Recomendaciones

- Mantener Doctor como capa explicativa mientras `v0.6.0` siga en modo solo lectura.
- No introducir reparación automática en esta línea de trabajo.
- Añadir salida estructurada solo cuando exista una estrategia común para todos los comandos.
- Documentar en una Work Order futura cuándo usar `ATTENTION_REQUIRED`.
- Registrar WO-0005 en GitHub solo después de la revisión final de secretos, cachés y estado Git.

## Decisión final

La arquitectura de Frankie Doctor MVP es coherente con Frankie Core `0.6.0-dev`.

El comando cumple el alcance definido:

- diagnóstico asistido;
- reutilización de Audit Engine;
- explicación comprensible;
- modo verbose;
- ausencia de acciones destructivas;
- ausencia de escritura;
- ausencia de secretos;
- integración con documentación y tests.

Decisión:

```text
apto para cierre de WO-0005
```
