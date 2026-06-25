# Estrategia de automatización

## Objetivo

Preparar la implantación del proyecto Frankie para que pueda repetirse y mantenerse con scripts controlados, revisables y seguros.

## Principios

- No ejecutar cambios sin revisión previa.
- Usar `--dry-run` antes de ejecutar en real.
- Mantener scripts idempotentes.
- No versionar secretos.
- Separar plantillas `.example` de configuraciones reales.
- Validar al final de cada script.

## Dry-run

Todos los scripts aceptan:

```bash
./script.sh --dry-run
```

Este modo debe mostrar los comandos previstos sin ejecutarlos. Es obligatorio revisarlo antes de una ejecución real.

## Ejecucion real

Los scripts que modifican sistema requieren privilegios:

```bash
sudo ./script.sh
```

## Idempotencia

Los scripts deben poder ejecutarse mas de una vez sin:

- Duplicar usuarios.
- Duplicar grupos.
- Duplicar redes Docker.
- Duplicar reglas UFW.
- Duplicar entradas cron.
- Duplicar bloques Samba gestionados.

## Secretos

No incluir en Git:

- `.env` reales.
- Passwords SMTP.
- Passwords PostgreSQL.
- Passwords Samba.
- Tokens OAuth.
- Claves privadas.

Los secretos deben venir de variables de entorno, ficheros `.env` no versionados o entrada interactiva segura.

## Revision manual

Antes de producción revisar:

- IPs actuales o reservas DHCP.
- Rutas de datos.
- Usuarios y grupos reales.
- Firewall.
- Backups.
- Restauracion.
- Impacto de reinicios.

## Paso siguiente

En el Paso 4 conviene probar los scripts en modo `--dry-run`, crear un entorno de prueba o snapshot, y ejecutar una validación completa por VM.
