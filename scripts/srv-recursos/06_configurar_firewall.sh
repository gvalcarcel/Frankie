#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 06_configurar_firewall.sh
# Version: 2026-06-25
# Finalidad: configurar UFW para SSH y Samba.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
RULES=(22/tcp 445/tcp 139/tcp 137/udp 138/udp)

for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }

require_root
run_cmd ufw default deny incoming
run_cmd ufw default allow outgoing
for rule in "${RULES[@]}"; do run_cmd ufw allow "$rule"; done
run_cmd ufw --force enable

log "Validacion"
run_cmd ufw status verbose
