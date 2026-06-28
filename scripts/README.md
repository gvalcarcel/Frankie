# Scripts

Scripts preparatorios para automatizar tareas de implantación del proyecto Frankie.

## Aviso

Revisar siempre antes de ejecutar en producción. Los scripts están preparados para ejecución controlada, pero siguen siendo automatizaciones sensibles.

No deben contener contraseñas, tokens ni secretos reales.

## Validación OFFLINE de Frankie Core

El flujo local de tests, regresión CLI, evidencias e informes se ejecuta con:

```bash
python scripts/validation/validate_evidence_flow.py
```

No actúa sobre servidores. Consulta [scripts/validation/README.md](validation/README.md) antes de usar `--force` o `--require-clean`.

## Uso de dry-run

Todos los scripts aceptan:

```bash
./script.sh --dry-run
```

El modo `--dry-run` muestra las acciones previstas sin ejecutarlas.

## Ejecucion real

Cuando se haya revisado el dry-run:

```bash
sudo ./script.sh
```

## Orden recomendado - srv-servicios

1. `01_instalar_dependencias.sh`
2. `02_instalar_docker.sh`
3. `03_crear_red_docker.sh`
4. `04_desplegar_portainer.sh`
5. Preparar `.env` reales fuera de Git.
6. `05_desplegar_postgres.sh`
7. `06_desplegar_n8n.sh`
8. `07_configurar_backup.sh`
9. `08_configurar_seguridad.sh`

## Orden recomendado - srv-recursos

1. `01_instalar_samba.sh`
2. `02_crear_usuarios_samba.sh`
3. Configurar passwords Samba con `smbpasswd` manualmente.
4. `03_crear_estructura_recursos.sh`
5. `04_aplicar_permisos.sh`
6. `05_configurar_smb_conf.sh`
7. `06_configurar_firewall.sh`
8. `07_configurar_backup_recursos.sh`

## Principios aplicados

- `set -euo pipefail`.
- Variables configurables al inicio.
- Funciones `log()` y `run_cmd()`.
- Idempotencia razonable.
- Validacion al final.
- Sin secretos reales.

## Paso 4: validación previa

Antes de ejecutar scripts reales en una VM:

1. Crear snapshot.
2. Confirmar backup.
3. Ejecutar auditoría de solo lectura.
4. Ejecutar `--dry-run`.
5. Revisar salida.
6. Ejecutar un solo script.
7. Validar.
8. Documentar resultado.

## Auditoria

Los scripts de `scripts/auditoria/` son de solo lectura:

```bash
./scripts/auditoria/auditar_srv-servicios.sh
./scripts/auditoria/auditar_srv-recursos.sh
```

No instalan paquetes, no reinician servicios y no modifican configuración.

## Reglas antes de ejecución real

- No ejecutar sin snapshot.
- No ejecutar sin leer el script.
- No ejecutar si el dry-run muestra acciones inesperadas.
- No ejecutar si faltan `.env` reales fuera de Git.
- No ejecutar varios scripts a la vez.
- No ejecutar si hay servicios fallidos sin diagnosticar.
