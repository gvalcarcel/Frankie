# Matriz de selección de agentes

## Regla rápida

Selecciona agentes por riesgo y entregable, no por cantidad. Toda combinación debe incluir quien produce el resultado y quien lo valida.

| Tipo de Work Order | Agentes recomendados | Modo | Gate principal |
|---|---|---|---|
| Desarrollo CLI | Software Architect; Python Developer; CLI Designer; QA Engineer; Security Reviewer; Technical Writer; Repository Maintainer | OFFLINE | Tests, contratos y ausencia de efectos laterales |
| Evidencias estructuradas | Software Architect; Data Model Designer; Evidence Engineer; QA Engineer; Security Reviewer; Technical Writer | OFFLINE/BOTH | Esquema, trazabilidad y saneamiento |
| Release | Release Manager; Repository Maintainer; QA Engineer; Security Reviewer; Technical Writer; System Auditor | OFFLINE | Versión, test, tag y verificación remota |
| Documentación de aula | Docente FP Básica; DevOps Educativo; UX Writer; Technical Writer; Product Owner | OFFLINE | Nivel, exactitud y resultado evaluable |
| Work Order LIVE | LIVE Operations Controller; Service Administrator; Network Administrator; Security Reviewer; System Auditor; Technical Writer | LIVE | Autorización, allowlist, parada y evidencia |
| Hardware / Proxmox | Hardware Infrastructure Architect; Proxmox / Virtualization Administrator; Storage and Backup Administrator; Network Administrator; Security Reviewer; System Auditor | BOTH | Identidad, capacidad, backup y rollback |

## Ajustes por situación

| Situación adicional | Añadir | Motivo |
|---|---|---|
| Código Python | Python Developer | Implementación y patrones del paquete activo |
| Nuevo JSON o esquema | Data Model Designer | Compatibilidad y tipos |
| Automatización futura | Automation Readiness Engineer | Idempotencia, dry-run y guardrails |
| Cambio físico | Physical Server Technician | Seguridad y validación hands-on |
| Backups o restauración | Storage and Backup Administrator | Integridad y recuperabilidad |
| Mensajes CLI complejos | UX Writer | Claridad y recuperación de errores |
| Prioridad o alcance discutible | Product Owner | Decisión de valor y aceptación |
| Actividad docente técnica | DevOps Educativo | Aprendizaje auténtico y seguro |

## Combinaciones mínimas

- Cambio documental simple: Technical Writer + Repository Maintainer.
- Cambio funcional offline: implementador + QA Engineer + Security Reviewer.
- Cambio LIVE: LIVE Operations Controller + especialista técnico + Security Reviewer + System Auditor.
- Publicación: Release Manager + Repository Maintainer + QA Engineer + Security Reviewer.

Una combinación mínima no elimina responsabilidades obligatorias de la Work Order.
