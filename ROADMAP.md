# Roadmap

Versión base actual: `v0.5.0 Foundation`.

## Fase 1 - Infraestructura Base

### Objetivos

- Documentar host, VMs, red, almacenamiento y servicios base.
- Mantener plantillas Docker, Samba, env y backups.
- Definir estructura de repositorio.

### Estado

En curso.

### Dependencias

- Inventario real.
- Evidencias de auditoría.
- Reglas de seguridad documental.

### Hitos

- Estructura base del repositorio.
- Documentación inicial.
- Auditoria inicial de VMs.

## Fase 2 - Automatizacion

### Objetivos

- Convertir operaciónes repetibles en scripts idempotentes.
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

- Crear auditorías de solo lectura.
- Guardar evidencias.
- Comparar estado real contra documentación.

### Estado

Iniciada.

### Dependencias

- Scripts de auditoría.
- Checklists.

### Hitos

- Auditoria de `srv-servicios`.
- Auditoria de `srv-recursos`.
- Informe de desviaciones.

## Fase 4 - Monitorizacion

### Objetivos

- Definir metricas de salud.
- Preparar monitorización de servicios, backups y espacio.
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

- Incorporar asistencia IA sobre documentación y evidencias.
- Ayudar en diagnostico, propuestas y revisiones.

### Estado

Pendiente.

### Dependencias

- Knowledge base limpia.
- Políticas de seguridad de datos.

### Hitos

- Casos de uso.
- Prompting operativo.
- Políticas de no exposición de secretos.

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
- Políticas de aprobacion.

### Hitos

- Runbooks validados.
- Acciones sugeridas.
- Acciones con aprobacion humana.
