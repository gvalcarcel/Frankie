# Frankie Inventory MVP - Auditoría inicial

## Datos de auditoría

- Work Order: WO-0003
- Componente auditado: `python -m frankie inventory`
- Versión objetivo: `0.6.0-dev`
- Fecha: 2026-06-26
- Tipo de revisión: auditoría local de implementación MVP.
- Decisión final provisional: listo para auditoría externa.

## Alcance

Esta auditoría cubre la implementación inicial del comando:

```bash
python -m frankie inventory
```

El alcance incluye:

- ejecución local del comando;
- revisión de salida por consola;
- revisión de separación arquitectónica;
- revisión de modo solo lectura;
- pruebas automatizadas con `unittest`;
- compilación del paquete Python;
- documentación asociada.

No se han revisado servidores reales, servicios en producción, conexiones SSH, Proxmox, Docker, Samba ni backups en vivo.

## Arquitectura revisada

El flujo implementado es:

```text
frankie.commands.inventory.run()
        |
        v
frankie.inventory.inventory_reader.build_inventory_report()
        |
        v
frankie.core.models.InventoryReport
        |
        v
frankie.output.console.render_inventory()
```

La lógica no queda concentrada en `commands/inventory.py`. El comando actúa como capa fina y delega en el lector de inventario y en el renderizador de consola.

## Fuentes de datos

El MVP lee únicamente fuentes locales del repositorio:

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
- `samba/smb.conf.example`
- `samba/estructura-recursos.example.txt`

Si una fuente falta, el comando conserva la ejecución y refleja estados como `UNKNOWN`, `PARTIAL` o `MISSING EVIDENCE`.

## Confirmación de solo lectura

La implementación revisada:

- no modifica servidores;
- no ejecuta scripts;
- no instala paquetes;
- no reinicia servicios;
- no borra archivos;
- no escribe ficheros;
- no usa SSH;
- no lee `.env`;
- no usa credenciales;
- no consulta Internet;
- no accede a GitHub API;
- no ejecuta comandos externos.

La búsqueda estática local no detecta operaciones incompatibles con el modo solo lectura en el flujo de `inventory`.

## Confirmación conceptual

El comando diferencia explícitamente:

- Frankie: servidor físico educativo.
- Frankie Core: herramienta software de solo lectura.
- Repositorio Frankie: documentación, scripts, evidencias y código fuente.

Esta separación cumple el objetivo pedagógico de la Work Order y evita tratar el servidor físico como si fuera una VM o como si fuera el propio software.

## Comandos ejecutados

```bash
python -m frankie inventory
python -m frankie status
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

## Resultados

- `python -m frankie inventory`: correcto.
- `python -m frankie status`: correcto.
- `python -m frankie version`: correcto.
- `python -m frankie help`: correcto.
- `python -m unittest discover -s tests`: `Ran 17 tests ... OK`.
- `python -m compileall frankie`: correcto.

## Salida verificada

La salida de `python -m frankie inventory` incluye:

- `Frankie Inventory`.
- `0.6.0-dev`.
- `read-only foundation`.
- `Physical server`.
- `Frankie`.
- `Frankie Core`.
- `srv-servicios`.
- `srv-recursos`.
- `Docker`.
- `Samba`.
- `aula-network`.
- `/srv/recursos`.
- `not exposed on host port 5432`.
- `Live connection................ no`.

## Tests añadidos

Se añadió cobertura para:

- ejecución correcta del comando;
- cabecera y versión;
- modo de solo lectura;
- diferenciación entre servidor físico, Frankie Core y repositorio;
- presencia de VMs y servicios conocidos;
- presencia de `aula-network`;
- tolerancia ante evidencias faltantes;
- ausencia de operaciones de escritura o subprocess en el flujo de inventario.

## Riesgos detectados

### Riesgo menor: inventario basado en texto

La detección de evidencias se basa en contenido textual de documentos y evidencias. Es suficiente para el MVP, pero en futuras iteraciones conviene evolucionar hacia evidencias estructuradas.

Clasificación: menor.

### Riesgo menor: datos conocidos parcialmente estáticos

El MVP muestra elementos conocidos de la infraestructura a partir de documentación. No representa un descubrimiento automático ni una consulta en vivo.

Clasificación: menor.

### Mejora futura: formatos de salida

La salida actual es texto por consola. No se implementa todavía `--format json`, para mantener el alcance controlado.

Clasificación: mejora futura.

## Decisión final provisional

listo para auditoría externa

La implementación cumple los criterios de la Work Order para quedar lista para revisión, sin cerrar todavía la Work Order ni declarar release.
