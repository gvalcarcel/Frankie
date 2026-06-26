# Checklist de validación - Frankie CLI

## Seguridad

- [ ] La CLI es de solo lectura.
- [ ] No instala paquetes.
- [ ] No reinicia servicios.
- [ ] No borra archivos.
- [ ] No se conecta por SSH en `v0.6.0`.
- [ ] No contiene secretos.
- [ ] No escribe archivos salvo con `--output`.
- [ ] No sobrescribe ficheros existentes.

## Comandos

- [ ] `frankie version` muestra versión, proyecto y modo.
- [ ] `frankie help` muestra comandos y documentación relacionada.
- [ ] `frankie status` lee evidencias locales.
- [ ] `frankie inventory` muestra inventario documentado.
- [ ] `frankie audit` lista scripts de auditoría sin ejecutarlos.

## Formatos

- [ ] Salida `text` legible.
- [ ] Salida `json` válida.
- [ ] Salida `markdown` válida.
- [ ] `--output` genera fichero solo si no existe previamente.

## Pruebas

- [ ] Tests unitarios ejecutados.
- [ ] Tests de CLI ejecutados con `python -m unittest`.
- [ ] Ejecución manual básica revisada.

## Decisión

- [ ] Apto para `v0.6.0`.
- [ ] Requiere revisión.
- [ ] No apto.
