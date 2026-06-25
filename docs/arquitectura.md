# Arquitectura

## Vista general

```text
Servidor fisico
└── Proxmox VE - srv-aula113
    ├── VM 100 - srv-servicios / frankie
    │   ├── Docker
    │   ├── Portainer
    │   ├── PostgreSQL
    │   └── n8n
    └── VM 101 - srv-recursos
        └── Samba / recursos docentes
```

## Host Proxmox

- Nodo: `srv-aula113`.
- Almacenamiento: ZFS mirror.
- Estado: pendiente de documentacion completa.

## VM srv-servicios

- Funcion: servicios de automatizacion.
- Servicios principales:
  - Docker.
  - Portainer.
  - PostgreSQL.
  - n8n.

## VM srv-recursos

- Funcion: recursos docentes compartidos.
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
