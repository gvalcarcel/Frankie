# Informe de publicación de Frankie Core v0.7.0

## Identificación

- Work Order: `WO-0015`.
- Fecha: 2026-06-28.
- Tipo: `OFFLINE`.
- Versión publicada: `v0.7.0`.
- Riesgo para producción: nulo.

## Publicación

- Tag anotado: `v0.7.0`.
- Mensaje del tag: `Frankie Core v0.7.0`.
- Commit asociado: `2c1109ec16ee67658588e52136aa9ee8fcf37e5b`.
- Commit resumido: `2c1109e chore: prepare Frankie Core v0.7.0 release`.
- GitHub Release: `Frankie Core v0.7.0`.
- URL: `https://github.com/gvalcarcel/Frankie/releases/tag/v0.7.0`.
- Publicada: 2026-06-28 08:40:34 UTC.
- Draft: no.
- Pre-release: no.
- Latest: sí.
- Assets de código fuente ZIP y TAR.GZ: disponibles.

## Método de publicación

El tag anotado se creó con Git y se subió directamente a `origin`.

GitHub CLI no estaba disponible. La GitHub Release se creó mediante la API oficial de GitHub, usando la autenticación del gestor de credenciales de Git. La credencial se mantuvo en memoria durante la solicitud y no se mostró, escribió ni incorporó al repositorio.

Las notas se tomaron de `docs/releases/v0.7.0.md`. La API confirmó que el cuerpo publicado coincide con el documento versionado.

## Validación previa

Antes de crear el tag se confirmó:

- working tree limpio;
- rama `main`;
- último commit correspondiente a la preparación de `v0.7.0`;
- versión `0.7.0`;
- ausencia previa del tag y de la GitHub Release `v0.7.0`;
- CLI completa en modo offline;
- JSON válido en Status, Inventory, Audit y Doctor;
- seis evidencias válidas y ninguna inválida.

## Tests y compilación

```text
python -m unittest discover -s tests
Ran 68 tests
OK

python -m compileall frankie
OK
```

Las cachés Python generadas durante la validación se retiraron antes de crear el tag.

## Estado funcional publicado

- SMB: `OK / PASS / INFO`.
- Portainer puerto 8000: `WARNING / WARN / LOW`.
- Status global: `WARNING`.
- Audit global: `WARN`.
- Evidence validate: `PASS`.

El aviso de Portainer permanece visible y no fue corregido durante esta publicación.

## Verificación de GitHub

- El tag remoto `v0.7.0^{}` apunta a `2c1109ec16ee67658588e52136aa9ee8fcf37e5b`.
- La GitHub Release usa el tag `v0.7.0`.
- La release no es draft ni pre-release.
- La API de GitHub devuelve `v0.7.0` como Latest.
- Los enlaces de código fuente ZIP y TAR.GZ están disponibles.
- No se creó ningún tag o release adicional.

## Seguridad y alcance

- No se implementó ni ejecutó Live Mode real.
- No se implementó ni ejecutó Repair Mode.
- No se accedió al servidor físico Frankie.
- No se accedió a VM100 ni VM101.
- No se modificaron Docker, Samba, Proxmox, Portainer, firewall o backups.
- No se utilizaron secretos en comandos o documentos versionados.
- La publicación solo afectó a Git y GitHub.

## Nota post-release

Este informe se creó después de publicar el tag y la GitHub Release `v0.7.0`. Por tanto, no forma parte del árbol de fuentes capturado por el tag `v0.7.0`.

Su propósito es documentar la publicación en la rama principal mediante un commit posterior. El tag publicado no debe moverse ni reescribirse.

## Riesgos pendientes

- Portainer mantiene el aviso conocido del puerto 8000.
- Las evidencias offline deben renovarse para evitar quedar desactualizadas.
- Live Mode sigue pendiente de Work Orders futuras, separadas y autorizadas.
- El material de aula requiere criterio docente antes de utilizarlo como evaluación formal.

## Decisión final

```text
release publication documented
```
