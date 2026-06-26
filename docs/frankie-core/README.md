# Frankie Core

## Qué es Frankie Core

Frankie Core es el núcleo Python del proyecto Frankie.

Su objetivo es proporcionar una base común para futuras capacidades de consulta, inventario, auditoría, monitorización, API, dashboard e integración con IA.

Frankie Core no es todavía una herramienta de administración remota. En `v0.6.0 - Frankie Core / CLI Foundation` solo ofrece una base modular y una CLI mínima de solo lectura.

## Por qué existe el paquete raíz `frankie/`

La decisión arquitectónica actual es construir Frankie como plataforma, no solo como CLI.

Por ese motivo, el paquete principal pasa a ser:

```text
frankie/
```

La CLI será una interfaz dentro del núcleo, junto a otros módulos futuros.

Esta estructura permite crecer hacia:

- CLI.
- Inventario.
- Lectura de knowledge base.
- Servicios de consulta.
- Monitorización.
- API.
- Dashboard.
- Asistencia IA.

## Diferencia entre Frankie Core y Frankie CLI

Frankie Core:

- Es el paquete raíz.
- Contiene constantes, configuración, rutas, servicios, inventario, knowledge, output y utilidades.
- Debe ser reutilizable por futuras interfaces.

Frankie CLI:

- Es una interfaz de línea de comandos dentro de Frankie Core.
- Usa `argparse`.
- En `v0.6.0` solo implementa comandos mínimos.
- No representa toda la plataforma.

## Comandos disponibles en v0.6.0

```bash
python -m frankie
python -m frankie version
python -m frankie help
python -m frankie status
python -m frankie inventory
python -m frankie audit
```

### `status`

El comando `status` es el primer MVP funcional de Frankie Core.

Lee evidencias documentadas en el repositorio y muestra un resumen de estado en modo solo lectura.

Documento específico:

- `docs/frankie-core/status.md`

### `inventory`

El comando `inventory` es el segundo MVP funcional de Frankie Core.

Lee documentación, knowledge base y evidencias locales para mostrar qué compone Frankie: servidor físico, VMs, servicios, recursos compartidos, seguridad, backups y fuentes disponibles.

Documento específico:

- `docs/frankie-core/inventory.md`

### `audit`

El comando `audit` es el tercer MVP funcional de Frankie Core.

Lee evidencias locales del repositorio y ejecuta checks documentales para generar hallazgos con estado, severidad, evidencias y recomendaciones.

Documento específico:

- `docs/frankie-core/audit.md`

## Comandos planificados

Estos comandos existen como placeholder, pero no están implementados todavía:

```bash
python -m frankie doctor
```

Salida esperada:

```text
Command 'doctor' is not implemented yet in v0.6.0 foundation.
This command is planned for a future iteration.
```

## Garantías de solo lectura

La versión `v0.6.0-dev`:

- No modifica servidores.
- No ejecuta scripts existentes.
- No instala paquetes.
- No reinicia servicios.
- No borra archivos.
- No escribe ficheros.
- No se conecta por SSH.
- No usa credenciales.
- No accede a servicios externos.

## Ejecución local

Desde la raíz del repositorio:

```bash
python -m frankie
python -m frankie version
python -m frankie help
python -m frankie status
python -m frankie inventory
python -m frankie audit
```

## Tests

Desde la raíz del repositorio:

```bash
python -m unittest discover -s tests
```

## Estado

Frankie Core está en fase foundation.

No debe considerarse todavía una release funcional completa de inventario, auditoría o monitorización.
