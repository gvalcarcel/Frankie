# Frankie Inventory

## Propósito

`python -m frankie inventory` muestra un inventario resumido de la infraestructura conocida de Frankie.

El comando transforma documentación, knowledge base y evidencias locales del repositorio en una vista consultable por consola. Su objetivo no es descubrir la infraestructura en tiempo real, sino explicar qué compone Frankie según la información documentada.

## Diferencia entre `status` e `inventory`

`status` responde a:

```text
¿Cómo está Frankie según la información disponible?
```

`inventory` responde a:

```text
¿Qué compone Frankie según la información disponible?
```

Por tanto:

- `status` resume estados operativos.
- `inventory` enumera componentes conocidos.
- Ambos son comandos de solo lectura.
- Ninguno consulta servidores reales en esta fase.

## Conceptos diferenciados

El MVP diferencia tres ideas que no deben mezclarse:

- Frankie: servidor físico del aula.
- Frankie Core: herramienta software de solo lectura.
- Repositorio Frankie: documentación, scripts, evidencias y código fuente.

Esta separación es importante para que el alumnado entienda la diferencia entre infraestructura física, software de gestión y fuente de verdad documental.

## Fuentes leídas

El comando usa como fuentes de solo lectura:

- `knowledge/SERVIDORES.md`
- `knowledge/SERVICIOS.md`
- `knowledge/DOCKER.md`
- `knowledge/SAMBA.md`
- `knowledge/BACKUPS.md`
- `knowledge/RED.md`
- `docs/arquitectura.md`
- `docs/DOC-SRV-001_Servidor_Aula_n8n.md`
- `docs/evidencias/paso-5-auditorias/auditoria_srv-servicios.txt`
- `docs/evidencias/paso-5-auditorias/auditoria_srv-recursos.txt`
- `docs/evidencias/paso-5-auditorias/informe_auditoria.md`
- `docs/evidencias/paso-7-mantenimiento/informe_mantenimiento_2026-06-26.md`
- `samba/smb.conf.example`
- `samba/estructura-recursos.example.txt`

Si una fuente falta, el comando no debe fallar. Debe marcar la información como parcial, desconocida o sin evidencia.

## Qué muestra

El inventario mínimo incluye:

- Servidor físico Frankie.
- Hipervisor Proxmox.
- VM100 `srv-servicios`.
- VM101 `srv-recursos`.
- Servicios conocidos de Docker.
- Red Docker `aula-network`.
- Servidor de recursos Samba.
- Ruta `/srv/recursos`.
- Comparticiones documentadas.
- Elementos de seguridad.
- Evidencia de backups de `srv-servicios` y `srv-recursos`.
- Evidencias disponibles.

## Qué no hace

`inventory` no realiza ninguna de estas acciones:

- No modifica servidores.
- No ejecuta scripts.
- No instala paquetes.
- No reinicia servicios.
- No borra archivos.
- No escribe ficheros.
- No se conecta por SSH.
- No lee `.env`.
- No usa credenciales.
- No consulta Internet.
- No accede a la API de GitHub.

## Estados de inventario

El inventario puede usar estos estados cuando un dato no está totalmente respaldado:

- `KNOWN`: dato documentado o inferido claramente desde evidencias.
- `UNKNOWN`: no hay información suficiente.
- `PARTIAL`: hay información incompleta.
- `PENDING`: elemento planificado pero pendiente.
- `MISSING EVIDENCE`: falta una fuente esperada.

## Ejemplo de uso

Desde la raíz del repositorio:

```bash
python -m frankie inventory
```

Salida orientativa:

```text
Frankie Inventory
Version: 0.7.0-dev
Mode: read-only foundation

Physical server:
  Name.......................... Frankie
  Role.......................... Educational physical server
  Hypervisor.................... Proxmox
  Purpose....................... Educational lab infrastructure

Frankie Core:
  Role.......................... Read-only software tool
  Purpose....................... Consult, audit, inventory and document known infrastructure
  Repository.................... Documentation, scripts, evidence and source code

Virtual machines:
  VM100......................... srv-servicios
  VM100 role.................... Services server
  VM100 known services.......... Docker, Portainer, PostgreSQL, n8n, backups, UFW, Fail2ban
  VM101......................... srv-recursos
  VM101 role.................... Resources server
  VM101 known services.......... Samba, shared classroom resources, alumnado/profesorado access model
```

## Limitaciones del MVP

- No es inventario en vivo.
- No detecta hardware automáticamente.
- No consulta Proxmox.
- No consulta Docker.
- No consulta Samba.
- No valida IPs reales.
- No calcula cambios entre auditorías.
- La detección se basa en textos documentados y evidencias locales.

## Uso pedagógico

Este comando puede utilizarse en clase para explicar:

- La diferencia entre servidor físico, hipervisor y máquina virtual.
- La función de una VM de servicios y una VM de recursos.
- El papel de Docker, Portainer, PostgreSQL, n8n y Samba.
- La importancia de documentar una infraestructura real.
- Cómo una herramienta puede convertir documentación técnica en información consultable.
- Por qué una fuente de verdad documental ayuda a administrar sistemas con orden.

## Próximos pasos

- Añadir salida JSON cuando sea necesario integrarlo con otras herramientas.
- Normalizar evidencias en un formato estructurado.
- Separar reglas de detección en una capa declarativa.
- Preparar inventario detallado por componente.
- Conectar el inventario con futuras vistas de dashboard, manteniendo el modo seguro.
