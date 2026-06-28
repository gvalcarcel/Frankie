# Sistema de agentes de Frankie

## Propósito

Esta carpeta define roles reutilizables para diseñar y ejecutar futuras Work Orders. Cada agente aporta una misión, límites, entradas, salidas y criterios de validación.

Los agentes no son procesos autónomos ni permisos para actuar. Son contratos de trabajo que Codex debe leer y combinar dentro del alcance autorizado.

## Categorías

- `hardware/`: host físico, Proxmox, red, almacenamiento, servicios y control LIVE.
- `software/`: arquitectura, Python, CLI, datos, evidencias, QA, releases y repositorio.
- `transversal/`: seguridad, auditoría, documentación, DevOps, pedagogía, producto y UX.

## Cómo invocarlos

Una Work Order puede declarar rutas exactas:

```text
Agentes asignados:
- docs/agents/software/software-architect.md
- docs/agents/software/python-developer.md
- docs/agents/software/qa-engineer.md
- docs/agents/transversal/security-reviewer.md
- docs/agents/transversal/technical-writer.md
```

Al recibir esa lista, Codex debe:

1. leer todos los archivos asignados antes de actuar;
2. respetar sus límites y reglas `Must enforce`;
3. combinar responsabilidades sin ampliar la Work Order;
4. aplicar los criterios de validación relevantes;
5. reportar riesgos y límites desde cada rol;
6. detenerse si dos agentes detectan requisitos incompatibles que no puedan resolverse con el alcance aprobado.

## Orden recomendado

1. Product Owner aclara valor y alcance cuando sea necesario.
2. Arquitectos y diseñadores definen la solución.
3. Implementadores o responsables operativos ejecutan el trabajo autorizado.
4. QA, Security Reviewer y System Auditor validan.
5. Technical Writer y Repository Maintainer cierran documentación y trazabilidad.

No todas las WOs necesitan todos los pasos ni todos los agentes. La [matriz de selección](agent-selection-matrix.md) ayuda a elegir el conjunto mínimo suficiente.

## Regla OFFLINE/LIVE

- OFFLINE es el modo predeterminado.
- Incluir un agente hardware no autoriza conexión o cambios.
- Toda WO LIVE debe asignar `LIVE Operations Controller` y `Security Reviewer`.
- Auditoría y reparación deben mantenerse separadas.
- Ningún snippet de agente sustituye la autorización explícita del usuario.

## Documentos operativos

- [Índice de agentes](agents-index.md).
- [Guía de uso](usage-guide.md).
- [Matriz de selección](agent-selection-matrix.md).
- [Plantillas de Work Orders](../../.vscode/prompts/).

## Mantenimiento

Los perfiles se versionan como documentación de producto. Un cambio de misión, límite o categoría debe revisarse como una modificación de contrato y reflejarse en el índice y la matriz.
