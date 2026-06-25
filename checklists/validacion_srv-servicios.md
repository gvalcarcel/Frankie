# Checklist de validacion - srv-servicios

## Identificacion

- [ ] La VM arranca correctamente.
- [ ] La IP responde desde la red del centro.
- [ ] El hostname es el esperado.
- [ ] La IP coincide con la configurada en `N8N_HOST`.

## Docker

- [ ] `01_instalar_dependencias.sh --dry-run` muestra acciones esperadas.
- [ ] `01_instalar_dependencias.sh` instala paquetes base sin errores.
- [ ] `02_instalar_docker.sh --dry-run` no muestra duplicacion de repositorios.
- [ ] `02_instalar_docker.sh` deja Docker operativo.
- [ ] `docker --version` muestra version instalada.
- [ ] `docker compose version` muestra version instalada.
- [ ] `docker ps` muestra `portainer`, `postgres` y `n8n`.
- [ ] `03_crear_red_docker.sh` crea o detecta `aula-network`.
- [ ] La red `aula-network` existe.
- [ ] No hay contenedores inesperados en ejecucion.

## Portainer

- [ ] `04_desplegar_portainer.sh --dry-run` es correcto.
- [ ] `04_desplegar_portainer.sh` no recrea si ya existe salvo `FORCE_RECREATE=true`.
- [ ] Portainer responde por `https://IP:9443`.
- [ ] El acceso administrativo funciona.
- [ ] El volumen `portainer_data` existe.

## PostgreSQL

- [ ] Existe `.env` real fuera de Git.
- [ ] `05_desplegar_postgres.sh --dry-run` es correcto.
- [ ] `05_desplegar_postgres.sh` despliega sin publicar `5432`.
- [ ] El contenedor `postgres` esta activo.
- [ ] El puerto `5432` no esta publicado hacia la red del centro.
- [ ] `docker ps` muestra solo `5432/tcp`, sin `0.0.0.0:5432`.
- [ ] Los logs muestran que PostgreSQL acepta conexiones.

## n8n

- [ ] Existe `.env` real fuera de Git.
- [ ] `06_desplegar_n8n.sh --dry-run` es correcto.
- [ ] `06_desplegar_n8n.sh` valida PostgreSQL activo.
- [ ] n8n responde por `http://IP:5678`.
- [ ] Se puede iniciar sesion.
- [ ] El log muestra la URL correcta.
- [ ] n8n conecta con PostgreSQL usando host `postgres`.
- [ ] Las invitaciones por correo funcionan, si SMTP esta configurado.

## SMTP

- [ ] Hay una cuenta tecnica definida o aprobada.
- [ ] Las variables SMTP no estan versionadas con secretos reales.
- [ ] Se recibe una invitacion de prueba.

## Seguridad

- [ ] `08_configurar_seguridad.sh --dry-run` es correcto.
- [ ] `08_configurar_seguridad.sh` configura UFW y Fail2ban.
- [ ] UFW esta activo.
- [ ] Solo estan permitidos los puertos necesarios.
- [ ] Fail2ban esta activo.
- [ ] `fail2ban-client status sshd` no muestra errores.

## Backups

- [ ] `07_configurar_backup.sh --dry-run` es correcto.
- [ ] `07_configurar_backup.sh` crea estructura y cron sin duplicados.
- [ ] Existe script de backup.
- [ ] Se ha ejecutado una copia manual.
- [ ] Hay log de backup reciente.
- [ ] Existe dump PostgreSQL reciente.
- [ ] Existe tar.gz de n8n reciente.
- [ ] Existe tar.gz de stacks reciente.

## PostgreSQL no expuesto

- [ ] `ss -tlnp | grep 5432` no muestra escucha en el host.
- [ ] UFW no permite `5432/tcp`.
