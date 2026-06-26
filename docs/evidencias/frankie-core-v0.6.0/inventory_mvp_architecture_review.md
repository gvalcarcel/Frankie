# Frankie Inventory MVP - Architecture Review

## Fecha de auditoría

2026-06-26

## Alcance revisado

Esta auditoría revisa arquitectónicamente el MVP del comando:

```bash
python -m frankie inventory
```

Archivos revisados:

- `frankie/commands/inventory.py`
- `frankie/inventory/inventory_reader.py`
- `frankie/core/models.py`
- `frankie/core/paths.py`
- `frankie/output/console.py`
- `frankie/commands/help.py`
- `tests/test_inventory.py`
- `tests/test_not_implemented_commands.py`
- `tests/test_read_only_foundation.py`
- `docs/frankie-core/inventory.md`
- `docs/frankie-core/README.md`
- `docs/evidencias/frankie-core-v0.6.0/inventory_mvp_audit.md`
- `CHANGELOG.md`
- `ROADMAP.md`

No se han revisado servidores reales, Proxmox, Docker, Samba, backups en producción ni conexiones SSH.

## Resumen ejecutivo

El comando `inventory` cumple la arquitectura esperada para Frankie Core `0.6.0-dev`.

La implementación mantiene el modo estrictamente solo lectura, no ejecuta comandos externos, no escribe ficheros, no lee credenciales y no consulta servicios reales. El inventario se construye a partir de documentación, knowledge base y evidencias locales del repositorio.

La separación de responsabilidades es correcta para el MVP: el comando actúa como capa fina, el lector de inventario construye el modelo, los modelos viven en `frankie/core/models.py`, las rutas se centralizan en `frankie/core/paths.py` y el renderizado de consola reside en `frankie/output/console.py`.

No se detectan bloqueos arquitectónicos ni riesgos críticos. Las mejoras identificadas son evolutivas y no impiden cerrar WO-0003.

## Tabla de validaciones arquitectónicas

| Área | Resultado | Observación |
| --- | --- | --- |
| Capa de comando | OK | `frankie/commands/inventory.py` solo delega en reader y renderer. |
| Servicio de inventario | OK | `inventory_reader.py` concentra la construcción del inventario. |
| Modelos de datos | OK | Existen `InventoryItem`, `InventorySection` e `InventoryReport`. |
| Renderizado | OK | `render_inventory()` solo presenta el modelo en consola. |
| Rutas | OK | `INVENTORY_SOURCE_PATHS` centraliza las fuentes documentales. |
| Flujo interno | OK | Respeta CLI parser -> command -> reader -> models -> renderer -> texto. |
| Solo lectura | OK | No se detectan operaciones de escritura ni ejecución externa en el flujo. |
| Evidencias faltantes | OK | El comando no rompe y usa estados de inventario. |
| Diferenciación conceptual | OK | Distingue Frankie físico, Frankie Core y repositorio. |
| Relación con `status` | OK | `status` responde estado; `inventory` responde composición. |
| Tests | OK | Cubren ejecución, salida, conceptos, evidencias faltantes y seguridad básica. |
| Documentación | OK | Explica propósito, fuentes, no acciones, limitaciones y uso pedagógico. |

## Validación de solo lectura

Se validó que `inventory`:

- no escribe ficheros;
- no modifica ficheros;
- no borra ficheros;
- no abre ficheros en modo escritura;
- no ejecuta subprocess;
- no lanza scripts Bash;
- no consulta servicios reales;
- no usa SSH;
- no accede a Internet;
- no lee credenciales;
- no lee `.env`;
- no modifica configuración.

La búsqueda estática de patrones sensibles solo detectó una docstring en `frankie/utils/safe_subprocess.py`, fuera del flujo del comando `inventory`.

## Validación de flujo interno

El flujo revisado es:

```text
CLI parser
  -> inventory command
  -> inventory reader/service
  -> inventory models
  -> console renderer
  -> output text
```

`frankie/commands/inventory.py` no contiene lógica de negocio ni rutas documentales. Su responsabilidad queda limitada a invocar:

```python
render_inventory(build_inventory_report())
```

Esta forma es coherente con `status` y permite evolucionar a otros renderizadores sin reescribir el comando.

## Validación de modelos

Los modelos existentes son:

- `InventoryItem`
- `InventorySection`
- `InventoryReport`

El modelo es suficientemente reutilizable para:

- salida JSON futura;
- salida Markdown futura;
- dashboard;
- API;
- módulo IA;
- tests unitarios de reglas de inventario.

`InventoryItem` valida estados permitidos mediante `ALLOWED_INVENTORY_STATES`, lo que reduce errores de representación.

## Validación de diferenciación conceptual

El comando diferencia correctamente:

- Frankie: servidor físico educativo.
- Frankie Core: herramienta software de solo lectura.
- Repositorio Frankie: documentación, scripts, evidencias y código fuente.

Esta distinción aparece en:

- salida de consola;
- tests;
- documentación `docs/frankie-core/inventory.md`;
- auditoría inicial del MVP.

La separación es adecuada para el propósito pedagógico del proyecto.

## Validación de lectura de fuentes

Las fuentes se centralizan en `INVENTORY_SOURCE_PATHS` y se leen mediante `FrankiePaths.read_text()`.

El comando no falla si una fuente no existe. En ese caso conserva la ejecución y refleja información parcial mediante:

- `UNKNOWN`
- `PARTIAL`
- `MISSING EVIDENCE`

La lectura documental no se presenta como descubrimiento en vivo. La salida incluye explícitamente:

```text
Live connection............... no
```

## Validación de relación con `status`

La separación conceptual es correcta:

- `status`: cómo está Frankie según la información disponible.
- `inventory`: qué compone Frankie según la información disponible.

Ambos comparten utilidades razonables:

- modelos en `frankie/core/models.py`;
- rutas en `frankie/core/paths.py`;
- renderizado en `frankie/output/console.py`;
- constantes de versión y modo.

No se detecta duplicación innecesaria que bloquee el cierre del MVP.

## Validación de tests

`tests/test_inventory.py` cubre:

- ejecución exitosa de `inventory`;
- cabecera `Frankie Inventory`;
- versión `0.6.0-dev`;
- modo `read-only foundation`;
- distinción entre Frankie físico, Frankie Core y repositorio;
- presencia de `srv-servicios`;
- presencia de `srv-recursos`;
- presencia de Docker;
- presencia de Samba;
- presencia de `aula-network`;
- comportamiento si faltan evidencias;
- ausencia de subprocess;
- ausencia de escritura en el flujo.

`tests/test_not_implemented_commands.py` se ajustó correctamente para dejar `inventory` fuera de los comandos placeholder.

`tests/test_read_only_foundation.py` mantiene una protección global contra operaciones incompatibles con la foundation de solo lectura.

## Validación de documentación

La documentación revisada explica:

- propósito del comando;
- fuentes leídas;
- qué no hace;
- diferencia entre `status` e `inventory`;
- significado de estados de inventario;
- limitaciones del MVP;
- carácter no tiempo real;
- ausencia de conexión con Frankie físico;
- utilidad pedagógica;
- que `v0.6.0` no está cerrada.

`CHANGELOG.md` y `ROADMAP.md` reflejan `inventory` como parte de `0.6.0-dev`, sin declarar release final.

## Comandos ejecutados

```bash
python -m frankie inventory
python -m frankie status
python -m frankie version
python -m frankie help
python -m unittest discover -s tests
python -m compileall frankie
```

Resultados:

- `python -m frankie inventory`: OK.
- `python -m frankie status`: OK.
- `python -m frankie version`: OK.
- `python -m frankie help`: OK.
- `python -m unittest discover -s tests`: `Ran 17 tests ... OK`.
- `python -m compileall frankie`: OK.

## Riesgos detectados

### Riesgo menor: detección textual

El inventario usa búsquedas textuales sobre documentos y evidencias. Es suficiente para el MVP, pero puede volverse frágil si aumenta el número de fuentes o si cambian mucho los textos.

Clasificación: menor.

### Riesgo menor: reglas de inventario en código

Las reglas de detección están concentradas en `inventory_reader.py`. Para el tamaño actual es razonable, pero en futuras versiones podría convenir moverlas a una capa declarativa o a un esquema de evidencias.

Clasificación: mejora futura.

### Riesgo menor: datos conocidos estáticos

Algunos datos base, como el nombre del servidor físico o los roles de las VMs, se muestran como inventario conocido del proyecto. Esto es coherente con la Work Order, pero debe seguir diferenciándose de descubrimiento automático.

Clasificación: menor.

## Correcciones realizadas

No se realizaron correcciones durante esta auditoría.

No se añadieron funcionalidades nuevas.

## Recomendaciones futuras

- Definir un formato estructurado para evidencias de inventario.
- Añadir salida JSON en una Work Order posterior.
- Preparar tests unitarios más finos sobre estados `KNOWN`, `PARTIAL`, `UNKNOWN` y `MISSING EVIDENCE`.
- Separar reglas de detección en una capa declarativa si crece el número de servicios.
- Mantener el texto pedagógico que diferencia servidor físico, software y repositorio.

## Decisión final

apto para cierre de WO-0003
