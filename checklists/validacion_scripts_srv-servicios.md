# Validacion de scripts - srv-servicios

## 01_instalar_dependencias.sh

Objetivo: instalar paquetes base.

Comando dry-run:

```bash
./01_instalar_dependencias.sh --dry-run
```

Debe mostrar:

- `apt update`.
- Instalacion solo de paquetes faltantes.
- Validacion de paquetes.

No debe hacer:

- Reiniciar la VM.
- Cambiar configuracion Docker.
- Tocar servicios n8n/PostgreSQL.

Validaciones posteriores:

- `dpkg -s ufw fail2ban tree`.
- `systemctl status fail2ban`.

Riesgo: bajo.

Decision final: apto / revisar / no ejecutar.

## 02_instalar_docker.sh

Objetivo: instalar Docker desde repositorio oficial.

Comando dry-run:

```bash
./02_instalar_docker.sh --dry-run
```

Debe mostrar:

- Creacion de `/etc/apt/keyrings`.
- Configuracion de repositorio Docker solo si falta.
- Instalacion de Docker Engine, CLI, containerd, buildx y compose.

No debe hacer:

- Duplicar repositorio Docker.
- Borrar contenedores.
- Reiniciar servicios ajenos.

Validaciones posteriores:

- `docker version`.
- `docker compose version`.
- `systemctl status docker`.

Riesgo: medio.

Decision final: apto / revisar / no ejecutar.

## 03_crear_red_docker.sh

Objetivo: crear `aula-network` si no existe.

Comando dry-run:

```bash
./03_crear_red_docker.sh --dry-run
```

Debe mostrar:

- Inspeccion de red.
- Creacion solo si falta.

No debe hacer:

- Eliminar redes existentes.
- Reconectar contenedores.

Validaciones posteriores:

- `docker network inspect aula-network`.

Riesgo: bajo.

Decision final: apto / revisar / no ejecutar.

## 04_desplegar_portainer.sh

Objetivo: desplegar Portainer CE.

Comando dry-run:

```bash
./04_desplegar_portainer.sh --dry-run
```

Debe mostrar:

- Creacion de volumen `portainer_data` si falta.
- Despliegue en puerto `9443`.
- No recrear si ya existe salvo `FORCE_RECREATE=true`.

No debe hacer:

- Borrar volumen `portainer_data`.
- Recrear contenedor existente sin autorizacion.

Validaciones posteriores:

- `docker ps --filter name=portainer`.
- Acceso a `https://IP:9443`.

Riesgo: medio.

Decision final: apto / revisar / no ejecutar.

## 05_desplegar_postgres.sh

Objetivo: desplegar PostgreSQL 17 sin exponer `5432`.

Comando dry-run:

```bash
./05_desplegar_postgres.sh --dry-run
```

Debe mostrar:

- Comprobacion de `aula-network`.
- Uso de `.env` real no versionado.
- Despliegue con Docker Compose.

No debe hacer:

- Publicar `5432:5432`.
- Borrar `/srv/docker/postgres/data`.
- Crear secretos en Git.

Validaciones posteriores:

- `docker ps --filter name=postgres`.
- `ss -tlnp | grep 5432` no debe mostrar escucha en host.
- `docker logs postgres --tail=50`.

Riesgo: alto.

Decision final: apto / revisar / no ejecutar.

## 06_desplegar_n8n.sh

Objetivo: desplegar n8n en `5678`.

Comando dry-run:

```bash
./06_desplegar_n8n.sh --dry-run
```

Debe mostrar:

- Comprobacion de PostgreSQL activo.
- Comprobacion de `aula-network`.
- Uso de `.env` real no versionado.

No debe hacer:

- Borrar `/srv/docker/n8n/data`.
- Cambiar credenciales.
- Publicar puertos no previstos.

Validaciones posteriores:

- `docker ps --filter name=n8n`.
- `curl -I http://localhost:5678`.
- Revision de logs.

Riesgo: alto.

Decision final: apto / revisar / no ejecutar.

## 07_configurar_backup.sh

Objetivo: instalar backup diario de servicios.

Comando dry-run:

```bash
./07_configurar_backup.sh --dry-run
```

Debe mostrar:

- Creacion de carpetas bajo `/srv/docker/backups`.
- Instalacion de script.
- Entrada cron a las `02:00`.

No debe hacer:

- Duplicar entradas cron.
- Borrar backups existentes.

Validaciones posteriores:

- `crontab -l`.
- `ls -lah /srv/docker/backups`.

Riesgo: medio.

Decision final: apto / revisar / no ejecutar.

## 08_configurar_seguridad.sh

Objetivo: configurar UFW y Fail2ban.

Comando dry-run:

```bash
./08_configurar_seguridad.sh --dry-run
```

Debe mostrar:

- Politica deny incoming.
- Allow outgoing.
- Reglas `22/tcp`, `5678/tcp`, `9443/tcp`.
- Configuracion Fail2ban SSH.

No debe hacer:

- Cerrar SSH accidentalmente.
- Abrir `5432/tcp`.
- Abrir puertos no previstos.

Validaciones posteriores:

- `ufw status verbose`.
- `fail2ban-client status sshd`.

Riesgo: alto.

Decision final: apto / revisar / no ejecutar.
