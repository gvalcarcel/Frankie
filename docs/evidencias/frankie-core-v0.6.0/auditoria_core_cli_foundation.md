# Auditoría Frankie Core / CLI Foundation

## Fecha de auditoría

2026-06-26

## Alcance revisado

Se ha revisado la implementación local de `Frankie Core / CLI Foundation v0.6.0-dev`.

Elementos revisados:

- `frankie/`
- `frankie/__main__.py`
- `frankie/app.py`
- `frankie/cli/parser.py`
- `frankie/commands/`
- `frankie/core/`
- `frankie/services/`
- `frankie/inventory/`
- `frankie/knowledge/`
- `frankie/output/`
- `frankie/utils/`
- `tests/`
- `pyproject.toml`
- `docs/frankie-core/README.md`
- `docs/frankie-cli/design.md`
- `ROADMAP.md`
- `CHANGELOG.md`

No se han revisado servidores reales ni se han ejecutado scripts de producción.

## Resumen ejecutivo

La implementación cumple el objetivo principal de la foundation:

- Existe paquete raíz `frankie/`.
- La versión está centralizada en `frankie/core/constants.py`.
- La versión declarada es `0.6.0-dev`.
- El modo declarado es `read-only foundation`.
- `python -m frankie`, `version` y `help` funcionan.
- `status`, `inventory`, `audit` y `doctor` devuelven mensaje claro de no implementado.
- No se detectan operaciones de escritura, borrado, conexión SSH, uso de credenciales, acceso externo ni ejecución de scripts en el paquete `frankie/`.
- `utils/safe_subprocess.py` está correctamente documentado como placeholder y no expone helper de ejecución.
- Los tests pasan correctamente.

Decisión final:

```text
apto para cierre de tarea
```

Con recomendaciones menores para una tarea futura.

## Tabla de validaciones

| Validación | Resultado | Observación |
|---|---|---|
| Paquete raíz `frankie/` existe | OK | Estructura creada según decisión arquitectónica |
| `frankie/__main__.py` existe | OK | Permite `python -m frankie` |
| `frankie/app.py` existe | OK | Enrutamiento simple de comandos |
| `frankie/cli/parser.py` existe | OK | Usa `argparse` |
| `frankie/commands/` existe | OK | Incluye `version`, `help`, `status`, `inventory`, `audit`, `doctor` |
| `frankie/core/` existe | OK | Incluye constantes, config y paths |
| `frankie/services/` existe | OK | Placeholders documentados |
| `frankie/inventory/` existe | OK | Placeholder documentado |
| `frankie/knowledge/` existe | OK | Placeholder documentado |
| `frankie/output/` existe | OK | Placeholders para futuras salidas |
| `frankie/utils/` existe | OK | Incluye `safe_subprocess.py` sin ejecución |
| `tests/` existe | OK | Tests básicos de foundation |
| `pyproject.toml` existe | OK | Define paquete `frankie-core` y entrypoint `frankie` |
| Versión centralizada | OK | `frankie/core/constants.py` |
| Versión `0.6.0-dev` | OK | Constante `VERSION` correcta |
| Modo `read-only foundation` | OK | Constante `MODE` correcta |
| Comandos futuros no implementados | OK | Devuelven mensaje claro |
| Sin operaciones peligrosas en paquete | OK | No se detectan escrituras, borrados, SSH ni subprocess reales |
| Tests | OK | `Ran 7 tests ... OK` |
| Documentación Core | OK | Explica Core, CLI, comandos y garantías |
| Documentación CLI | OK con observación | Incluye nota arquitectónica, pero conserva estructura antigua como antecedente |
| Release v0.6.0 no declarada final | OK | `CHANGELOG.md` mantiene cambios en `Unreleased` |

## Resultados de comandos

### `python -m frankie`

Resultado:

```text
Frankie Core 0.6.0-dev

Frankie Core is the foundation package for the Frankie platform.
The CLI is one interface inside the core, not the whole project.

Mode: read-only foundation
This version does not modify servers or services.

Available commands:
  frankie version
  frankie help

Planned commands:
  frankie status
  frankie inventory
  frankie audit
  frankie doctor

This foundation version does not modify servers, services, files, or configurations.
```

Código de salida: `0`.

### `python -m frankie version`

Resultado:

```text
Frankie Core 0.6.0-dev
Mode: read-only foundation
Project: Frankie
This version does not modify servers or services.
```

Código de salida: `0`.

### `python -m frankie help`

Resultado:

```text
Frankie Core 0.6.0-dev

Frankie Core is the foundation package for the Frankie platform.
The CLI is one interface inside the core, not the whole project.

Mode: read-only foundation
This version does not modify servers or services.

Available commands:
  frankie version
  frankie help

Planned commands:
  frankie status
  frankie inventory
  frankie audit
  frankie doctor

This foundation version does not modify servers, services, files, or configurations.
```

Código de salida: `0`.

### `python -m frankie status`

Resultado:

```text
Command 'status' is not implemented yet in v0.6.0 foundation.
This command is planned for a future iteration.
```

Código de salida: `0`.

### `python -m frankie inventory`

Resultado:

```text
Command 'inventory' is not implemented yet in v0.6.0 foundation.
This command is planned for a future iteration.
```

Código de salida: `0`.

### `python -m frankie audit`

Resultado:

```text
Command 'audit' is not implemented yet in v0.6.0 foundation.
This command is planned for a future iteration.
```

Código de salida: `0`.

### `python -m frankie doctor`

Resultado:

```text
Command 'doctor' is not implemented yet in v0.6.0 foundation.
This command is planned for a future iteration.
```

Código de salida: `0`.

### Comando desconocido

Comando ejecutado:

```bash
python -m frankie unknown
```

Resultado:

```text
Unknown command: unknown
Run 'frankie help' to see available commands.
```

Código de salida: `2`.

## Resultado de tests

Comando ejecutado:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 7 tests in 0.552s

OK
```

## Resultado de compilación

Comando ejecutado:

```bash
python -m compileall frankie
```

Resultado:

```text
OK
```

Todos los módulos del paquete `frankie/` compilan correctamente.

## Revisión de seguridad y solo lectura

Se buscaron patrones asociados a:

- apertura de ficheros en modo escritura,
- borrado de archivos,
- modificación de configuración,
- ejecución de comandos del sistema,
- llamadas a scripts de producción,
- conexiones SSH,
- uso de credenciales,
- acceso a servicios externos.

Resultado:

- No se detectan operaciones peligrosas en `frankie/`.
- `subprocess` aparece solo en tests para ejecutar `python -m frankie` localmente.
- `safe_subprocess.py` no ejecuta comandos; está documentado como placeholder.
- No se detectan secretos, IPs internas ni credenciales en la implementación de Frankie Core.

## Riesgos detectados

### R-001 - Convivencia con implementación anterior en `cli/`

Clasificación: menor.

Existe una implementación previa en `cli/` con su propio paquete `cli/frankie/`.

Impacto:

- Puede generar confusión sobre cuál es la CLI oficial.
- Puede provocar diferencias de comportamiento si se ejecuta desde `cli/` en lugar de desde la raíz del repositorio.

Evaluación:

- Puede convivir temporalmente porque no se ha eliminado ni modificado.
- La nueva dirección arquitectónica está documentada en `docs/frankie-cli/design.md` y `docs/frankie-core/README.md`.

Recomendación:

- En una tarea futura, decidir si `cli/` debe migrarse, archivarse bajo documentación histórica o eliminarse tras consolidar `frankie/`.

### R-002 - `docs/frankie-cli/design.md` conserva estructura antigua

Clasificación: menor.

El documento contiene una nota arquitectónica nueva que corrige la dirección del proyecto, pero conserva más abajo la propuesta inicial basada en `cli/`.

Impacto:

- Puede confundir a lectores nuevos si no leen la nota inicial.

Recomendación:

- En una tarea documental posterior, reescribir el documento para separar claramente:
  - diseño histórico de CLI,
  - decisión vigente de Frankie Core,
  - arquitectura actual.

### R-003 - Artefactos `__pycache__` locales ignorados

Clasificación: menor.

La ejecución de tests y `compileall` generó directorios `__pycache__` ignorados por Git.

Impacto:

- No afecta al repositorio si `.gitignore` se respeta.

Recomendación:

- Limpiarlos antes de empaquetar o revisar commits si se desea un árbol local más limpio.

## Desviaciones

| Desviación | Severidad | Estado |
|---|---|---|
| Existe implementación previa en `cli/` | Menor | Aceptable temporalmente |
| Diseño CLI conserva estructura antigua | Menor | Mitigado por nota arquitectónica |
| `pyproject.toml` usa versión PEP 440 `0.6.0.dev0`, mientras la constante visible usa `0.6.0-dev` | Menor | Aceptable; conviene documentarlo si se empaqueta |

## Recomendaciones

1. Mantener la implementación actual como base de `Frankie Core`.
2. No implementar `status`, `inventory`, `audit` ni `doctor` hasta cerrar la auditoría de arquitectura.
3. Crear una tarea específica para resolver el destino de `cli/`.
4. Crear una tarea documental para limpiar o reorganizar `docs/frankie-cli/design.md`.
5. Antes de cerrar `v0.6.0`, decidir si se mantiene la doble notación de versión:
   - `0.6.0-dev` visible para usuarios.
   - `0.6.0.dev0` en `pyproject.toml`.
6. Mantener tests de solo lectura como barrera obligatoria para futuras ampliaciones.

## Decisión final

```text
apto para cierre de tarea
```

La foundation cumple el alcance solicitado y no presenta riesgos críticos ni importantes.

No se declara la release `v0.6.0` como final.
