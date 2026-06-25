#!/bin/bash
set -euo pipefail

# Frankie - srv-recursos - 01_instalar_samba.sh
# Version: 2026-06-25
# Finalidad: instalar Samba y utilidades base.
# Aviso: revisar antes de ejecutar en produccion.

DRY_RUN=false
PACKAGES=(samba ufw tree)
for arg in "$@"; do case "$arg" in --dry-run) DRY_RUN=true ;; *) echo "Uso: $0 [--dry-run]" >&2; exit 2 ;; esac; done
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
run_cmd() { if "$DRY_RUN"; then echo "[DRY-RUN] $*"; else "$@"; fi; }
require_root() { [[ "${EUID}" -eq 0 ]] || { echo "ERROR: ejecuta con sudo o root." >&2; exit 1; }; }
pkg_installed() { dpkg -s "$1" >/dev/null 2>&1; }

require_root
run_cmd apt update
missing=()
for pkg in "${PACKAGES[@]}"; do pkg_installed "$pkg" || missing+=("$pkg"); done
[[ "${#missing[@]}" -eq 0 ]] || run_cmd env DEBIAN_FRONTEND=noninteractive apt install -y "${missing[@]}"
run_cmd systemctl enable --now smbd

log "Validacion"
run_cmd systemctl status smbd --no-pager
