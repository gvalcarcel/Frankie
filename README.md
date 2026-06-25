# Frankie

Frankie es una plataforma para administrar, desplegar, documentar, auditar y monitorizar infraestructuras Linux destinadas a laboratorios docentes.

El proyecto no es solo un servidor ni una coleccion de scripts. Frankie debe funcionar como una plataforma mantenible, versionada y preparada para crecer durante anos como producto software.

## Origin and Purpose

> "No eras el más bonito y te tuvimos que hacer con un megamix de piezas, pero naciste siendo leyenda".

Frankie nace como servidor educativo dentro del Grado Básico en Informática y Comunicaciones del Centro de Formación Somorrostro.

Su origen es humilde y muy real: una máquina construida con recursos hardware limitados, reutilizando componentes tomados de distintos equipos y aprovechando lo que estaba disponible en el centro. Esa limitación no es una debilidad; forma parte de su valor didáctico. Frankie representa una idea muy importante en informática: con criterio técnico, documentación, orden y ganas de aprender, incluso una infraestructura modesta puede convertirse en una plataforma poderosa.

El propósito de Frankie es ambicioso: convertirse en una plataforma real de aprendizaje, automatización, documentación, auditoría y servicios de aula. No se trata únicamente de levantar servicios, sino de construir un entorno donde el alumnado pueda experimentar con redes, servidores, automatización, recursos compartidos, buenas prácticas DevOps y administración de sistemas.

El objetivo principal es ofrecer al alumnado de Grado Básico una infraestructura potente, realista y motivadora. Frankie busca que estos alumnos adquieran competencias técnicas sólidas, ganen confianza y se sientan capaces de trabajar de tú a tú con alumnado de Grado Medio y Grado Superior.

Frankie es, por tanto, una herramienta técnica y también una declaración educativa: aprender haciendo, documentar lo aprendido y demostrar que la calidad profesional no depende solo del hardware disponible, sino de cómo se piensa, se cuida y se evoluciona un proyecto.

## Descripcion del proyecto

Frankie centraliza conocimiento, procedimientos, plantillas, auditorias, checklists y automatizaciones controladas para infraestructuras Linux de aula.

El repositorio actua como Single Source of Truth del proyecto:

- documentacion tecnica,
- decisiones de arquitectura,
- plantillas de configuracion,
- scripts revisables,
- evidencias de auditoria,
- checklists operativos,
- futura monitorizacion,
- futura capa de asistencia con IA.

## Objetivos

- Mantener documentada la infraestructura de laboratorio.
- Facilitar despliegues repetibles y auditables.
- Separar configuraciones reales de plantillas versionables.
- Evitar inclusion de secretos en Git.
- Preparar automatizaciones idempotentes y seguras.
- Permitir validaciones previas con dry-run.
- Construir una base de conocimiento reutilizable.
- Evolucionar hacia monitorizacion, dashboard y autocuracion.

## Arquitectura general

La arquitectura actual documentada se organiza alrededor de:

```text
Frankie
├── governance      Politicas, vision y reglas del proyecto
├── knowledge       Base de conocimiento operativa
├── docs            Documentacion tecnica y evidencias
├── scripts         Automatizaciones y auditorias
├── docker          Plantillas Docker Compose
├── samba           Plantillas Samba
├── monitor         Futuro sistema de monitorizacion
├── ai              Futuras capacidades de asistencia IA
├── backups         Plantillas de backup
├── checklists      Validaciones operativas
└── env             Plantillas de variables de entorno
```

Infraestructura de referencia actualmente documentada:

| Capa | Nombre | Funcion |
|---|---|---|
| Host fisico | `srv-aula113` | Proxmox VE, almacenamiento ZFS y gestion de VMs |
| VM 100 | `srv-servicios` / `frankie` | Docker, Portainer, PostgreSQL y n8n |
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

Estado de producto: `v0.5.0 Foundation`.

El repositorio contiene:

- estructura inicial de plataforma,
- documentacion base,
- plantillas Docker/Samba/env/backups,
- scripts idempotentes con dry-run,
- scripts de auditoria de solo lectura,
- evidencias de auditoria inicial,
- checklists de validacion.

Pendientes destacados:

- validacion SMB desde cliente real,
- reservas DHCP o estrategia de nombres estable,
- prueba formal de restauracion,
- definicion de monitorizacion,
- preparacion de dashboard,
- consolidacion de knowledge base.

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
└── .github/
```

## Como colaborar

Frankie se publica como repositorio publico con finalidad documental, educativa y de portfolio tecnico. Su contenido puede consultarse publicamente, pero el proyecto no funciona actualmente como una comunidad abierta de desarrollo.

No se aceptan contribuciones externas no solicitadas por defecto. Las issues, pull requests, propuestas de cambios o solicitudes externas podran cerrarse sin revision si no han sido solicitadas expresamente por el propietario del repositorio.

La gestion del roadmap, cambios, versiones, releases y prioridades corresponde exclusivamente al propietario del repositorio. Las normas completas estan descritas en [CONTRIBUTING.md](CONTRIBUTING.md).

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

El proyecto seguira Semantic Versioning.

Version inicial de fundacion:

```text
v0.5.0 Foundation
```

Ver [governance/VERSIONING.md](governance/VERSIONING.md).

## Autor

Proyecto mantenido por Gotzon Valcarcel con asistencia tecnica de IA.

## Historial del proyecto

Frankie nace como una implantacion real de servidor de aula y evoluciona hacia una plataforma reutilizable para laboratorios docentes Linux.

Hitos iniciales:

- documentacion del servidor,
- separacion en VMs de servicios y recursos,
- plantillas de despliegue,
- automatizaciones con dry-run,
- auditorias de solo lectura,
- preparacion de estructura de producto.
