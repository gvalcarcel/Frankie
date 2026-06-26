# Frankie Core v0.6.0 - Release Readiness Review

Fecha de revision: 2026-06-26

Version revisada: `0.6.0-dev`

Decision final: `apto para preparar release v0.6.0`

## 1. Alcance

Esta revision evalua si Frankie Core esta preparado para avanzar hacia una futura release estable `v0.6.0`.

La revision incluye:

- comandos CLI disponibles;
- tests automatizados;
- compilacion Python;
- arquitectura interna;
- seguridad y modo solo lectura;
- documentacion principal;
- evidencias de Work Orders;
- estado Git;
- ausencia de archivos temporales relevantes.

Esta Work Order no crea release, no crea tag, no cambia version y no publica `v0.6.0` como final.

## 2. Resumen ejecutivo

Frankie Core `0.6.0-dev` esta en condiciones de preparar una release candidata `v0.6.0`.

Los comandos principales funcionan:

- `python -m frankie`
- `python -m frankie version`
- `python -m frankie help`
- `python -m frankie status`
- `python -m frankie inventory`
- `python -m frankie audit`
- `python -m frankie audit --verbose`
- `python -m frankie doctor`
- `python -m frankie doctor --verbose`

La suite de tests pasa correctamente. La compilacion con `compileall` no detecta errores. La arquitectura mantiene separacion por capas y el comportamiento sigue siendo de solo lectura.

El proyecto conserva valor pedagogico: permite explicar CLI, inventario, auditoria, diagnostico sin reparacion, evidencias, versionado, validacion previa y preparacion de release.

## 3. Estado funcional de comandos

| Comando | Resultado | Observacion |
| --- | --- | --- |
| `python -m frankie` | PASS | Muestra ayuda principal y comandos disponibles. |
| `python -m frankie version` | PASS | Muestra `Frankie Core 0.6.0-dev`. |
| `python -m frankie help` | PASS | Lista `version`, `help`, `status`, `inventory`, `audit` y `doctor`; no quedan placeholders. |
| `python -m frankie status` | PASS | Responde como estado conocido de Frankie segun evidencias locales. |
| `python -m frankie inventory` | PASS | Responde que compone Frankie segun documentacion y evidencias. |
| `python -m frankie audit` | PASS | Ejecuta checks documentales, muestra evidencias, hallazgos y resultado global. |
| `python -m frankie audit --verbose` | PASS | Amplia categoria, descripcion y recomendacion. |
| `python -m frankie doctor` | PASS | Explica hallazgos, impacto probable, pasos seguros y acciones que no deben hacerse. |
| `python -m frankie doctor --verbose` | PASS | Incluye check de origen, estado, severidad, resultado y razon de no reparacion. |

Resultado actual observado:

- `status`: `WARNING`, por desviacion conocida de Portainer y validacion SMB pendiente.
- `inventory`: fuentes completas, `14 of 14`, sin fuentes faltantes.
- `audit`: `WARN`, con 5 checks `PASS`, 1 `WARN` y 1 `PENDING`.
- `doctor`: `ACTIONS_RECOMMENDED`, coherente con los hallazgos de auditoria.

## 4. Resultado de tests

Comando ejecutado:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 34 tests
OK
```

La cobertura funcional incluye comandos basicos, modo solo lectura, `status`, `inventory`, `audit`, `doctor` y ausencia de placeholders foundation.

## 5. Resultado de compileall

Comando ejecutado:

```bash
python -m compileall frankie
```

Resultado:

```text
OK
```

No se detectaron errores de compilacion Python.

Los directorios `__pycache__` generados localmente durante esta comprobacion fueron eliminados despues de la prueba.

## 6. Revision arquitectonica

La arquitectura mantiene separacion adecuada:

```text
frankie/
  app.py              despachador CLI
  cli/                parser argparse
  commands/           capa fina de comandos
  core/               constantes, modelos, rutas y estado
  inventory/          lector de inventario
  audit/              motor, checks y reglas
  doctor/             diagnostico y consejos
  output/             renderizado de consola
```

Hallazgos:

- Los modulos en `commands/` son finos y delegan en motores o lectores.
- `status`, `inventory`, `audit` y `doctor` permanecen separados.
- `audit` no depende de `doctor`.
- `doctor` reutiliza `run_audit()` de forma programatica, sin `subprocess`.
- Los modelos en `core/models.py` son reutilizables para futuras salidas JSON, Markdown, dashboard, API o IA.
- Las rutas de evidencias estan centralizadas en `core/paths.py`.
- `output/console.py` concentra el renderizado de consola.

Riesgos arquitectonicos no bloqueantes:

- Existe una carpeta historica `cli/` fuera del paquete principal. No interfiere con Frankie Core, pero conviene revisarla antes de una release publica final para evitar confusion.
- Hay modulos placeholder futuros en `frankie/services/` y `frankie/utils/safe_subprocess.py`. No se usan en los flujos actuales.
- `ATTENTION_REQUIRED` existe como resultado Doctor permitido, pero el algoritmo actual no lo emite. No bloquea la release foundation.

## 7. Revision de seguridad

Se revisaron patrones sensibles:

```text
subprocess
os.system
popen
open(..., "w")
open(..., "a")
write_text
unlink
remove
rmdir
shutil.rmtree
ssh
docker
systemctl
requests
urllib
socket
.env
password
secret
token
client_secret
SMTP_PASSWORD
private key
repair
restart
```

Resultado:

- `subprocess` aparece en tests para ejecutar la CLI localmente.
- `write_text` aparece en tests para crear evidencias temporales dentro de `TemporaryDirectory`.
- `Docker`, `SSH`, `.env`, `systemctl`, `repair` y `restart` aparecen en documentacion, texto explicativo o recomendaciones de no actuacion.
- `frankie/utils/safe_subprocess.py` es un placeholder documentado para futuras comprobaciones de solo lectura; no forma parte del flujo productivo actual.
- Los comandos productivos no ejecutan comandos externos.
- No se detectan secretos reales ni credenciales en los flujos de Frankie Core.

Confirmaciones:

- No escribe ficheros.
- No modifica ficheros.
- No borra ficheros.
- No ejecuta scripts Bash.
- No usa SSH.
- No accede a Internet.
- No lee credenciales.
- No lee `.env`.
- No repara nada.
- No se conecta al servidor fisico Frankie.

## 8. Revision de documentacion

Documentos revisados:

| Documento | Estado |
| --- | --- |
| `README.md` | Existe |
| `CHANGELOG.md` | Existe |
| `ROADMAP.md` | Existe |
| `docs/frankie-core/README.md` | Existe |
| `docs/frankie-core/status.md` | Existe |
| `docs/frankie-core/inventory.md` | Existe |
| `docs/frankie-core/audit.md` | Existe |
| `docs/frankie-core/doctor.md` | Existe |

La documentacion explica:

- que es Frankie;
- que es Frankie Core;
- que es el repositorio Frankie;
- diferencia entre servidor fisico, herramienta software y documentacion;
- comandos disponibles;
- proposito de cada comando;
- limitaciones;
- modo solo lectura;
- ausencia de conexion en vivo;
- ausencia de reparacion;
- utilidad pedagogica;
- estado `0.6.0-dev`;
- que `v0.6.0` no esta cerrada todavia.

## 9. Revision de evidencias

Ruta revisada:

```text
docs/evidencias/frankie-core-v0.6.0/
```

Evidencias presentes:

- `auditoria_core_cli_foundation.md`
- `status_mvp_audit.md`
- `status_mvp_architecture_review.md`
- `inventory_mvp_audit.md`
- `inventory_mvp_architecture_review.md`
- `audit_engine_v1_audit.md`
- `audit_engine_v1_architecture_review.md`
- `doctor_mvp_audit.md`
- `doctor_mvp_architecture_review.md`

No faltan las evidencias esperadas para WO-0001 a WO-0005.

## 10. Revision de Git

Comandos ejecutados:

```bash
git status
git log --oneline -5
git tag
```

Resultado:

- Working tree limpio antes de crear este informe.
- Ultimos commits coherentes:
  - `164032a docs: record server maintenance and resource backups`
  - `1bc1579 feat: add Frankie Doctor MVP`
  - `db8c536 feat: add Frankie Audit Engine v1`
  - `2505b65 feat: add Frankie Inventory MVP`
  - `5988a48 feat: add Frankie Core CLI foundation`
- No hay tags locales.
- No existe tag `v0.6.0`.
- No se ha creado release en esta Work Order.

Tras crear este informe, el working tree queda con este documento pendiente de commit.

## 11. Archivos temporales

Se detectaron directorios `__pycache__` y ficheros `.pyc` generados por la validacion `compileall`.

Accion realizada:

- eliminados `__pycache__/` locales generados durante la comprobacion.

No se detectaron `.env`, logs, dumps SQL, backups comprimidos ni zips generados para incluir.

## 12. Riesgos detectados

| Riesgo | Severidad | Estado | Recomendacion |
| --- | --- | --- | --- |
| Portainer publica `8000`, aunque UFW no lo permite. | Menor | Conocido | Decidir si se mantiene por compatibilidad o se elimina del compose. |
| Validacion SMB desde cliente Windows real sigue pendiente. | Menor | Pendiente | Ejecutar prueba desde un equipo Windows del aula. |
| Carpeta historica `cli/` fuera del paquete principal puede confundir. | Menor | No bloqueante | Revisar antes de release publica final o documentar su estado. |
| Metapaquetes de kernel retenidos en las VMs. | Operativo, fuera de Core | No bloqueante para software | Planificar ventana de mantenimiento si se actualiza kernel. |
| No hay salida JSON/Markdown en CLI actual. | Mejora futura | No bloqueante | Programar para una version posterior. |

## 13. Correcciones menores realizadas

No se realizaron correcciones funcionales ni documentales fuera de este informe.

Se eliminaron caches locales generadas por las pruebas (`__pycache__`).

## 14. Elementos pendientes antes de release

Antes de publicar `v0.6.0`, se recomienda:

1. Revisar si la carpeta historica `cli/` debe mantenerse, archivarse o explicarse.
2. Ejecutar una ultima busqueda de secretos sobre todo el repositorio.
3. Decidir si las evidencias con datos de infraestructura interna son aptas para repositorio publico.
4. Validar SMB desde cliente Windows real y documentar el resultado.
5. Revisar el puerto `8000` de Portainer.
6. Preparar documento de release `v0.6.0`.
7. Actualizar `CHANGELOG.md` moviendo los cambios desde `Unreleased` solo en la Work Order de release.
8. Cambiar version de `0.6.0-dev` a `0.6.0` solo en la Work Order de release.

## 15. Recomendaciones

- Abrir `WO-0006B - Preparar release v0.6.0`.
- Mantener `v0.6.0` como release foundation de solo lectura.
- No introducir nuevas funcionalidades antes de cerrar la release.
- Limitar WO-0006B a versionado, changelog, documento de release, tag y publicacion controlada.
- Conservar el enfoque pedagogico: explicar que una release no es solo codigo, sino validacion, evidencias y decision documentada.

## 16. Decision final

```text
apto para preparar release v0.6.0
```

Frankie Core `0.6.0-dev` no queda declarado como release final en esta revision.
