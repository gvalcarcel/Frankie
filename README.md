# Frankie

Frankie es una plataforma para administrar, desplegar, documentar, auditar y monitorizar infraestructuras Linux destinadas a laboratorios docentes.

El proyecto no es solo un servidor ni una coleccion de scripts. Frankie debe funcionar como una plataforma mantenible, versionada y preparada para crecer durante años como producto software.

## Origin and Purpose

> "No eras el más bonito y te tuvimos que hacer con un megamix de piezas, pero naciste siendo leyenda".

Frankie nace como servidor educativo dentro del Grado Básico en Informática y Comunicaciones del Centro de Formación Somorrostro.

Su origen es humilde y muy real: una máquina construida con recursos hardware limitados, reutilizando componentes tomados de distintos equipos y aprovechando lo que estaba disponible en el centro. Esa limitación no es una debilidad; forma parte de su valor didáctico. Frankie representa una idea muy importante en informática: con criterio técnico, documentación, orden y ganas de aprender, incluso una infraestructura modesta puede convertirse en una plataforma poderosa.

El propósito de Frankie es ambicioso: convertirse en una plataforma real de aprendizaje, automatización, documentación, auditoría y servicios de aula. No se trata únicamente de levantar servicios, sino de construir un entorno donde el alumnado pueda experimentar con redes, servidores, automatización, recursos compartidos, buenas prácticas DevOps y administración de sistemas.

El objetivo principal es ofrecer al alumnado de Grado Básico una infraestructura potente, realista y motivadora. Frankie busca que estos alumnos adquieran competencias técnicas sólidas, ganen confianza y se sientan capaces de trabajar de tú a tú con alumnado de Grado Medio y Grado Superior.

Frankie es, por tanto, una herramienta técnica y también una declaración educativa: aprender haciendo, documentar lo aprendido y demostrar que la calidad profesional no depende solo del hardware disponible, sino de cómo se piensa, se cuida y se evoluciona un proyecto.

## Descripción del proyecto

Frankie centraliza conocimiento, procedimientos, plantillas, auditorías, checklists y automatizaciones controladas para infraestructuras Linux de aula.

El repositorio actúa como Single Source of Truth del proyecto:

- documentación técnica,
- decisiones de arquitectura,
- plantillas de configuración,
- scripts revisables,
- evidencias de auditoría,
- checklists operativos,
- futura monitorización,
- futura capa de asistencia con IA.

## Objetivos

- Mantener documentada la infraestructura de laboratorio.
- Facilitar despliegues repetibles y auditables.
- Separar configuraciones reales de plantillas versionables.
- Evitar inclusión de secretos en Git.
- Preparar automatizaciones idempotentes y seguras.
- Permitir validaciones previas con dry-run.
- Construir una base de conocimiento reutilizable.
- Evolucionar hacia monitorización, dashboard y autocuración.

## Arquitectura general

La arquitectura actual documentada se organiza alrededor de:

```text
Frankie
├── governance      Políticas, visión y reglas del proyecto
├── knowledge       Base de conocimiento operativa
├── docs            Documentación técnica y evidencias
├── scripts         Automatizaciones y auditorías
├── docker          Plantillas Docker Compose
├── samba           Plantillas Samba
├── monitor         Futuro sistema de monitorización
├── ai              Futuras capacidades de asistencia IA
├── backups         Plantillas de backup
├── checklists      Validaciones operativas
└── env             Plantillas de variables de entorno
```

Infraestructura de referencia actualmente documentada:

| Capa | Nombre | Función |
|---|---|---|
| Host físico | Frankie (`srv-aula113`) | Proxmox VE, almacenamiento ZFS y gestión de VMs |
| VM 100 | `srv-servicios` | Docker, Portainer, PostgreSQL y n8n |
| VM 101 | `srv-recursos` | Samba y recursos docentes compartidos |

## Tecnologias utilizadas

- Linux / Ubuntu Server.
- Proxmox VE.
- Docker Engine.
- Docker Compose.
- Portainer CE.
- PostgreSQL.
- n8n.
- Samba.
- UFW.
- Fail2ban.
- Bash.
- Markdown.
- GitHub.

## Estado actual

Estado de producto: `v0.8.0-dev` abierto sobre la release estable `v0.7.0`.

El repositorio contiene:

- estructura inicial de plataforma,
- documentación base,
- plantillas Docker/Samba/env/backups,
- scripts idempotentes con dry-run,
- scripts de auditoría de solo lectura,
- evidencias de auditoría inicial,
- checklists de validación,
- CLI offline con salida JSON y consulta de evidencias estructuradas,
- guías didácticas y actividades para FP Básica,
- diseño seguro de Live Mode, sin implementación real,
- sistema operativo de 24 agentes reutilizables,
- matriz de selección y plantillas de Work Orders para VS Code/Codex.
- resumen avanzado de evidencias e informes consolidados Markdown/JSON.
- arquitectura de Live Mode preparada, simulable y desactivada sin transporte real.

Pendientes destacados:

- ejecutar el backlog priorizado de `v0.8.0-dev`,
- revisión del puerto `8000` de Portainer,
- reservas DHCP o estrategia de nombres estable,
- prueba formal de restauración,
- definición de monitorización,
- preparación de dashboard,
- consolidacion de knowledge base.

Material docente: [docs/aula/README.md](docs/aula/README.md).

Informes consolidados: [docs/frankie-core/reports.md](docs/frankie-core/reports.md).

Sistema de agentes: [docs/agents/README.md](docs/agents/README.md). Las plantillas de `.vscode/prompts/` ayudan a construir Work Orders generales, OFFLINE, LIVE, de release y pedagógicas.

Live Mode y Repair Mode no están implementados. Las futuras tareas LIVE solo se ejecutarán cuando el usuario lo indique y autorice mediante una Work Order específica.

## Roadmap

Ver [ROADMAP.md](ROADMAP.md).

Fases previstas:

1. Infraestructura Base.
2. Automatizacion.
3. Auditoria.
4. Monitorizacion.
5. Dashboard.
6. Knowledge Base.
7. Frankie AI.
8. Autocuracion.

## Estructura del repositorio

```text
Frankie/
├── docs/
│   └── agents/
├── governance/
├── knowledge/
├── scripts/
├── docker/
├── samba/
├── monitor/
├── ai/
├── backups/
├── checklists/
├── env/
├── .github/
└── .vscode/prompts/
```

## Como colaborar

Frankie se publica como repositorio público con finalidad documental, educativa y de portfolio técnico. Su contenido puede consultarse públicamente, pero el proyecto no funciona actualmente como una comunidad abierta de desarrollo.

No se aceptan contribuciones externas no solicitadas por defecto. Las issues, pull requests, propuestas de cambios o solicitudes externas podrán cerrarse sin revisión si no han sido solicitadas expresamente por el propietario del repositorio.

La gestión del roadmap, cambios, versiones, releases y prioridades corresponde exclusivamente al propietario del repositorio. Las normas completas están descritas en [CONTRIBUTING.md](CONTRIBUTING.md).

## Licencia

Licencia pendiente de definir. Ver [LICENSE_PLACEHOLDER.md](LICENSE_PLACEHOLDER.md).

## Capturas

Pendiente de incorporar:

- Vista general de Proxmox.
- Estado de VMs.
- Portainer.
- n8n.
- Recursos Samba desde cliente.
- Dashboard futuro.

## Versiones

El proyecto seguirá Semantic Versioning.

Versión inicial de fundación:

```text
v0.5.0 Foundation
```

Primera release estable:

```text
v0.6.0 Frankie Core / CLI Foundation
```

Versión estable publicada:

```text
v0.7.0
```

Versión actual de desarrollo:

```text
v0.8.0-dev
```

El ciclo actual añade datos estructurados sin abandonar el modo seguro. Están disponibles:

```bash
python -m frankie status --json
python -m frankie audit --json
python -m frankie audit --verbose --json
python -m frankie inventory --json
python -m frankie doctor --json
python -m frankie evidence list
python -m frankie evidence validate
python -m frankie evidence show samba-validation-current --json
```

La salida JSON usa las mismas evidencias documentadas que la consola. No existe conexión live con Frankie físico ni modo repair.

Doctor también incorpora un diagnóstico pedagógico: explica impacto, urgencia, por qué importa, siguiente acción segura y qué no debe hacerse. Continúa siendo offline y no repara sistemas.

La referencia completa de comandos está en [docs/frankie-core/cli.md](docs/frankie-core/cli.md).

Ver [governance/VERSIONING.md](governance/VERSIONING.md).

## Autor

Proyecto mantenido por Gotzon Valcarcel con asistencia técnica de IA.

## Historial del proyecto

Frankie nace como una implantación real de servidor de aula y evoluciona hacia una plataforma reutilizable para laboratorios docentes Linux.

Hitos iniciales:

- documentación del servidor,
- separación en VMs de servicios y recursos,
- plantillas de despliegue,
- automatizaciones con dry-run,
- auditorías de solo lectura,
- preparación de estructura de producto.
