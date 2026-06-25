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

- Separar documentacion, conocimiento y automatizacion.
- Evitar acoplar scripts a una unica instalacion.
- Mantener plantillas sin secretos.
- Diseñar para multiples laboratorios futuros.

## Ejemplo de infraestructura gestionada

```text
Host Proxmox
├── VM servicios
└── VM recursos
```

Este ejemplo no debe limitar la evolucion futura.
