# Auditoria final de release - v0.6.0

Fecha: 2026-06-27

Tipo de Work Order: `OFFLINE`

Decision final: `apto para registrar release preparada`

## 1. Alcance

Esta auditoria revisa la preparacion local de Frankie Core `v0.6.0` antes de registrarla en GitHub. Comprueba version, documentacion, comportamiento funcional, tests, arquitectura, seguridad, estado Git y riesgos conocidos.

La auditoria no se conecto al servidor fisico Frankie ni a sus maquinas virtuales. No uso SSH, Docker o Samba, no ejecuto scripts de produccion y no modifico servidores.

## 2. Resumen ejecutivo

La preparacion de `v0.6.0` es coherente y supera todas las comprobaciones obligatorias. La version esta sincronizada, los comandos funcionan en modo solo lectura, los 37 tests pasan y el paquete compila correctamente.

La evidencia actual mantiene SMB como validado y conserva el unico aviso activo: Portainer publica el puerto `8000`. Este riesgo permanece visible como `WARN / LOW` y no bloquea el registro de la release preparada.

## 3. Archivos revisados

- `frankie/core/constants.py`
- `frankie/core/status.py`
- `frankie/audit/checks.py`
- `pyproject.toml`
- `CHANGELOG.md`
- `README.md`
- `ROADMAP.md`
- `docs/arquitectura.md`
- `docs/frankie-core/README.md`
- `docs/frankie-core/status.md`
- `docs/frankie-core/inventory.md`
- `docs/frankie-core/audit.md`
- `docs/frankie-core/doctor.md`
- `docs/releases/README.md`
- `docs/releases/v0.6.0.md`
- `docs/evidencias/frankie-core-v0.6.0/release_preparation_audit.md`
- `tests/test_version.py`
- `tests/test_status.py`
- `tests/test_inventory.py`
- `tests/test_audit.py`
- `tests/test_doctor.py`
- Resto de archivos modificados y no versionados mostrados por `git status`.

## 4. Correcciones realizadas

Se corrigio una ambiguedad documental para identificar de forma inequivoca a Frankie como el servidor fisico y a VM100 como `srv-servicios`. El hostname del nodo Proxmox, `srv-aula113`, se conserva como dato tecnico diferenciado del nombre del servidor.

No fue necesaria ninguna correccion de codigo, tests o documentacion funcional de Frankie Core.

Se eliminaron exclusivamente los directorios `__pycache__` y ficheros `.pyc` generados por las comprobaciones locales.

## 5. Validacion de version

| Comprobacion | Resultado |
| --- | --- |
| `frankie/core/constants.py` | `VERSION = "0.6.0"` |
| `pyproject.toml` | `version = "0.6.0"` |
| `python -m frankie version` | `Frankie Core 0.6.0` |

Las referencias a `0.6.0-dev` restantes pertenecen a evidencias historicas o al documento de transicion de la version anterior a la actual. No se encontraron referencias obsoletas usadas como version actual.

## 6. Validacion de CHANGELOG

`CHANGELOG.md` contiene la seccion `[v0.6.0] - 2026-06-26` y mantiene `Unreleased` preparado para cambios futuros.

La seccion incluye CLI Foundation, Status MVP, Inventory MVP, Audit Engine v1, Doctor MVP, readiness review, comprobacion live pre-release, sincronizacion de evidencia SMB, documentacion, evidencias, tests y garantia de solo lectura.

Tambien documenta el riesgo de Portainer puerto `8000` y no afirma que exista tag o GitHub Release.

## 7. Validacion del documento de release

`docs/releases/v0.6.0.md` contiene nombre, fecha, resumen ejecutivo, alcance, comandos, estados esperados, evidencias, riesgos, limitaciones, exclusiones, uso pedagogico, criterios de validacion y resultado final.

El documento deja claro que:

- no existe conexion live con Frankie fisico;
- no existe reparacion automatica;
- no se ejecutan comandos externos contra servidores;
- la release se basa en evidencias documentadas;
- SMB esta validado por evidencia pre-release;
- Portainer puerto `8000` permanece como `WARN`;
- la release aun no esta publicada.

## 8. Validacion funcional de comandos

| Comando | Codigo | Resultado |
| --- | ---: | --- |
| `python -m frankie` | 0 | Ayuda general y version `0.6.0`. |
| `python -m frankie version` | 0 | Version `0.6.0`. |
| `python -m frankie help` | 0 | Lista completa de comandos. |
| `python -m frankie status` | 0 | Estado global `WARNING` por Portainer; SMB `OK`. |
| `python -m frankie inventory` | 0 | Inventario disponible; 15 de 15 fuentes. |
| `python -m frankie audit` | 0 | Resultado global `WARN`; 6 `PASS` y 1 `WARN`. |
| `python -m frankie audit --verbose` | 0 | Evidencias y recomendaciones detalladas. |
| `python -m frankie doctor` | 0 | `ACTIONS_RECOMMENDED` por Portainer. |
| `python -m frankie doctor --verbose` | 0 | Diagnostico ampliado, sin reparacion automatica. |

## 9. Resultado de tests

Comando:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 37 tests
OK
```

## 10. Resultado de compileall

Comando:

```bash
python -m compileall frankie
```

Resultado: `OK`.

## 11. Validacion de arquitectura

- `commands/` conserva handlers finos que delegan en motores y renderizadores.
- `core/` mantiene constantes, rutas, estado y modelos comunes.
- `inventory/` mantiene el lector de inventario.
- `audit/` mantiene motor, checks y reglas.
- `doctor/` reutiliza `run_audit()` programaticamente y no usa subprocess.
- `audit` no depende de `doctor`.
- `output/` mantiene el renderizado separado.
- `status`, `inventory`, `audit` y `doctor` funcionan de manera independiente.
- Los informes y hallazgos siguen representados por modelos reutilizables para futuras salidas JSON, Markdown, API o dashboard.

No se detecto ruptura arquitectonica causada por la preparacion de release.

## 12. Validacion de seguridad

Se revisaron los cambios pendientes en busca de secretos, credenciales, IPs, usuarios personales y operaciones peligrosas.

Resultado:

- no se detectaron contrasenas ni tokens;
- no se detectaron claves privadas ni certificados;
- no se detectaron credenciales reales;
- no se detectaron IPs internas nuevas en los cambios;
- no se detectaron ficheros `.env`, dumps SQL, logs ni backups comprimidos versionados;
- no se detectaron llamadas nuevas a SSH, Docker, systemd, red o subprocess;
- no se detectaron escrituras, borrados, reinicios ni reparaciones en runtime;
- las coincidencias con `repair` son advertencias documentales que explican que esa capacidad no existe.

## 13. Estado SMB

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO
```

La evidencia pre-release resuelve el pendiente operativo de SMB. Las evidencias historicas se conservan para trazabilidad.

## 14. Estado Portainer

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN / LOW
Doctor: ACTIONS_RECOMMENDED
```

El puerto `8000` sigue publicado segun la evidencia documentada. La release no oculta ni corrige automaticamente este hallazgo.

## 15. Estado Git

- Rama: `main`.
- `HEAD`: `b5663cab5c2abb585ad3c63689916557b381266d`.
- `origin/main`: `b5663cab5c2abb585ad3c63689916557b381266d`.
- Existen cambios locales de WO-0007 y este informe final pendientes de commit.
- No existen conflictos.
- No se detectaron temporales tras la limpieza.
- No existe tag local o remoto `v0.6.0`.
- GitHub informa de cero releases.
- No se realizo push durante esta Work Order.

Advertencia menor: Git muestra avisos de normalizacion futura de finales de linea `LF` a `CRLF` en el entorno Windows. No afecta al contenido ni a la validacion.

## 16. Riesgos conocidos

| Riesgo | Estado | Tratamiento |
| --- | --- | --- |
| Portainer publica el puerto `8000`. | `WARN / LOW` | Revisar su necesidad en una Work Order posterior. |
| El estado depende de evidencias documentadas. | Aceptado | Evolucionar a evidencias estructuradas. |
| No existe modo live. | Aceptado | Disenarlo con permisos y limites explicitos. |
| No existe modo repair. | Aceptado | Mantener control humano y seguridad por defecto. |
| Normalizacion `LF`/`CRLF` en Windows. | Menor | Definir una politica `.gitattributes` en trabajo futuro si se considera necesario. |

## 17. Pendientes posteriores a release

- Registrar los cambios preparados mediante WO-0007B.
- Crear el tag y publicar GitHub Release solo mediante WO-0007C.
- Decidir si Portainer necesita el puerto `8000`.
- Disenar salida JSON y evidencias estructuradas en versiones posteriores.
- Disenar por separado cualquier modo live, dashboard o integracion IA.

## 18. Confirmaciones de control

- No se creo commit.
- No se hizo push.
- No se creo tag.
- No se creo GitHub Release.
- No se tocaron servidores.
- No se anadieron funcionalidades.

## 19. Decision final

```text
apto para registrar release preparada
```

La release preparada satisface los criterios tecnicos, documentales, arquitectonicos y de seguridad de WO-0007A. Esta decision autoriza el siguiente paso documental y Git, pero no publica por si misma `v0.6.0`.
