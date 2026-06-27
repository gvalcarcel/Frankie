# Arquitectura

## Vista general

```text
Servidor físico - Frankie
└── Proxmox VE - srv-aula113
    ├── VM 100 - srv-servicios
    │   ├── Docker
    │   ├── Portainer
    │   ├── PostgreSQL
    │   └── n8n
    └── VM 101 - srv-recursos
        └── Samba / recursos docentes
```

## Host Proxmox

- Nombre del servidor físico: Frankie.
- Hostname del nodo Proxmox: `srv-aula113`.
- Almacenamiento: ZFS mirror.
- Estado: pendiente de documentación completa.

## VM srv-servicios

- Función: servicios de automatización.
- Servicios principales:
  - Docker.
  - Portainer.
  - PostgreSQL.
  - n8n.

## VM srv-recursos

- Función: recursos docentes compartidos.
- Servicio principal:
  - Samba.
- Estructura prevista:
  - `00_LEEME`
  - `01_INSTALABLES`
  - `02_ISOS`
  - `03_DRIVERS`
  - `04_MATERIAL_CLASE`
  - `05_PLANTILLAS`
  - `06_PRACTICAS`
  - `07_ENTREGAS`
  - `99_PROFESORADO`
