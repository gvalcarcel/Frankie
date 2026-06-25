# Architecture

## Estado

Documento inicial.

## Capas del proyecto

```text
Frankie
├── Governance
├── Knowledge Base
├── Documentation
├── Automation
├── Templates
├── Monitoring
├── AI Assistance
└── Evidence
```

## Principios de arquitectura

- Separar documentación, conocimiento y automatización.
- Evitar acoplar scripts a una única instalación.
- Mantener plantillas sin secretos.
- Diseñar para multiples laboratorios futuros.

## Ejemplo de infraestructura gestionada

```text
Host Proxmox
├── VM servicios
└── VM recursos
```

Este ejemplo no debe limitar la evolucion futura.
