# Release Publication Report - Frankie Core v0.6.0

Fecha: 2026-06-27

Tipo de Work Order: `OFFLINE`

Decisión final: `listo para registrar documentación post-release`

## 1. Resumen

Frankie Core `v0.6.0` ha sido publicado oficialmente en GitHub como la primera release estable de Frankie Core.

La publicación formaliza la base Python de consulta, inventario, auditoría y diagnóstico en modo solo lectura. Su funcionamiento se apoya en evidencias documentadas del repositorio y no requiere conexión en vivo con la infraestructura.

## 2. Estado de publicación

```text
Release: Frankie Core v0.6.0
Tag: v0.6.0
Estado en GitHub: Latest
Draft: no
Prerelease: no
Assets: Source code zip / Source code tar.gz
```

URL pública:

`https://github.com/gvalcarcel/Frankie/releases/tag/v0.6.0`

## 3. Tag y commit asociados

| Elemento | Valor |
| --- | --- |
| Tag local | `v0.6.0` |
| Tag remoto | `v0.6.0` |
| Tipo | Tag anotado |
| Mensaje | `Frankie Core v0.6.0` |
| Commit | `000013dc5f75d7d22f95604399633651f5a98b39` |
| Commit resumido | `000013d chore: prepare Frankie Core v0.6.0 release` |

La referencia remota `refs/tags/v0.6.0^{}` apunta al mismo commit.

## 4. Método de publicación y validación

El tag anotado se creó localmente y se subió a `origin` durante WO-0007C.

GitHub CLI no estaba disponible, por lo que la GitHub Release fue creada posteriormente de forma manual desde la interfaz web de GitHub usando:

- tag: `v0.6.0`;
- título: `Frankie Core v0.6.0`;
- notas: contenido preparado en `docs/releases/v0.6.0.md`.

La existencia y los metadatos de la release se validaron después mediante la API pública de GitHub. La API confirma que no es draft ni prerelease, que `v0.6.0` es la release más reciente y que están disponibles las descargas automáticas `zipball` y `tarball` del código fuente.

## 5. Assets disponibles

GitHub proporciona automáticamente:

- `Source code (zip)`;
- `Source code (tar.gz)`.

No se publicaron binarios ni assets adicionales. La API informa de cero assets adjuntos manualmente y confirma las URLs automáticas de código fuente.

## 6. Validación local de versión

Comando:

```bash
python -m frankie version
```

Resultado:

```text
Frankie Core 0.6.0
Mode: read-only foundation
Project: Frankie
This version does not modify servers or services.
```

## 7. Validación funcional

| Comando | Resultado |
| --- | --- |
| `python -m frankie` | Correcto; muestra ayuda general y versión `0.6.0`. |
| `python -m frankie version` | Correcto; muestra `0.6.0`. |
| `python -m frankie help` | Correcto; lista los comandos disponibles. |
| `python -m frankie status` | `WARNING` global por Portainer; SMB `OK`. |
| `python -m frankie inventory` | Correcto; 15 de 15 fuentes disponibles. |
| `python -m frankie audit` | `WARN` global; 6 `PASS` y 1 `WARN`. |
| `python -m frankie doctor` | `ACTIONS_RECOMMENDED`; una incidencia revisada. |

Todos los comandos finalizaron con código de salida `0`.

## 8. Resultado de tests

Comando:

```bash
python -m unittest discover -s tests
```

Resultado:

```text
Ran 37 tests
OK
```

## 9. Resultado de compileall

Comando:

```bash
python -m compileall frankie
```

Resultado: `OK`.

Las cachés `__pycache__` y los ficheros `.pyc` generados por esta validación fueron eliminados después de la prueba.

## 10. Estado SMB

```text
Samba: OK
Windows/SMB validation: OK
AUD-SAMBA-001: PASS / INFO
```

La evidencia pre-release mantiene resuelto el pendiente histórico de validación SMB.

## 11. Estado Portainer

```text
Portainer: WARNING
AUD-SERVICES-PORTAINER-001: WARN / LOW
Doctor: ACTIONS_RECOMMENDED
```

El puerto `8000` de Portainer continúa documentado como advertencia conocida. La publicación no oculta ni corrige automáticamente este hallazgo.

## 12. Riesgos conocidos

| Riesgo | Estado | Tratamiento |
| --- | --- | --- |
| Portainer publica el puerto `8000`. | `WARN / LOW` | Revisar su necesidad en una Work Order posterior. |
| El estado depende de evidencias documentadas. | Aceptado | Evolucionar hacia evidencias estructuradas. |
| No existe modo live. | Aceptado | Diseñarlo con permisos y límites explícitos. |
| No existe modo repair. | Aceptado | Mantener control humano y seguridad por defecto. |

## 13. Impacto sobre servidores

No fue necesario conectarse al servidor físico Frankie.

No se modificaron Frankie, Proxmox, las máquinas virtuales, Docker, Samba, PostgreSQL, n8n, UFW, Fail2ban ni la configuración de backups.

No se usó SSH, no se ejecutaron scripts de producción y no se realizó ninguna acción live.

## 14. Control de publicación

- El tag `v0.6.0` ya existía antes de esta Work Order.
- No se creó ningún tag adicional.
- La GitHub Release `v0.6.0` ya había sido creada manualmente antes de esta Work Order.
- No se creó ninguna release adicional.
- No se modificó la GitHub Release existente.
- No se realizaron commits ni push durante esta Work Order.

## 15. Nota post-release

Este informe se creó después de publicar el tag `v0.6.0` y la GitHub Release correspondiente.

Por tanto, constituye documentación post-release y no forma parte del árbol de fuentes capturado por el tag `v0.6.0`. Su registro en la rama principal deberá realizarse mediante una Work Order posterior, sin mover ni reescribir el tag publicado.

## 16. Decisión

```text
listo para registrar documentación post-release
```

La publicación oficial de la primera release estable de Frankie Core queda verificada y documentada. El informe está preparado para revisión antes de registrarse en GitHub mediante WO-0007E.
