# Auditoría del sistema de agentes reutilizables

## Identificación

- Work Order: `WO-0016`.
- Fecha: 2026-06-28.
- Tipo: `OFFLINE`.
- Objetivo: incorporar un sistema operativo de agentes y plantillas para futuras Work Orders.
- Riesgo para producción: nulo.

## Estructura creada

```text
docs/agents/
├── README.md
├── agents-index.md
├── usage-guide.md
├── agent-selection-matrix.md
├── hardware/       7 agentes
├── software/       9 agentes
└── transversal/    8 agentes

.vscode/prompts/    6 plantillas
```

## Agentes hardware creados

1. Hardware Infrastructure Architect.
2. Physical Server Technician.
3. Proxmox / Virtualization Administrator.
4. Network Administrator.
5. Storage and Backup Administrator.
6. Service Administrator.
7. LIVE Operations Controller.

## Agentes software creados

1. Software Architect.
2. Python Developer.
3. CLI Designer.
4. QA Engineer.
5. Data Model Designer.
6. Evidence Engineer.
7. Release Manager.
8. Repository Maintainer.
9. Automation Readiness Engineer.

## Agentes transversales creados

1. Security Reviewer.
2. System Auditor.
3. Technical Writer.
4. DevOps Engineer.
5. DevOps Educativo.
6. Docente FP Básica.
7. Product Owner.
8. UX Writer.

## Plantillas creadas

- `.vscode/prompts/work-order-template.md`.
- `.vscode/prompts/offline-work-order-template.md`.
- `.vscode/prompts/live-work-order-template.md`.
- `.vscode/prompts/release-work-order-template.md`.
- `.vscode/prompts/pedagogical-work-order-template.md`.
- `.vscode/prompts/agent-selector.md`.

## Archivos generales creados

- `docs/agents/README.md`.
- `docs/agents/agents-index.md`.
- `docs/agents/usage-guide.md`.
- `docs/agents/agent-selection-matrix.md`.

## Archivos modificados

- `.gitignore`: permite versionar solo `.vscode/prompts/*.md` dentro de `.vscode`.
- `README.md`: incorpora el sistema y corrige el estado publicado de `v0.7.0`.
- `ROADMAP.md`: registra agentes, plantillas y selección OFFLINE/LIVE.
- `CHANGELOG.md`: añade el sistema bajo `Unreleased`.
- `docs/frankie-core/README.md`: enlaza la operación con agentes.

## Validación del número de agentes

```text
Hardware:      7
Software:      9
Transversales: 8
Total:        24
```

Resultado: `PASS`.

## Validación de estructura por agente

Los 24 archivos se comprobaron automáticamente. Cada uno contiene una vez:

- título `Agent`;
- Category;
- Mission;
- When to use;
- Responsibilities;
- Must enforce;
- Must not do;
- Inputs expected;
- Outputs expected;
- Typical Work Orders;
- Suggested companion agents;
- Prompt snippet.

Todos incluyen clasificación OFFLINE/LIVE, límite de alcance y reporte de riesgos. Security Reviewer conserva además la regla específica de bloqueo ante secretos reales o acciones inseguras.

Resultado: `PASS`.

## Validación del índice

`agents-index.md` contiene los 24 agentes con categoría, uso, modo, riesgo principal, compañeros y ruta. Cada ruta se contrastó con un archivo existente.

Resultado: `PASS`.

## Validación de la guía de uso

La guía explica selección, combinación, categorías, tamaño de WO y uso desde VS Code/Codex. Incluye ejemplos de:

- desarrollo CLI;
- release;
- documentación de aula;
- intervención LIVE en Portainer;
- revisión de backups.

Resultado: `PASS`.

## Validación de la matriz de selección

La matriz cubre Desarrollo CLI, Evidencias estructuradas, Release, Documentación de aula, Work Order LIVE y Hardware/Proxmox. También incluye ajustes por situación y combinaciones mínimas.

Resultado: `PASS`.

## Validación VS Code/Codex

- Se detectaron seis plantillas Markdown.
- Las seis aparecen como archivos versionables pese al bloqueo general de `.vscode`.
- Cada plantilla contiene los controles exigidos para su tipo de WO.
- `agent-selector.md` enruta código, servidores, alumnado, release y evidencias.

Resultado: `PASS`.

## Validación técnica

Se ejecutaron correctamente:

- `python -m frankie version`;
- `python -m frankie help`;
- `python -m frankie status`;
- `python -m frankie audit`;
- `python -m frankie doctor`.

```text
python -m unittest discover -s tests
Ran 68 tests
OK

python -m compileall frankie
OK
```

## Revisión de seguridad

- No se incluyeron contraseñas, tokens, claves privadas o credenciales reales.
- Los términos sensibles aparecen únicamente como reglas preventivas o ejemplos de campos prohibidos.
- No se incluyeron direcciones IP internas.
- No se incluyeron `.env`, logs, dumps, backups o cachés Python.
- No se creó funcionalidad ejecutable desde los perfiles o plantillas.

## Confirmaciones

- No hubo cambios funcionales en Frankie Core.
- No se tocó el servidor físico Frankie.
- No se accedió a VM100 ni VM101.
- No se ejecutó Live Mode ni Repair Mode.
- No se creó tag ni GitHub Release.
- El sistema de agentes no concede permisos; solo define contratos de trabajo.

## Riesgos

- Asignar demasiados agentes puede añadir coste sin mejorar la decisión.
- Asignar muy pocos puede dejar sin cubrir seguridad, QA o documentación.
- Un perfil hardware no constituye autorización LIVE.
- Los snippets deben mantenerse sincronizados con el índice y la matriz.
- Las plantillas ayudan a estructurar, pero no sustituyen la revisión humana del alcance.

## Decisión final

```text
listo para revisión
```
