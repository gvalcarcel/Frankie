#!/bin/bash
set -euo pipefail

# Frankie - srv-servicios - 07_configurar_backup.sh
# Version: 2026-06-25
# Finalidad: instalar backup diario de PostgreSQL, n8n y stacks.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
BACKUP_BASE="${BACKUP_BASE:-/srv/docker/backups}"
SCRIPT_PATH="${SCRIPT_PATH:-/srv/docker/scripts/backup.sh}"
TEMPLATE="${TEMPLATE:-../../backups/backup-servicios.sh.example}"
CRON_LINE="0 2 * * * ${SCRIPT_PATH}"

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root

run_cmd mkdir -p "$BACKUP_BASE/postgres" "$BACKUP_BASE/n8n" "$BACKUP_BASE/stacks" "$BACKUP_BASE/logs" "$(dirname "$SCRIPT_PATH")"
run_cmd cp "$TEMPLATE" "$SCRIPT_PATH"
run_cmd chmod 750 "$SCRIPT_PATH"

if "$DRY_RUN"; then
  echo "[DRY-RUN] instalar cron: $CRON_LINE"
else
  current="$(mktemp)"
  crontab -l 2>/dev/null > "$current" || true
  if ! grep -Fq "$SCRIPT_PATH" "$current"; then
    echo "$CRON_LINE" >> "$current"
    crontab "$current"
  fi
  rm -f "$current"
fi

log "Validacion"
run_cmd crontab -l
