#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 04_aplicar_permisos.sh
# Version: 2026-06-25
# Finalidad: aplicar permisos de alumnado/profesorado en /srv/recursos.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
BASE_DIR="${BASE_DIR:-/srv/recursos}"
PROF_GROUP="${PROF_GROUP:-profesorado}"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root
getent group "$PROF_GROUP" >/dev/null || { echo "ERROR: falta grupo $PROF_GROUP" >&2; exit 1; }
[[ -d "$BASE_DIR" ]] || { echo "ERROR: falta $BASE_DIR" >&2; exit 1; }

run_cmd chown -R "root:${PROF_GROUP}" "$BASE_DIR"
run_cmd chmod 755 "$BASE_DIR"
run_cmd find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d -exec chmod 755 {} +
run_cmd chmod 2775 "$BASE_DIR/02_ISOS"
run_cmd chmod 2770 "$BASE_DIR/07_ENTREGAS" "$BASE_DIR/99_PROFESORADO"

log "Validacion"
run_cmd ls -ld "$BASE_DIR" "$BASE_DIR/02_ISOS" "$BASE_DIR/07_ENTREGAS" "$BASE_DIR/99_PROFESORADO"
