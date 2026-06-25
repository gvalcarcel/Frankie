#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 03_crear_red_docker.sh
# Version: 2026-06-25
# Finalidad: crear la red Docker externa aula-network si no existe.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
NETWORK_NAME="${NETWORK_NAME:-aula-network}"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root

if docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
  log "La red $NETWORK_NAME ya existe"
else
  run_cmd docker network create "$NETWORK_NAME"
fi

log "Validacion"
run_cmd docker network ls
if ! "$DRY_RUN"; then docker network inspect "$NETWORK_NAME" >/dev/null; fi
