# Frankie CLI - Diseño técnico

## Versión objetivo

`v0.6.0 - Frankie CLI Foundation`

## Objetivo

Diseñar la primera versión de `frankie`, una herramienta de línea de comandos para consultar, auditar e inventariar la infraestructura Frankie.

La primera versión debe ser estrictamente de solo lectura. Su finalidad es ofrecer una interfaz coherente para consultar estado, inventario y auditorías sin modificar los servidores ni sustituir todavía los scripts existentes.

## Principios de diseño

- Solo lectura por defecto y por diseño.
- Sin instalación de paquetes.
- Sin reinicio de servicios.
- Sin borrado de archivos.
- Sin escritura fuera de rutas explícitas de salida solicitadas por el usuario.
- Sin secretos, tokens ni credenciales embebidas.
- Compatible con Ubuntu Server.
- Integrada con la documentación del repositorio.
- Preparada para crecer hacia monitorización, reporting y asistencia IA.
- Reutilización de scripts existentes cuando sea razonable.

## Lenguaje propuesto

### Elección recomendada: Python

Python es la opción recomendada para `Frankie CLI Foundation`.

### Justificación

Python ofrece el mejor equilibrio para esta fase:

- Está disponible de forma habitual en Ubuntu Server.
- Permite crear una CLI mantenible sin compilar binarios.
- Facilita salidas en texto, JSON y Markdown.
- Permite leer ficheros del repositorio, ejecutar comprobaciones de solo lectura y componer informes.
- Es más mantenible que Bash para una CLI que crecerá en comandos, formatos y validaciones.
- Es más accesible para un contexto educativo que Go en una primera versión.
- Permite test unitarios sencillos con `pytest` en fases futuras.

### Alternativas consideradas

#### Bash

Ventajas:

- Encaja con los scripts existentes.
- No requiere dependencias adicionales.
- Es directo para comandos del sistema.

Limitaciones:

- Difícil de escalar con estructura modular.
- Manejo más frágil de errores, formatos y parsing.
- Tests menos cómodos.

Uso recomendado:

- Mantener Bash para scripts de auditoría ya existentes.
- Reutilizarlos desde la CLI cuando proceda.

#### Go

Ventajas:

- Binario único.
- Muy robusto para CLI.
- Buen rendimiento.

Limitaciones:

- Requiere toolchain o pipeline de builds.
- Añade más complejidad inicial.
- Menos inmediato para iteración educativa temprana.

Uso recomendado:

- Valorar Go si Frankie CLI evoluciona hacia distribución binaria estable.

## Estructura propuesta del repositorio

```text
Frankie/
├── cli/
│   ├── README.md
│   ├── frankie/
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── app.py
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── version.py
│   │   │   ├── status.py
│   │   │   ├── inventory.py
│   │   │   ├── audit.py
│   │   │   └── help.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── output.py
│   │   │   ├── paths.py
│   │   │   └── runner.py
│   │   └── integrations/
│   │       ├── __init__.py
│   │       ├── audit_scripts.py
│   │       ├── docs.py
│   │       └── inventory.py
│   ├── tests/
│   │   ├── test_version.py
│   │   ├── test_output.py
│   │   └── test_no_write_mode.py
│   └── pyproject.toml
├── docs/
│   └── frankie-cli/
│       └── design.md
└── checklists/
    └── validacion_frankie_cli.md
```

Esta estructura queda propuesta para una fase posterior. En este paso no se debe crear código funcional.

## Comandos iniciales

### `frankie version`

Objetivo: mostrar la versión de Frankie CLI y el estado de compatibilidad con el repositorio.

Debe hacer:

- Mostrar versión de la CLI.
- Mostrar versión objetivo del proyecto si está definida.
- Mostrar ruta del repositorio detectada, si aplica.
- Indicar que la CLI está en modo solo lectura.

No debe hacer:

- Consultar servidores.
- Escribir archivos.
- Comprobar actualizaciones externas.
- Modificar configuración.

Salida esperada:

```text
Frankie CLI 0.6.0
Project: Frankie
Mode: read-only
Repository: detected
```

### `frankie status`

Objetivo: mostrar un resumen rápido del estado conocido de la infraestructura.

Debe hacer:

- Leer información local del repositorio y evidencias disponibles.
- Mostrar estado resumido de `srv-servicios` y `srv-recursos` basado en la última evidencia disponible.
- Indicar fecha de la última auditoría o mantenimiento documentado.
- Avisar si la información está desactualizada.

No debe hacer:

- Conectarse por SSH en la primera versión, salvo opción futura explícita.
- Ejecutar cambios remotos.
- Reiniciar servicios.
- Actualizar paquetes.

### `frankie inventory`

Objetivo: mostrar el inventario documentado de la infraestructura Frankie.

Debe hacer:

- Leer inventario desde `knowledge/`, `docs/arquitectura.md` y evidencias publicables.
- Mostrar VMs, servicios principales y componentes asociados.
- Permitir salida en texto y JSON.

No debe hacer:

- Escanear redes.
- Descubrir hosts automáticamente.
- Consultar credenciales.
- Modificar documentación.

### `frankie audit`

Objetivo: unificar la ejecución o lectura de auditorías de solo lectura.

Debe hacer:

- Mostrar instrucciones para ejecutar scripts existentes.
- Opcionalmente, invocar scripts de `scripts/auditoria/` si se ejecuta localmente en la VM correcta.
- Capturar salida solo si el usuario indica una ruta de salida.
- Marcar claramente que la auditoría es de solo lectura.

No debe hacer:

- Instalar dependencias.
- Elevar privilegios de forma oculta.
- Usar contraseñas.
- Cambiar servicios.
- Corregir desviaciones automáticamente.

Scripts reutilizables:

- `scripts/auditoria/auditar_srv-servicios.sh`
- `scripts/auditoria/auditar_srv-recursos.sh`

Regla:

- Los scripts siguen siendo la fuente operativa de auditoría.
- La CLI no debe duplicar toda su lógica en `v0.6.0`.
- La CLI debe explicar cuándo conviene ejecutarlos con `sudo`.

### `frankie help`

Objetivo: mostrar ayuda breve, comandos disponibles y enlaces documentales relevantes.

Debe hacer:

- Listar comandos.
- Explicar el modo solo lectura.
- Indicar documentación relacionada.

No debe hacer:

- Ejecutar validaciones.
- Leer información sensible.
- Modificar archivos.

## Formatos de salida

### Consola

Formato por defecto:

- Texto claro.
- Secciones cortas.
- Estados legibles: `OK`, `WARNING`, `ERROR`, `UNKNOWN`.
- Sin colores obligatorios para mantener compatibilidad con terminales básicos.

Ejemplo:

```text
srv-servicios  OK       latest evidence found
srv-recursos   WARNING  SMB client validation pending
```

### JSON

Formato opcional para automatización futura:

```bash
frankie status --format json
```

### Markdown

Formato opcional para informes:

```bash
frankie audit --format markdown --output informe.md
```

Reglas:

- Solo escribir si el usuario especifica `--output`.
- No sobrescribir sin confirmación o sin una opción explícita futura.
- No guardar evidencias sensibles en el repositorio público.

## Integración con documentación existente

### `docs/`

La CLI debe enlazar y consumir documentación operativa:

- `docs/arquitectura.md`
- `docs/validacion_scripts.md`
- `docs/mantenimiento_servidor.md`
- `docs/evidencias/`

### `knowledge/`

La CLI debe tratar `knowledge/` como base de conocimiento inventariable:

- `SERVIDORES.md`
- `SERVICIOS.md`
- `DOCKER.md`
- `SAMBA.md`
- `BACKUPS.md`
- `RED.md`
- `INCIDENCIAS.md`
- `DECISIONES.md`

### `checklists/`

La CLI debe apuntar a checklists relevantes:

- `validacion_srv-servicios.md`
- `validacion_srv-recursos.md`
- `validacion_scripts_srv-servicios.md`
- `validacion_scripts_srv-recursos.md`
- `mantenimiento_servidor.md`

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Que la CLI parezca una herramienta de ejecución remota | Alto | Mensajes explícitos de solo lectura |
| Que se duplique lógica de auditoría existente | Medio | Reutilizar scripts existentes |
| Que se documenten evidencias sensibles | Alto | Salidas a fichero controladas y advertencias |
| Que se vuelva dependiente de rutas rígidas | Medio | Centralizar rutas |
| Que crezca sin arquitectura | Medio | Separar comandos, core e integraciones |
| Que requiera dependencias no disponibles | Medio | Mantener librería estándar en `v0.6.0` |

## Pruebas mínimas

- `frankie version` muestra versión y modo solo lectura.
- `frankie help` lista todos los comandos iniciales.
- `frankie inventory` funciona sin servidores accesibles.
- `frankie status` informa si no hay evidencias.
- `frankie status` detecta última evidencia documentada.
- `frankie audit` no ejecuta cambios.
- La CLI no escribe archivos salvo que exista `--output`.
- La salida JSON es válida.
- La salida Markdown es válida.
- La ejecución sin argumentos muestra ayuda.

## Criterios de finalización de v0.6.0

`v0.6.0 - Frankie CLI Foundation` se considerará completada cuando:

- Exista estructura `cli/` documentada.
- Exista comando instalable o ejecutable `frankie`.
- Funcionen los comandos:
  - `frankie version`
  - `frankie status`
  - `frankie inventory`
  - `frankie audit`
  - `frankie help`
- Todos los comandos sean de solo lectura.
- No haya secretos ni credenciales en código, tests o documentación.
- La CLI pueda ejecutarse en Ubuntu Server.
- Existan pruebas mínimas.
- La documentación de uso esté creada.
- `ROADMAP.md` refleje el alcance de `v0.6.0`.
- `CHANGELOG.md` tenga entrada `Unreleased` sin declarar release final.

## Decisión arquitectónica

La primera versión de Frankie CLI debe implementarse en Python, usando únicamente librería estándar siempre que sea posible.

Bash queda reservado para scripts de auditoría y mantenimiento ya existentes.

Go queda como opción futura si el proyecto necesita distribución binaria estable.
