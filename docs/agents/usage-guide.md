# Guía de uso de agentes

## Qué son

Los agentes son perfiles documentados que orientan el trabajo de Codex dentro de una Work Order. No ejecutan tareas por sí solos y no sustituyen el alcance, la autorización ni los criterios de cierre.

## Cómo usarlos en una WO

1. Clasifica la WO como OFFLINE o LIVE.
2. Define objetivo, alcance y fuera de alcance.
3. Consulta la [matriz de selección](agent-selection-matrix.md).
4. Asigna el conjunto mínimo de agentes que cubra diseño, ejecución y validación.
5. Incluye sus rutas en `Agentes asignados`.
6. Ordena los entregables y validaciones.
7. Usa una plantilla de `.vscode/prompts/`.

Desde VS Code/Codex, abre la plantilla, completa los campos y adjunta o referencia los agentes seleccionados. Codex debe leerlos antes de actuar.

## Cómo combinarlos

- Un agente principal decide o produce el resultado central.
- Agentes especialistas cubren datos, infraestructura, pedagogía o release.
- QA y Security Reviewer aportan gates independientes.
- Technical Writer documenta hechos ya verificados.
- Repository Maintainer registra únicamente el alcance aprobado.

Evita asignar dos agentes con decisiones contradictorias sin declarar quién resuelve el conflicto. Product Owner resuelve prioridad; Software Architect, arquitectura; LIVE Operations Controller, seguridad operativa inmediata.

## Hardware, software y transversales

- **Hardware:** sistemas reales, virtualización, red, almacenamiento y servicios. Pueden diseñar offline, pero actuar exige una WO LIVE.
- **Software:** Frankie Core, CLI, datos, tests, automatización y GitHub.
- **Transversales:** seguridad, auditoría, documentación, pedagogía, producto y comunicación.

## Tamaño de las Work Orders

### Evitar WOs demasiado pequeñas

Agrupa cambios que comparten objetivo, archivos y validación. No separes en varias WOs una implementación, sus tests y su documentación si forman una unidad revisable.

### Cuándo usar una WO amplia

Úsala para trabajo OFFLINE con bajo riesgo y fuerte cohesión: documentación de un subsistema, una feature completa con tests o preparación de release.

### Cuándo usar una WO pequeña

Úsala para acciones LIVE, cambios de red, firewall, almacenamiento, permisos, servicios o cualquier operación con rollback independiente.

## Ejemplo 1: desarrollo CLI

```text
Tipo: OFFLINE
Objetivo: implementar un comando de consulta sin efectos laterales.
Agentes asignados:
- docs/agents/software/software-architect.md
- docs/agents/software/python-developer.md
- docs/agents/software/cli-designer.md
- docs/agents/software/qa-engineer.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/technical-writer.md
- docs/agents/software/repository-maintainer.md
Validación: consola, JSON, errores, unittest y compileall.
```

## Ejemplo 2: release

```text
Tipo: OFFLINE con GitHub
Objetivo: preparar o publicar una versión ya validada.
Agentes asignados:
- docs/agents/software/release-manager.md
- docs/agents/software/repository-maintainer.md
- docs/agents/software/qa-engineer.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/technical-writer.md
- docs/agents/transversal/system-auditor.md
Validación: versión, tests, tag, release remota y post-release.
```

## Ejemplo 3: documentación de aula

```text
Tipo: OFFLINE
Objetivo: crear una práctica guiada para FP Básica.
Agentes asignados:
- docs/agents/transversal/docente-fp-basica.md
- docs/agents/transversal/devops-educativo.md
- docs/agents/transversal/ux-writer.md
- docs/agents/transversal/technical-writer.md
- docs/agents/transversal/product-owner.md
Validación: nivel, pasos, resultado, preguntas y mini rúbrica.
```

## Ejemplo 4: intervención LIVE en Portainer

```text
Tipo: LIVE de solo lectura
Objetivo: explicar la publicación del puerto 8000 sin cambiarla.
Agentes asignados:
- docs/agents/hardware/live-operations-controller.md
- docs/agents/hardware/service-administrator.md
- docs/agents/hardware/network-administrator.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/system-auditor.md
- docs/agents/transversal/technical-writer.md
Validación: identidad, allowlist, timeout, evidencia saneada y cierre sin cambios.
```

## Ejemplo 5: revisión de backups

```text
Tipo: LIVE de solo lectura
Objetivo: comprobar cobertura, antigüedad y trazabilidad sin restaurar ni borrar.
Agentes asignados:
- docs/agents/hardware/storage-backup-administrator.md
- docs/agents/hardware/live-operations-controller.md
- docs/agents/software/evidence-engineer.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/system-auditor.md
- docs/agents/transversal/technical-writer.md
Validación: metadatos, logs saneados, gaps y límites de restaurabilidad.
```
