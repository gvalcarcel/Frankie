# Auditoría de documentación didáctica y diseño Live

## Identificación

- Work Order: `WO-0013`.
- Fecha: 2026-06-28.
- Tipo: `OFFLINE`.
- Versión revisada: `0.7.0-dev`.
- Riesgo para producción: nulo.

## Alcance

La intervención completa el material didáctico de Frankie Core para FP Básica, formaliza el diseño seguro de Live Mode y propone futuras Work Orders LIVE. No incorpora código funcional ni conexiones.

## Archivos creados

- `docs/aula/README.md`.
- `docs/aula/que-es-frankie.md`.
- `docs/aula/como-usar-frankie-core.md`.
- `docs/aula/como-leer-un-status.md`.
- `docs/aula/como-leer-una-auditoria.md`.
- `docs/aula/glosario-frankie.md`.
- `docs/aula/actividades-frankie-core.md`.
- `docs/frankie-core/live-mode-design.md`.
- `docs/roadmap/live-workorders.md`.
- `docs/evidencias/frankie-core-v0.7.0/pedagogical_docs_and_live_design_audit.md`.

## Archivos modificados

- `docs/aula/doctor-como-diagnostico.md`.
- `docs/aula/json-en-frankie-core.md`.
- `docs/aula/evidencias-estructuradas.md`.
- `docs/frankie-core/README.md`.
- `docs/frankie-core/cli.md`.
- `docs/frankie-core/evidence.md`.
- `README.md`.
- `ROADMAP.md`.
- `CHANGELOG.md`.

## Documentación didáctica

El itinerario introduce de forma progresiva:

1. diferencia entre Frankie, Frankie Core y repositorio;
2. uso seguro de la CLI;
3. lectura de Status;
4. lectura de Audit;
5. interpretación de Doctor;
6. JSON y evidencias estructuradas;
7. vocabulario técnico básico;
8. planificación antes de modificar un servidor.

Se verificaron ocho actividades. Cada una contiene objetivo, material, pasos guiados, resultado esperado, preguntas de repaso y mini rúbrica de tres puntos. El glosario incluye los 25 términos mínimos de WO-0013.

## Diseño de Live Mode

El diseño propone comandos futuros separados, `live-status` y `live-audit`, para que la intención de conexión sea explícita. Define mínimo privilegio, configuración sin secretos, confirmación previa, lista cerrada de consultas, prohibición de cambios, timeouts, evidencia raw privada, saneamiento y errores seguros.

Los comandos son únicamente una propuesta documental. No están registrados en la CLI ni pueden ejecutarse en esta versión.

## Work Orders LIVE propuestas

- `WO-LIVE-0001`: captura real de estado Frankie.
- `WO-LIVE-0002`: revisión de Portainer puerto 8000.
- `WO-LIVE-0003`: validación avanzada Samba.
- `WO-LIVE-0004`: validación de backups.
- `WO-LIVE-0005`: snapshot/backup antes de cambios.

Cada propuesta declara objetivo, acceso necesario, consultas de solo lectura, riesgos, evidencias y criterio de cierre. Ninguna fue ejecutada.

## Validación local

Se ejecutó correctamente la matriz offline obligatoria:

- ayuda, versión, Status, Inventory, Audit y Doctor;
- variantes JSON de Status, Inventory, Audit y Doctor;
- listado y validación de evidencias;
- parseo correcto de todas las salidas JSON;
- comprobación de enlaces relativos en documentos modificados y creados;
- comprobación de cobertura de actividades y glosario.

```text
python -m unittest discover -s tests
Ran 68 tests
OK

python -m compileall frankie
OK
```

## Seguridad

- No se accedió al servidor físico Frankie.
- No se accedió a VM100 ni VM101.
- No se ejecutaron comandos remotos o scripts de producción.
- No se solicitaron ni utilizaron credenciales.
- No se modificó código, Docker, Samba, firewall, backups o servicios.
- Los ejemplos de configuración usan placeholders.
- La evidencia raw futura se define como privada hasta su saneamiento.

## Confirmación de modos

- Live Mode: no implementado y no ejecutado.
- Repair Mode: no implementado y fuera de alcance.
- Modo actual: offline y de solo lectura.
- Una tarea LIVE futura requerirá indicación y autorización expresa del usuario.

## Estado conocido

- Frankie Core: `0.7.0-dev`.
- Evidencias estructuradas: 6 válidas, 0 inválidas.
- SMB: `OK / PASS / INFO`.
- Portainer puerto 8000: `WARNING / WARN / LOW`.
- Status global: `WARNING`.
- Audit global: `WARN`.

## Riesgos pendientes

- El material necesita revisión final del responsable docente antes de usarse como evaluación formal.
- Las evidencias offline pueden quedar desactualizadas y deben mostrar siempre su origen.
- Live Mode aún necesita decisiones técnicas y pruebas controladas sobre autenticación, transporte y saneamiento.
- El aviso de Portainer sigue abierto; este documento no autoriza corregirlo.
- Una consulta LIVE puede exponer información interna si no se aplican límites y saneamiento.

## Decisión final

```text
listo para revisión
```
