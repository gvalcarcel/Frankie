#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 04_desplegar_portainer.sh
# Version: 2026-06-25
# Finalidad: desplegar Portainer CE con volumen persistente.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
CONTAINER_NAME="${CONTAINER_NAME:-portainer}"
VOLUME_NAME="${VOLUME_NAME:-portainer_data}"
PORTAINER_IMAGE="${PORTAINER_IMAGE:-portainer/portainer-ce:latest}"
FORCE_RECREATE="${FORCE_RECREATE:-false}"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root

docker volume inspect "$VOLUME_NAME" >/dev/null 2>&1 || run_cmd docker volume create "$VOLUME_NAME"

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  if [[ "$FORCE_RECREATE" == "true" ]]; then
    run_cmd docker rm -f "$CONTAINER_NAME"
  else
    log "El contenedor $CONTAINER_NAME ya existe. No se recrea."
    run_cmd docker ps -a --filter "name=^/${CONTAINER_NAME}$"
    exit 0
  fi
fi

run_cmd docker run -d \
  --name "$CONTAINER_NAME" \
  --restart=unless-stopped \
  -p 9443:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "${VOLUME_NAME}:/data" \
  "$PORTAINER_IMAGE"

log "Validacion"
run_cmd docker ps --filter "name=^/${CONTAINER_NAME}$"
