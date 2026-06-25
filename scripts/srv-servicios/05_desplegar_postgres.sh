#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 05_desplegar_postgres.sh
# Version: 2026-06-25
# Finalidad: desplegar PostgreSQL 17 sin exponer 5432 al host.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
NETWORK_NAME="${NETWORK_NAME:-aula-network}"
STACK_DIR="${STACK_DIR:-/srv/docker/stacks/postgres}"
DATA_DIR="${DATA_DIR:-/srv/docker/postgres/data}"
COMPOSE_TEMPLATE="${COMPOSE_TEMPLATE:-../../docker/postgres/docker-compose.yml.example}"
ENV_FILE="${ENV_FILE:-${STACK_DIR}/postgres.env}"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root

docker network inspect "$NETWORK_NAME" >/dev/null 2>&1 || { echo "ERROR: falta red Docker $NETWORK_NAME" >&2; exit 1; }
[[ -f "$ENV_FILE" || "$DRY_RUN" == "true" ]] || { echo "ERROR: falta .env real no versionado: $ENV_FILE" >&2; exit 1; }

run_cmd mkdir -p "$STACK_DIR" "$DATA_DIR"
if [[ ! -f "$STACK_DIR/docker-compose.yml" ]]; then
  run_cmd cp "$COMPOSE_TEMPLATE" "$STACK_DIR/docker-compose.yml"
fi

run_cmd bash -c "cd '$STACK_DIR' && docker compose --env-file '$ENV_FILE' up -d"

log "Validacion"
run_cmd docker ps --filter "name=^/postgres$"
if "$DRY_RUN"; then
  echo "[DRY-RUN] comprobar que 5432 no esta publicado en el host"
else
  if ss -tlnp | grep -q ':5432'; then
    echo "ERROR: 5432 aparece escuchando en el host. Revisar publicacion de puertos." >&2
    exit 1
  fi
  docker logs postgres --tail=50
fi
