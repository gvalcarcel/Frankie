# Roadmap

Version base actual: `v0.5.0 Foundation`.

## Fase 1 - Infraestructura Base

### Objetivos

- Documentar host, VMs, red, almacenamiento y servicios base.
- Mantener plantillas Docker, Samba, env y backups.
- Definir estructura de repositorio.

### Estado

En curso.

### Dependencias

- Inventario real.
- Evidencias de auditoria.
- Reglas de seguridad documental.

### Hitos

- Estructura base del repositorio.
- Documentacion inicial.
- Auditoria inicial de VMs.

## Fase 2 - Automatizacion

### Objetivos

- Convertir operaciones repetibles en scripts idempotentes.
- Mantener dry-run y validaciones.
- Evitar secretos en automatizaciones.

### Estado

Iniciada.

### Dependencias

- Fase 1.
- Snapshots antes de pruebas.

### Hitos

- Scripts base.
- Scripts idempotentes.
- Validacion controlada.

## Fase 3 - Auditoria

### Objetivos

- Crear auditorias de solo lectura.
- Guardar evidencias.
- Comparar estado real contra documentacion.

### Estado

Iniciada.

### Dependencias

- Scripts de auditoria.
- Checklists.

### Hitos

- Auditoria de `srv-servicios`.
- Auditoria de `srv-recursos`.
- Informe de desviaciones.

## Fase 4 - Monitorizacion

### Objetivos

- Definir metricas de salud.
- Preparar monitorizacion de servicios, backups y espacio.
- Registrar alertas.

### Estado

Pendiente.

### Dependencias

- Auditoria estable.
- Servicios definidos.

### Hitos

- Eleccion de herramienta.
- Checks iniciales.
- Alertas basicas.

## Fase 5 - Dashboard

### Objetivos

- Crear vista operativa del estado de infraestructuras.
- Mostrar servicios, backups, incidencias y riesgos.

### Estado

Pendiente.

### Dependencias

- Monitorizacion.
- Modelo de datos.

### Hitos

- Prototipo de dashboard.
- Vista por servidor.
- Vista por laboratorio.

## Fase 6 - Knowledge Base

### Objetivos

- Consolidar conocimiento reutilizable.
- Documentar patrones de despliegue.
- Registrar incidencias y decisiones.

### Estado

Pendiente.

### Dependencias

- Governance.
- Evidencias reales.

### Hitos

- Taxonomia de conocimiento.
- Plantillas de incidencias.
- Guias operativas.

## Fase 7 - Frankie AI

### Objetivos

- Incorporar asistencia IA sobre documentacion y evidencias.
- Ayudar en diagnostico, propuestas y revisiones.

### Estado

Pendiente.

### Dependencias

- Knowledge base limpia.
- Politicas de seguridad de datos.

### Hitos

- Casos de uso.
- Prompting operativo.
- Politicas de no exposicion de secretos.

## Fase 8 - Autocuracion

### Objetivos

- Proponer respuestas automaticas o semiautomaticas ante incidencias.
- Mantener control humano en cambios de riesgo.

### Estado

Pendiente.

### Dependencias

- Monitorizacion.
- Auditoria.
- Runbooks.
- Politicas de aprobacion.

### Hitos

- Runbooks validados.
- Acciones sugeridas.
- Acciones con aprobacion humana.
